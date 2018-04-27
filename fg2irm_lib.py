#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# fg2irm_lib
# 2018 Aun "Skippern" Johnsen <skippern@gimnechiske.org
#
# Converts from Fantasy Grounds formats to irm_lib data
#
import argparse
import os
import json
from lxml import etree

parser = argparse.ArgumentParser(description='Convert from an FG xml to irm_lib')
parser.add_argument('--xml', metavar='FGXML', type=str,
                    help='FG XML File', required=True)
parser.add_argument('--data', metavar='DATADIR', type=str,
                    help='irm_lib data dir', required=True)
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('-vv', '--debug', action='store_true')
parser.add_argument('-s', '--silent', action='store_true')
args = parser.parse_args()

__OUTPUT = 1
if (args.debug):
    __OUTPUT = 3
elif (args.verbose):
    __OUTPUT = 2
elif (args.silent):
    __OUTPUT = 0

def printf(text, level=1):
    if (__OUTPUT >= level):
        print text

printf('__OUTPUT {0}'.format(__OUTPUT), 3)

printf('--data {0}'.format(args.data), 3)
printf('--xml {0}'.format(args.xml), 3)

__DATA = args.data
root = etree.parse(args.xml)

__dirname = __DATA + 'tables'
try:
    os.stat(__dirname)
except:
    os.mkdir(__dirname)
__dirname = __DATA + 'skills'
try:
    os.stat(__dirname)
except:
    os.mkdir(__dirname)
__dirname = __DATA + 'races'
try:
    os.stat(__dirname)
except:
    os.mkdir(__dirname)
__dirname = __DATA + 'professions'
try:
    os.stat(__dirname)
except:
    os.mkdir(__dirname)
__dirname = __DATA + 'trainingpackages'
try:
    os.stat(__dirname)
except:
    os.mkdir(__dirname)
__dirname = __DATA + 'spells'
try:
    os.stat(__dirname)
except:
    os.mkdir(__dirname)
__dirname = __DATA + 'talents'
try:
    os.stat(__dirname)
except:
    os.mkdir(__dirname)
__dirname = __DATA + 'flaws'
try:
    os.stat(__dirname)
except:
    os.mkdir(__dirname)

__tables = root.find("Tables")

for table in __tables:
    printf(etree.tostring(table), 0)
    printf(table.tag)
    __filename = __DATA + 'tables/' + table.tag + '.json'

    __table_data = {}
    __table_data['id'] = table.find("Id").text
    __table_data['name'] = table.find("Name").text
    __table_data['type'] = table.find("TableType").text
    __table_data['class'] = table.find("Class").text
    __table_data['sort'] = table.find("SortOrder").text



    __table_data['xml'] = etree.tostring(table)

    f = open(__filename, 'wb')
    f.write(json.dumps( __table_data , indent=3))
    f.close()

    ## We now have extracted tables from the XML and are ready to create a matrix of values

