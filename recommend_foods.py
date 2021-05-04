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

food_freq = {} # Food Classifier에서 분류 결과로서 생성한 dictionory라고 가정함
food_freq['닭갈비'] = 6
food_freq['오일파스타'] = 4
food_freq['김밥'] = 2
food_freq['된장찌개'] = 1
food_freq['쌀국수'] = 1 # '씰국수'는 menu2vec에 포함되어있지 않음!

food_sim = {} # food_freq의 각 food당 유사한 음식들의 목록
for food in food_freq:
  if food not in menu2vec.index_to_key:
    food_sim[food] = []
  else:
    food_sim[food] = menu2vec.most_similar(positive=[food], topn=20)

for menu, sim in food_sim.items():
  print(menu, end=' -> ')
  print(sim)
