import urllib.parse
import urllib.request
import argparse


def rest_api(query, id1, id2):
    url = 'https://www.uniprot.org/uploadlists/'

    params = {
    'from': id1,
    'to': id2,
    'format': 'tab',
    'query': query
    }

    data = urllib.parse.urlencode(params)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data)
    with urllib.request.urlopen(req) as f:
       response = f.read()
    print(response.decode('utf-8'))


def read_query(path, column, skip):
    query = ''
    check = []
    with open(path, 'r') as infile:
        for i in range(skip+1):
            line = infile.readline()
        while line:
            cells = line.rstrip('\n').split('\t')
            if not cells[column] in check:
                query = query + cells[column] + ' '
                check.append(cells[column])
            line = infile.readline()
    return query


def main():
    parser = argparse.ArgumentParser(description="Uses Uniprot REST api to map ids")
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')
    required.add_argument("-i", "--input", type=str, default=None, required=True,
                          help="Path to input file, needs to be in tsv format")
    required.add_argument("-f", "--id1", type=str, default=None, required=True,
                          help="id to convert, https://www.uniprot.org/help/api_idmapping")
    required.add_argument("-t", "--id2", type=str, default=None, required=True,
                          help="output id, https://www.uniprot.org/help/api_idmapping")
    optional.add_argument("-l", "--ignore_lines", type=int, default=0,
                          help="skip the first n lines (for example headers)")
    optional.add_argument("-c", "--column", type=int, default=0,
                          help="column that contains the ids")
    args = parser.parse_args()
    query = read_query(args.input, args.column, args.ignore_lines)
    rest_api(query, args.id1, args.id2)


if __name__ == '__main__':
    main()