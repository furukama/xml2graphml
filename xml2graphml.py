#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from BeautifulSoup import BeautifulStoneSoup as BSS
import codecs

try:
    filename = sys.argv[1]
    output = sys.argv[2]
except IndexError:
    print "Usage: xml2graphml.py <Input> <Output>"
    sys.exit(2)

print "Reading " + filename
file = open(filename)
xml = file.read()
file.close()

print "Parsing data"

nodes = []
frequency = {}

soup = BSS(xml)

for node in soup.findAll("node"):
    nodes.append(node['id'])
    frequency[node['id']] = node.findAll(id="frequency")[0]['value']

f = codecs.open(output, encoding='utf-8', mode='w+')

f.write('<?xml version="1.0" encoding="UTF-8"?><graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd"><graph id="G" edgedefault="directed"><key id="label" for="node" attr.name="label" attr.type="string"/><key id="frequency" for="node" attr.name="frequency" attr.type="double"/><key id="weight" for="edge" attr.name="weight" attr.type="double"/>')

print "Writing nodes"

for node in nodes:
    f.write('<node id="' + str(nodes.index(node)) + '"><data key="label">' + node + '</data><data key="frequency">' + frequency[node] + '</data></node>')

print "Writing edges"

for edge in soup.findAll("link"):
    f.write('<edge source="' + str(nodes.index(edge["source"])) + '" target="' + str(nodes.index(edge["target"])) + '">')

    try:
        f.write('<data key="weight">' + str(edge["value"]) + '</data>')
    except KeyError:
        f.write('<data key="weight">1.0</data>')

    f.write('</edge>')

f.write('</graph></graphml>')

f.close()
