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
    parser.add_argument("-o", "--offset", type=int, default=0, help="Show publications starting from given ID. Default: 0")
    parser.add_argument("-f", "--filter", action='append', help="Filter out publications that include keyword in the title")
    parser.add_argument("-i", "--include", action='append', help="Keep only the publications that include keywords in the title or abstract")
    parser.add_argument("--save-csv", action="store_true", help="Save output in a CSV file")
    args = parser.parse_args()
    #print(args)
    return args.query, args.venue, args.limit, args.offset, args.filter, args.include, args.save_csv

def contains_filtered_keyword(filters, title):
    for f in filters:
        if f.lower() in title.lower():
            return True
    return False

def containes_necessary_words(necessary_keywords, title, abstract):
    for nk in necessary_keywords:
        if nk.lower() in title.lower() or nk.lower() in abstract.lower():
            return True
    return False

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
API_key_header={'x-api-key': ''} # ENTER API KEY HERE (OPTIONAL)

# query the api
final_url = base_url+params
print("Final URL: "+final_url)
req = requests.get(final_url, headers=API_key_header)

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
        continue

    # filter out unwanted papers
    if filter is not None \
        and contains_filtered_keyword(filter, title):
        continue
    
    if include is not None \
        and not containes_necessary_words(include, title, abstract):
        continue

    print("\n{}. ".format(i+offset))
    print_paper(p)
    
    # write to the CSV file
    if save_csv: write_to_csv(publications_writer, p)

if save_csv: publications_file.close()
