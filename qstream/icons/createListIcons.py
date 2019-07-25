# -*- coding: utf-8 -*-
"""
Created on Mon May 13 11:06:01 2019

@author: aurelien.clairais
"""

import os

output = open("IconList.txt", "w")

for file in os.listdir("."):
    if file.endswith(".png"):
        output.write("<file>icons/" + file + "</file>\n")
        
output.close()
        
