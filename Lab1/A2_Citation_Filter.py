import argparse
import csv
import os
import re
import time
from datetime import date, datetime
from typing import Dict, Tuple, Union

from lxml import etree
from tqdm import tqdm

class InvalidElementName(Exception):
    def __init__(self, invalid_element_name, tag_name, parent_name):
        self.invalid_element_name = invalid_element_name
        self.tag_name = tag_name
        self.parent_name = parent_name

    def __str__(self):
        return 'Invalid name %s found in tag %s within element %s' % (repr(self.invalid_element_name),
                                                                      repr(self.tag_name),
                                                                      repr(self.parent_name))

def get_element_attributes(xml_file, elements: set) -> dict:
    context = etree.iterparse(xml_file, dtd_validation=True, events=('start', 'end'), attribute_defaults=True,
                              load_dtd=True)
    # turn it into an iterator
    context = iter(context)
    # get the root element
    event, root = next(context)
    data = dict()
    for element in elements:
        data[element] = set()
    current_tag = None
    for event, elem in context:
        if current_tag is None and event == 'start' and elem.tag in elements:
            current_tag = elem.tag
            keys = elem.keys()
            if len(keys) > 0:
                keys = set(keys)
                attributes = data[current_tag]
                attributes.update(keys)
        elif current_tag is not None and event == 'end':
            if elem.tag == current_tag:
                current_tag = None
            elif elem.tag is not None and elem.text is not None:
                if elem.tag == 'id':
                    raise InvalidElementName('id', elem.tag, current_tag)
                attributes = data[current_tag]
                attributes.add(elem.tag)
                keys = elem.keys()
                if len(keys) > 0:
                    for key in keys:
                        attributes.add('%s-%s' % (elem.tag, key))
            root.clear()
    for element in elements:
        attributes = data[element]
        if len(attributes) == 0:
            data.pop(element)
        elif 'id' in attributes:
            raise InvalidElementName('id', element, 'root')
    return data

def get_elements(dtd_file) -> set:
    dtd = etree.DTD(dtd_file)
    elements = set()
    for el in dtd.iterelements():
        if el.type == 'element':
            elements.add(el.name)
    elements.remove('dblp')
    return elements

with open('dblp.dtd', mode='rb') as dtd_file:
    print('Reading elements from DTD file...')
    elements = get_elements(dtd_file)

xml_file = 'dblp.xml'
tag_stack = []
elem_stack = []
attrib_stack = []
key2cites = {}

cite_name = "cite_file.txt"

import os
if os.path.exists(cite_name):
  os.remove(cite_name)
else:
  print("The file does not exist")

cite_file = open("cite_file.txt", "a+")
index = 0
for event, elem in tqdm(etree.iterparse(xml_file, dtd_validation=True, events=('start', 'end'))):

    if (index+1)%1000000 == 0:
        print(index+1)
    key = ""
    cites = []
    if event == 'start':
        tag_stack.append(elem.tag)
        elem_stack.append(elem)
        attrib_stack.append(elem.attrib)
    elif event == 'end':
        index += 1
        # print(tag_stack, elem_stack, attrib_stack)
        if attrib_stack:
            for attrib in attrib_stack:
                if attrib and 'key' in attrib:
                    key = attrib['key']
        if elem_stack[-1].tag == "cite":
            cites.append(elem_stack[-1].text)
        try:
            tag_stack.pop()
            elem_stack.pop()
            attrib_stack.pop()
        except IndexError:
            pass
    if key and cites:
        for cite in cites:
            if cite != "...":
                cite_file.write(key+","+cite+"\n")
                cite_file.close()
                cite_file = open("cite_file.txt", "a+")
cite_file.close()



cite_file = open("cite_file.txt","r")
keys = []
values = []
for line in cite_file.readlines():
    key,value = line.split(",")
    keys.append(key)
    values.append(value)
print(len(set(keys)),len(set(values)),len(set(keys+values)))

keys_set = list(set(keys+values))

import pandas as pd
df = pd.read_csv("output_/output_article_bk.csv", delimiter=";")
filtered_df = df[df['key'].isin(keys_set)]
print(filtered_df)
filtered_df.to_csv("output_/output_article.csv",index=False,sep=";")

import pandas as pd
df = pd.read_csv("output_/output_book_bk.csv", delimiter=";")
filtered_df = df[df['key'].isin(keys_set)]
print(filtered_df)
filtered_df.to_csv("output_/output_book.csv",sep=";")

import pandas as pd
df = pd.read_csv("output_/output_incollection_bk.csv", delimiter=";")
filtered_df = df[df['key'].isin(keys_set)]
print(filtered_df)
filtered_df.to_csv("output_/output_incollection.csv",sep=";")

import pandas as pd
df = pd.read_csv("output_/output_mastersthesis_bk.csv", delimiter=";")
filtered_df = df[df['key'].isin(keys_set)]
print(filtered_df)
filtered_df.to_csv("output_/output_mastersthesis.csv",sep=";")

import pandas as pd
df = pd.read_csv("output_/output_phdthesis_bk.csv", delimiter=";")
filtered_df = df[df['key'].isin(keys_set)]
print(filtered_df)
filtered_df.to_csv("output_/output_phdthesis.csv",sep=";")

import pandas as pd
df = pd.read_csv("output_/output_proceedings_bk.csv", delimiter=";")
filtered_df = df[df['key'].isin(keys_set)]
print(filtered_df)
filtered_df.to_csv("output_/output_proceedings.csv",sep=";")

import pandas as pd
df = pd.read_csv("output_/output_inproceedings_bk.csv", delimiter=";")
filtered_df = df[df['key'].isin(keys_set)]
print(filtered_df)
filtered_df.to_csv("output_/output_inproceedings.csv",sep=";")