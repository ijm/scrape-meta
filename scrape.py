from argparse import ArgumentParser, FileType
from sys import stdout
import requests
from bs4 import BeautifulSoup
import json
import yaml


def doArgs():
    args = ArgumentParser(description="Scrape meta data from HTML URL into a JSON, YAML, or XML file")
    args.add_argument('-o', '--outfile', dest='ofile', type=FileType('w'),
                      default=stdout, help='output file, (defaults to stdout)')
    args.add_argument('-y', '--yaml', dest='yaml', action='store_true',
                      help="output YAML")
    args.add_argument('-x', '--xml', dest='xml', action='store_true',
                      help="output regenerated XML")
    args.add_argument('url', help="URL to scrape")

    return args.parse_args()


def scrape(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')


def extract_meta(meta_tags):
    named = {}
    graph = {}
    other = []
    for tag in meta_tags:
        if name := tag.get('name'):
            named[name] = tag.get('content', '')
        elif prop := tag.get('property'):
            graph[prop] = tag.get('content', '')
        else:
            other.append(str(tag))

    return named, graph, other


def main():
    args = doArgs()
    url = args.url

    soup = scrape(url)

    meta_tags = soup.find_all('meta')

    named, graph, other = extract_meta(meta_tags)
    meta = {
        "sourceurl": url,
        "named": named,
        "opengraph": graph,
        "other": other
    }

    if args.xml:
        root = BeautifulSoup()
        top = root.new_tag('meta_tags')
        top.extend(meta_tags)
        outstring = top.prettify()
    elif args.yaml:
        outstring = yaml.dump(meta, default_flow_style=False)
    else:
        outstring = json.dumps(meta, indent=2)

    args.ofile.write(outstring)


if __name__ == "__main__":
    main()
