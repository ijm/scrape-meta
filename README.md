# scrape-meta

A Python script to scrape HTML meta tags from a URL and output them in a human-readable JSON or YAML file.

```
% python scrape.py -help
usage: scrape.py [-h] [-o OFILE] [-y] [-x] url

Scrape meta data from HTML URL into a JSON, YAML, or XML file

positional arguments:
  url                   URL to scrape

options:
  -h, --help            show this help message and exit
  -o OFILE, --outfile OFILE
                        output file, (defaults to stdout)
  -y, --yaml            output YAML
  -x, --xml             output regenerated XML
```
