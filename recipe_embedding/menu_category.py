import gensim.models
from gensim.models import FastText
from gensim.models import KeyedVectors
import csv
import os
import numpy as np
import random
import menu_embedding

category = {}
folders = os.listdir('./recipe_data')
print(folders)
menu_count = 0
for folder in folders:
  category[folder] = [food_name[7:len(food_name)-4] for food_name in os.listdir('./recipe_data/'+folder)]
  folder_count = len(os.listdir('./recipe_data/'+folder))
  menu_count = menu_count + folder_count
  print("[{}개] {}->{}".format(folder_count, folder, category[folder]))
print("the number of menu: {}".format(menu_count))
print("\n\n")


menu2vec = menu_embedding.load_menu2vec()

def get_random_index(count, min, max):
  random_index = []
  while len(random_index) < count:
    rannum = random.randint(min, max)
    if rannum not in random_index:
      random_index.append(rannum)
  # print("random index: {}".format(random_index))
  return random_index

def get_random_food(foods, count):
  random_index = get_random_index(count, 0, len(foods)-1)
  random_set = []
  for index in random_index:
    random_set.append(foods[index])
  return random_set

#전체에서 랜덤한 메뉴 선택
random_index = get_random_index(10, 0, len(menu2vec)-1)
set_food_ran = []
for index in random_index:
  set_food_ran.append(menu2vec.index_to_key[index])

#여러 카테고리의 메뉴 합집합
set_food_union = category['밥_죽_떡'] + category['국_탕'] + category['찌개']
set_food_union = list(set(set_food_union))

#모든 메뉴 합집합
set_food_all = []
for foods in category.values():
  set_food_all = set_food_all + foods
set_food_all = list(set(set_food_all))

#임의의 집합
set_noodle = ['국수','김치비빔국수', '냉면', '라면', '바지락칼국수', '볶음라면', '볶음우동', '비빔국수', '비빔면',
              '열무비빔국수', '우동', '잔치국수', '짜장면', '짬뽕', '쫄면', '칼국수', '콩국수']
set_pasta = ['까르보나라', '스파게티', '알리오올리오', '오일파스타', '크림스파게티', '토마토스파게티', '토마토파스타', '크림파스타']
set_chicken = ['닭개장', '닭곰탕', '닭볶음탕', '삼계탕', '닭갈비', '찜닭', '치킨', '닭가슴살스테이크']
set_seafood = ['꽃게탕', '미역국', '북어국', '오징어무국', '홍합탕', '갈치조림', '고등어조림', '골뱅이무침', '낙지볶음', '오징어볶음',
               '주꾸미볶음', '코다리조림', '바지락칼국수', '새우볶음밥', '초밥', '생선까스', '연어스테이크', '동태찌개', '바지락순두부찌개',
               '오징어찌개', '우렁된장찌개']
set_meat = ['갈비탕', '감자탕', '소고기무국', '소고기미역국', '육개장', '갈비찜', '돈까스', '돼지갈비찜', '떡갈비', '불고기', '소갈비찜',
            '소불고기', '수육', '제육볶음', '탕수육', '버거', '등심스테이크', '스테이크','안심스테이크', '찹스테이크', '함박스테이크',
            '돼지고기고추장찌개', '돼지고기김치찌개', '부대찌개', '차돌박이된장찌개']
set_chinese = ['마파두부', '탕수육', '짜장면', '짬뽕', '계란볶음밥', '볶음밥', '짜장밥']
set_japanese = ['밀푀유나베', '돈까스', '볶음우동', '우동', '유부초밥', '주먹밥', '초밥', '카레라이스']
set_dumpling = ['수제비', '비빔만두', '만두']


set_food = set_meat
set_food = list(set(set_food))
print(set_food)
print("num of menu: {}".format(len(set_food)))

set_similarity = [] #집합 내의 서로다른 두 메뉴의 유사도 값들을 저장한 리스트
for food_A in set_food:
  for food_B in set_food:
    if food_A != food_B:
      set_similarity.append(menu2vec.similarity(food_A, food_B))
set_sim_avg = 0 # set_similarity의 평균값
for elem in set_similarity:
  set_sim_avg = set_sim_avg + elem
set_sim_avg = set_sim_avg / len(set_similarity)
print("Average of similarities: {}".format(set_sim_avg))


diff_set_similarity = [] #서로다른 두 집합의 메뉴의 유사도 값들을 저장한 리스트
set_food_A = set_noodle
set_food_B = set_meat
for food_A in set_food_A:
  for food_B in set_food_B:
    if food_A != food_B:
      diff_set_similarity.append(menu2vec.similarity(food_A, food_B))
diff_set_sim_avg = 0 # diff_set_similarity의 평균값
for elem in diff_set_similarity:
  diff_set_sim_avg = diff_set_sim_avg + elem
diff_set_sim_avg = diff_set_sim_avg / len(diff_set_similarity)
print("Average of similarities: {}".format(diff_set_sim_avg))