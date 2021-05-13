import gensim.models
from gensim.models import FastText
from gensim.models import KeyedVectors
import csv
import os
import numpy as np

# import local files
from recipe_embedding import menu_embedding
import KakaoLocalApi


if '_menu2vec_wv' not in os.listdir('./recipe_embedding/'):
  wv_ingredient_loaded = KeyedVectors.load('./recipe_embedding/_model_ingredient_wv')  # wv 로드
  menu2vec = menu_embedding.get_menu2vec(wv_ingredient_loaded)
  menu_embedding.save_menu2vec(menu2vec)
menu2vec = menu_embedding.load_menu2vec()
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
    food_sim[food] = menu2vec.most_similar(positive=[food], topn=10)

for menu, sim in food_sim.items():
  print(menu, end=' -> ')
  print(sim)
print('\n')

food_recommend = [] # 추천할 음식 list (각 food의 유사음식 list 에서, 최대 freq개 만큼, similarity>0.90인 음식 선택)
for food, freq in food_freq.items():
  for i, food_sim_tuple in enumerate(food_sim.get(food)):
    if i >= freq:
      break
    elif food_sim_tuple[1] > 0.90:
      food_recommend.append(food_sim_tuple[0])

print(food_recommend)

food_rec_json_object = {} # food_recommend의 각 food에 대해 KakaoLocalAPI에 검색한 음식점 정보 Dictionary
rest_api_key = "8edafea22605fecd679938e8880fa6ee"
for food in food_recommend:
  food_rec_json_object[food] = KakaoLocalApi.local_api_keyword(rest_api_key=rest_api_key, keyword=food, size=10)

for food in food_recommend:
  print("[{}]".format(food), end=' ')
  print("Total_count: {}".format(food_rec_json_object[food]['meta']['total_count'])) # 각 food당 총 검색된 음식점 수
  for i in range(len(food_rec_json_object[food]['documents'])): # 검색된 음식점 중 현재 page내의 정보 모두 출력
    print(food_rec_json_object[food]['documents'][i])

"""
food_freq_2 = {}
for i, food in enumerate(menu2vec.index_to_key):
  if i >= 50:
    break
  food_freq_2[food] = 1

food_sim_2 = {} # food_freq의 각 food당 유사한 음식들의 목록
for food in food_freq_2:
  if food not in menu2vec.index_to_key:
    food_sim_2[food] = []
  else:
    food_sim_2[food] = menu2vec.most_similar(positive=[food], topn=10)

for menu, sim in food_sim_2.items():
  print(menu, end=' -> ')
  print(sim)
print('\n')
"""

