# Semantic-Scholar-Querier

```
$ python3 semantic_scholar_survey.py -h
usage: semantic_scholar_survey.py [-h] [-q QUERY] [-v VENUE] [-l LIMIT] [-o OFFSET] [-f FILTER] [-i INCLUDE] [--save-csv]

Semantic Scholar Querier

options:
  -h, --help            show this help message and exit
  -q QUERY, --query QUERY
                        Search keywords
  -v VENUE, --venue VENUE
                        Venue name ('j acm', 'icnc', 'ace', 'nossdav', 'cig', 'infocom'...)
  -l LIMIT, --limit LIMIT
                        Number of publications to show (<=100). Default: 10
  -o OFFSET, --offset OFFSET
                        Show publications starting from given ID. Default: 0
  -f FILTER, --filter FILTER
                        Filter out publications that include keyword in the title
  -i INCLUDE, --include INCLUDE
                        Keep only the publications that include keywords in the title or abstract
  --save-csv            Save output in a CSV file
```
