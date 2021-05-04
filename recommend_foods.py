import gensim.models
from gensim.models import FastText
from gensim.models import KeyedVectors
import csv
import os
import numpy as np

from recipe_embedding import menu_embedding

model_ingredient_loaded = FastText.load('./recipe_embedding/_model_ingredient') #모델 로드
wv_ingredient_loaded = KeyedVectors.load('./recipe_embedding/_model_ingredient_wv') #wv 로드

menu2vec = menu_embedding.get_menu2vec(wv_ingredient_loaded)
print(menu2vec.index_to_key) # menu2vec에 포함된 memu 목록


