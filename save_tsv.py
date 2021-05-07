import random

import gensim.models
from gensim.models import FastText
from gensim.models import KeyedVectors
import csv
import os
import numpy as np

import recipe_embedding.menu_embedding
from recipe_embedding import menu_embedding


wv_ingredient_loaded = KeyedVectors.load('./recipe_embedding/_model_ingredient_wv')  # wv 로드
menu2vec_wv = menu_embedding.load_menu2vec()

fo = open('./tsv_files/menu2vec.tsv', 'w', encoding='utf-8', newline='')
wtr = csv.writer(fo, delimiter='\t')
for food in menu2vec_wv.index_to_key:
  wtr.writerow(menu2vec_wv[food])
fo.close()

fo = open('./tsv_files/menu2vec_meta.tsv', 'w', encoding='utf-8', newline='')
wtr = csv.writer(fo, delimiter='\t')
for i, food in enumerate(menu2vec_wv.index_to_key):
  wtr.writerow([food])
fo.close()

fo = open('./tsv_files/ingre2vec.tsv', 'w', encoding='utf-8', newline='')
wtr = csv.writer(fo, delimiter='\t')
for food in wv_ingredient_loaded.index_to_key:
  wtr.writerow(wv_ingredient_loaded[food])
fo.close()

fo = open('./tsv_files/ingre2vec_meta.tsv', 'w', encoding='utf-8', newline='')
wtr = csv.writer(fo, delimiter='\t')
for food in wv_ingredient_loaded.index_to_key:
  wtr.writerow([food])
fo.close()