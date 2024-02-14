#!/bin/env python

import coreapi
import argparse


def getomagroup(groupid, outpath, client, schema):
        action = ["group", "read"]
        params = {"group_id": groupid,}
        out = open(outpath + '/' + groupid + '.fasta', 'w')
        result = client.action(schema, action, params=params)
        for i in result['members']:
            out.write('>' + i['omaid'] + '\n')
            action = ["protein", "read"]
            params = {"entry_id": i['omaid'],}
            prot = client.action(schema, action, params=params)
            out.write(prot['sequence'] + '\n')


# Initialize a client & load the schema document
def main():
    parser = argparse.ArgumentParser(description="Use OMA api to download OMA groups by their id")
    parser.add_argument("-i", "--ids", type=str, nargs='+', default=None, required=True,
                          help="group ids, needs at least one, multiple divided by spaces")
    parser.add_argument("-o", "--outpath", type=str, default='.',
                          help="folder where fasta files will be written, all fasta file will be named after their "
                               "group id")
    args = parser.parse_args()
    client = coreapi.Client()
    schema = client.get("https://omabrowser.org/api/docs")
    for groupid in args.ids:
        print('Getting: ' + groupid)
        getomagroup(groupid, args.outpath, client, schema)
    print('done!')


if __name__ == '__main__':
    main()

