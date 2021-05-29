import gensim.models
from gensim.models import FastText
from gensim.models import KeyedVectors
import csv
import os
import numpy as np

# import local files
from recipe_embedding import menu_embedding
import KakaoLocalApi

def dict_to_numpy (dict):
  np_array = np.array(list(dict.values()))
  print(dict)
  print(np_array)
  return np_array

def softmax_sum_n (np_array, sum = 10):
  exp_a = np.exp(np_array)
  exp_sum = np.sum(exp_a)
  res = exp_a / exp_sum
  print("original array: {}".format(np_array))
  print("exp(org array): {}".format(exp_a))
  print("sigmoid sum_n : {}".format(res*10))
  return res

# food_pref_dic의 각 key에 대해서 유사메뉴리스트 얻기
def get_food_sim (menu2vec, food_pref_dic, topn=10):
  food_sim = {}  # food_freq의 각 food당 유사한 음식들의 목록
  for food in food_pref_dic:
    if food not in menu2vec.index_to_key:
      food_sim[food] = []
    else:
      food_sim[food] = menu2vec.most_similar(positive=[food], topn=topn)

  for menu, sim in food_sim.items():
    print(menu, end=' -> ')
    print(sim)
  print('\n')

  return food_sim

# 최종 추천 리스트 생성
def get_food_recommend (food_pref_dic, food_sim, size=10):
  food_recommend = []  # 추천할 음식 list (각 음식 당 최대 freq개 만큼, similarity>0.90인 음식 선택)
  freq_sum = 0  # food_pref_dic의 freq 총합 (menu2vec에 없는 menu 제외)
  for food, freq in food_pref_dic.items():
    if len(food_sim[food]) != 0:
      freq_sum += freq
  food_pref_dic_mod = {} # freq 총합이 size에 가까워지도록 조정 (menu2vec에 없는 menu 제외)
  for food, freq in food_pref_dic.items():
    if len(food_sim[food]) != 0:
      food_pref_dic_mod[food] = round((freq / freq_sum) * size)
  print("modified food_pref_dict: {}".format(food_pref_dic_mod))

  for food, freq in food_pref_dic_mod.items():
    for i, food_sim_tuple in enumerate(food_sim.get(food)):
      if i >= freq:
        break
      elif food_sim_tuple[1] > 0.90:
        food_recommend.append(food_sim_tuple[0])

  print("food_recommend: {}".format(food_recommend))
  return food_recommend

# food_recommend의 각 food에 대해 Kakao local Api에 query를 한 결과
def KakaoLocalQuery (food_recommend, size = 10):
  food_rec_json_object = {}  # food_recommend의 각 food에 대해 KakaoLocalAPI에 검색한 음식점 정보 Dictionary
  rest_api_key = "8edafea22605fecd679938e8880fa6ee"
  for food in food_recommend:
    food_rec_json_object[food] = KakaoLocalApi.local_api_keyword(rest_api_key=rest_api_key, keyword=food, size=size)
  return food_rec_json_object


# Food Classifier에서 분류 결과로서 생성한 dictionory라고 가정함 (food_preference_dictionary)
food_freq = {}
food_freq['닭갈비'] = 6
food_freq['오일파스타'] = 8
food_freq['김밥'] = 3
food_freq['된장찌개'] = 5
food_freq['쌀국수'] = 2 # '씰국수'는 menu2vec에 포함되어있지 않음!


menu2vec = menu_embedding.load_menu2vec(filepath='./recipe_embedding/', filename='_menu2vec_wv')
print(menu2vec.index_to_key) # menu2vec에 포함된 memu 목록

food_freq = dict(sorted(food_freq.items(), key=(lambda x: x[1]), reverse=True)) # food_pref_dict를 정렬
print("food_preference_dict: {}".format(food_freq))

food_sim = get_food_sim(menu2vec, food_freq, 10)  # 각 key값에 대해 유사메뉴 리스트 생성
food_recommend = get_food_recommend(food_freq, food_sim, size=10) # 최종 추천 리스트 생성

food_rec_query_result = KakaoLocalQuery(food_recommend, size=10) # 최종 추천리스트에 해당하는 음식점 검색

for food in food_recommend:
  print("[{}]".format(food), end=' ')
  print("Total_count: {}".format(food_rec_query_result[food]['meta']['total_count'])) # 각 food당 총 검색된 음식점 수
  for i in range(len(food_rec_query_result[food]['documents'])): # 검색된 음식점 중 현재 page내의 정보 모두 출력
    print(food_rec_query_result[food]['documents'][i])


