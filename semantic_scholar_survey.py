import requests
import argparse
import sys
import csv

def print_paper(p):
    for key,value in p.items():
        print(key+": "+str(value))

def parse_input():
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description='Semantic Scholar Querier')
    parser.add_argument("-q", "--query",help="Search keywords")
    parser.add_argument("-v", "--venue",help="Venue name ('j acm', 'icnc', 'ace', 'nossdav', 'cig', 'infocom'...)")
    parser.add_argument("-l", "--limit", type=int, default=10, help="Number of publications to show (<=100). Default: 10")
    parser.add_argument("-o", "--offset", type=int, default=0, help="Show publications starting from the given ID. Default: 0")
    parser.add_argument("-f", "--filter", action='append', help="Filter out publications that include at least one of these keywords in the title")
    parser.add_argument("-i", "--include", action='append', help="Keep only the publications that include at least one of the keywords in the title or abstract")
    parser.add_argument("--save-csv", action="store_true", help="Save output in a CSV file")
    args = parser.parse_args()
    #print(args)
    #sys.exit()
    return args.query, args.venue, args.limit, args.offset, args.filter, args.include, args.save_csv


def containes_keyword(keyword, title, abstract):
    # Input keyword samples:
    # "cheat OR attack"
    # "online OR multiplayer OR Network"
    # "detect OR prevent"
    # "game theory"
    
    for i in keyword.split(" OR "):
        if i.lower() in title.lower() or i.lower() in abstract.lower():
            #print("Contains "+i)
            return True
    #print("Doesn't contain "+keyword)
    return False

def containes_keywords(keywords, title, abstract):
    # Input keywords samples:
    # ["gam", "cheat OR attack", "online OR multiplayer OR Network", "detect OR prevent"]
    # ["game theory"]

    for kw in keywords:
        if not containes_keyword(kw, title, abstract):
            #print("Doesn't contain "+str(kw))
            return False
    #print("Contains "+str(keywords))
    return True

def write_to_csv(publications_writer, publication):
    publications_writer.writerow(publication)


query, venue, limit, offset, filter, include, save_csv = parse_input()


# Build URL
base_url = "https://api.semanticscholar.org/graph/v1/paper/search?"

params = \
"query={}&limit={}&offset={}".format(query, limit, offset)+\
"&fields=title,venue,year,referenceCount,citationCount,publicationTypes,abstract"

# search for venue, too
if venue is not None:
    params += "&venue={}".format(venue)

# Beuild the headers
API_key_header={'x-api-key': 'tLDDwfKyhy9utmxB0pPJC1GZHVBAY5Q47762sENF'}

# query the api
final_url = base_url+params
print("Final URL: "+final_url)
req = requests.get(final_url, headers=API_key_header)

#print(req.json())

# you might get 'Too Many Requests' error
if "message" in req.json().keys():
    print("\n"+req.json()["message"] )
    sys.exit()

# number of total papers
num_of_papers = req.json()['total']
print("\nTotal: {}".format(num_of_papers))
if num_of_papers==0:
    sys.exit()

data=req.json()['data']

# set up the CSV file
if save_csv:
    publications_file = open('publications.csv', mode='w')
    publications_writer = csv.DictWriter(publications_file, data[0].keys())
    publications_writer.writeheader()

for p,i in zip(data, range(limit)): 
    title = p['title']
    abstract = p['abstract']

    # filter out papers that don't have title or abstract
    if title is None or abstract is None:
        print("Filtering out because title or abstract is NULL")
        continue

    #print("\n{}. ".format(i+offset))
    #print_paper(p)
    #print("----")

    # filter out unwanted papers
    if filter is not None \
        and containes_keywords(filter, title, abstract):
        print("Filtering out because contains bad words")
        continue
    
    if include is not None \
        and not containes_keywords(include, title, abstract):
        print("Filtering out because doesn't contain good words")
        continue
    print("YEEEEEEEEEEEEEEEEEEEEEEEEe")
    
    print("\n{}. ".format(i+offset))
    print_paper(p)


    # write to the CSV file
    if save_csv: write_to_csv(publications_writer, p)

if save_csv: publications_file.close()
