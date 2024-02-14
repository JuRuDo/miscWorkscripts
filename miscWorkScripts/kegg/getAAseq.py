#!/bin/env python

from lxml import etree
from io import StringIO
import urllib3 as urllib
import argparse


def get_xml(path):
    http = urllib.PoolManager()
    html = http.request('GET', path)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(str(html.data)), parser)
    return tree


def get_orthologs(pathway):
    url = 'https://www.kegg.jp/kegg-bin/view_ortholog_table?map='
    pathway_tree = get_xml(url + pathway)
    root = pathway_tree.getroot()
    groups = {}
    groups_index = []
    for i in range(len(root[0][9][3][0][1])):
        groups[root[0][9][3][0][1][i][0].text] = []
        groups_index.append(root[0][9][3][0][1][i][0].text)
    for spec in root[0][9][3][1]:
        spec_id = spec[2][0].text
        for group in range(3, len(groups_index) + 3):
            for entry in spec[group]:
                if entry.text:
                    link = entry.values()[0].split('?')[1][:-2]
                    groups[groups_index[group - 3]].append((spec_id, entry.text, link))
    return groups


def get_aa_sequences(groups, outpath):
    url = 'https://www.kegg.jp/dbget-bin/www_bget?-f+-n+a+'
    with open(outpath, 'w') as out:
        for group in groups:
            for entry in groups[group]:
                try:
                    tree = get_xml(url + entry[2])
                    root = tree.getroot()
                    lines = root[0][9][1][1].tail.split('\\n')
                    seq = ''.join(lines[1:-1])
                    out.write('>' + group + '#' + entry[0] + '@' + entry[1] + '\n' + seq + '\n')
                except:
                    print(entry)


def main():
    parser = argparse.ArgumentParser(description="get all AA sequences of a kegg pathway")
    parser.add_argument("-i", "--pathway_id", type=str, default=None, required=True,
                        help="Id of the pathway, only give the numerical part")
    parser.add_argument("-o", "--outpath", type=str, default='./kegg_out.fasta',
                        help="outputfile (fasta format)")
    args = parser.parse_args()
    groups = get_orthologs(args.pathway_id)
    get_aa_sequences(groups, args.outpath)


if __name__ == '__main__':
    main()
