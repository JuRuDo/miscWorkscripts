#!/bin/env python

#######################################################################
# Copyright (C) 2022 Julian Dosch
#
# This file is part of .
#
#  SpICE is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SpICE is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with expNet.  If not, see <http://www.gnu.org/licenses/>.
#
#######################################################################



import argparse
from pkg_resources import get_distribution
import xml.etree.ElementTree as ET


def read_xml(path, outpath):
    with open(outpath, 'w') as out:
        tree = ET.parse(path)
        root = tree.getroot()
        for child in root:
            if child.tag == '{http://www.ncbi.nlm.nih.gov/geo/info/MINiML}Sample':
                out.write(child.attrib['iid'])
                x = 0
                tmp = {'lms from initial subtype discovery': '', 'lms from random forest prediction model': ''}
                for child2 in child:
                    if child2.tag == '{http://www.ncbi.nlm.nih.gov/geo/info/MINiML}Channel':
                        for child3 in child2:
                            if child3.tag == '{http://www.ncbi.nlm.nih.gov/geo/info/MINiML}Characteristics':
                                if child3.attrib['tag'] == 'lms from initial subtype discovery':
                                    tmp['lms from initial subtype discovery'] = child3.text.strip(' ').strip('\n')
                                elif child3.attrib['tag'] == 'lms from random forest prediction model':
                                    tmp['lms from random forest prediction model'] = child3.text.strip(' ').strip('\n')
                out.write('\t' + tmp['lms from initial subtype discovery'] + '\t' + tmp['lms from random forest prediction model'] + '\n')
    out.close()


def main():
    version = get_distribution('workScripts').version
    parser = argparse.ArgumentParser(description='checks a list of genes for DGE in a file with multiple clusters',
                                     epilog="")
    required = parser.add_argument_group('required arguments')
    parser.add_argument('--version', action='version', version=str(version))
    required.add_argument("-x", "--xml", default=None, type=str, required=True,
                          help="path to the xml file")
    required.add_argument("-o", "--outpath", default=None, type=str, required=True,
                          help="path to output file")
    args = parser.parse_args()

    read_xml(args.xml, args.outpath)

if __name__ == '__main__':
    main()
