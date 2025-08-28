#!/usr/bin/env python3

"""
StrUsageXML2XLS.py

A script to convert Structure Usage Reports from XML to XLS format.

input : StrUsageReport.xml - XML file - PLSCADD report save all as XML
output: XLS file with each table in a separate sheet
"""

import xml.etree.ElementTree as ET
tree = ET.parse('StrUsageReport.xml')
root = tree.getroot()

"""
possibly will use pandas to import from xml directly without ET
"""
