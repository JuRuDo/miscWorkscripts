#!/bin/env python


import argparse


def main():
    parser = argparse.ArgumentParser(description="Processes sce data from a h5ad file, needs a Patient and Type obs "
                                                 "column")
    parser.add_argument("-i", "--input", type=str, default=None, required=True,
                          help="input data as h5ad file.")
    parser.add_argument("-n", "--addName", action="store_true",
                        help="add gene names as a third column.")
    parser.add_argument("-v", "--omitVersion", action="store_false",
                        help="omit version numbers for transcript and gene id.")
    parser.add_argument("-o", "--output", type=str, default=None, required=True,
                          help="Output file.")
    args = parser.parse_args()

    ttable = create_transcript_list(args.input, args.addName, args.omitVersion)
    print_output(args.output, ttable, args.addName)



def create_transcript_list(infile, use_name, use_version):
    gtf = open(infile, 'r')
    r = {}
    for line in gtf:
        if len(line) == 0 or line[0] == '#':
            continue
        l = line.strip().split('\t')
        if l[2] == 'transcript':
            info = l[8]
            d = {}
            for x in info.split('; '):
                x = x.strip()
                p = x.find(' ')
                if p == -1:
                    continue
                k = x[:p]
                p = x.find('"',p)
                p2 = x.find('"',p+1)
                v = x[p+1:p2]
                d[k] = v


            if 'transcript_id' not in d or 'gene_id' not in d:
                continue

            tid = d['transcript_id']
            gid = d['gene_id']
            if use_version:
                if 'transcript_version' not in d or 'gene_version' not in d:
                    continue

                tid += '.' + d['transcript_version']
                gid += '.' + d['gene_version']
            gname = None
            if use_name:
                if 'gene_name' not in d:
                    continue
                gname = d['gene_name']

            if tid in r:
                continue

            r[tid] = (gid, gname)
    gtf.close()
    return r



def print_output(output, ttable, use_name):
    with open(output, 'w') as out:
        for tid in ttable:
            if use_name:
                out.write("%s\t%s\t%s\n"%(tid, ttable[tid][0], ttable[tid][1]))
            else:
                out.write("%s\t%s\n"%(tid, ttable[tid][0]))
    out.close()

if __name__ == '__main__':
    main()
