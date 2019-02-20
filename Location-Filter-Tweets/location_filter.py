# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 16:36:11 2017

@author: Juan David Martínez
"""

import os
import re
import functools
import pandas as pd
from glob import glob 
import functools
from functools import reduce
import time
import datetime
import random
import recordlinkage as rl
import numpy as np
import pickle
from nltk.corpus import stopwords



#loc = pd.read_csv("diccionario_localizacion.csv", sep = ';')
loc = pd.read_csv("diccionario_localizacion_generales.csv", sep = ';')




def removeStopwords(texto):
    
    words = re.findall(r'\w+', texto) 
    
    important_words = filter(lambda x: x not in stopwords.words('spanish'), words)

    listofwords = list(important_words)
    
    loc = ' '.join(word for word in listofwords)

    return loc



def clean_loc(x):
    '''
    Esta función recibe una marca y la limpia según los lineamientos del paso 1.
    '''
    x = str(x)
    
    c_brand = x.lower()
    
    pattern = re.compile('([^\s\w]|_)+')
    
    c_brand = pattern.sub('', c_brand)

    c_brand = re.sub(r'ñ', 'n', c_brand)
    
    c_brand = re.sub(r'á', 'a', c_brand)
    
    c_brand = re.sub(r'â', 'a', c_brand)
    
    c_brand = re.sub(r'ã', 'a', c_brand)

    c_brand = re.sub(r'é', 'e', c_brand)

    c_brand = re.sub(r'í', 'i', c_brand)

    c_brand = re.sub(r'ó', 'o', c_brand)
    
    c_brand = re.sub(r'ú', 'u', c_brand)
    
    c_brand = re.sub(r'º', '', c_brand)
    
    c_brand = re.sub('\s+',' ', c_brand)
    
    c_brand = c_brand.strip()
    
    c_brand = removeStopwords(c_brand)
    
    c_brand = c_brand.strip()
    
    return c_brand



loc['loc_var'] =  loc['loc_var'].map(clean_loc)


nodes = pd.read_csv("graph_28_08_nodes.csv", sep = ';')

#variables en donde se busca la loc: label, place_country, place_fullname, place_name, description, real_name, location

loc_list = list(loc['loc_var'])

def word_loc_list(x):
    
    if x in loc_list:
        
        return True

def en_colombia(text):
    
    text = str(text)
    
    text = removeStopwords(text)
    
    text = clean_loc(text)
   
    words = re.findall(r'\w+', text) 
    
    for word in words:
        
        value = word_loc_list(word)
    
        if value == True:
            
            return True
    

nodes_filtered = nodes

nodes_filtered['en_colombia--location'] = nodes_filtered['location'].map(en_colombia)
nodes_filtered['en_colombia--description'] = nodes_filtered['description'].map(en_colombia)
nodes_filtered['en_colombia--placecountry'] = nodes_filtered['place_country'].map(en_colombia)
nodes_filtered['en_colombia--place_fullname'] = nodes_filtered['place_fullname'].map(en_colombia)
nodes_filtered['en_colombia--place_name'] = nodes_filtered['place_name'].map(en_colombia)
nodes_filtered['en_colombia--real_name'] = nodes_filtered['real_name'].map(en_colombia)
nodes_filtered['en_colombia--label'] = nodes_filtered['label'].map(en_colombia)


nodes_filtered.to_csv("nodes_30082017_filtered_loc.csv", sep = ';')
