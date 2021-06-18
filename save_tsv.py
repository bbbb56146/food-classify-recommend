import random

import gensim.models
from gensim.models import FastText
from gensim.models import KeyedVectors
import csv
import os
import numpy as np

import recipe_embedding.menu_embedding
from recipe_embedding import menu_embedding

# <기본 분류>
category = {}
folders = os.listdir('./recipe_data')
print(folders)
menu_count = 0
for folder in folders:
  category[folder] = [food_name[7:len(food_name)-4] for food_name in os.listdir('./recipe_data/'+folder)]
  folder_count = len(os.listdir('./recipe_data/'+folder))
  menu_count = menu_count + folder_count
  print("[{}개] {}->{}".format(folder_count, folder, category[folder]))
print("\n")

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

wv_ingredient_loaded = KeyedVectors.load('./recipe_embedding/_model_ingredient_wv')  # wv 로드
menu2vec_wv = menu_embedding.load_menu2vec()

fo = open('./tsv_files/menu2vec.tsv', 'w', encoding='utf-8', newline='')
wtr = csv.writer(fo, delimiter='\t')
for food in menu2vec_wv.index_to_key:
  wtr.writerow(menu2vec_wv[food])
fo.close()

fo = open('./tsv_files/menu2vec_meta.tsv', 'w', encoding='utf-8', newline='')
wtr = csv.writer(fo, delimiter='\t')
wtr.writerow(['menu', 'category', 'sub_category','main_ingredient', 'origin'])
for i, food in enumerate(menu2vec_wv.index_to_key):
  str_category = 'null'
  str_subcategory = 'null'
  str_main_ingre = 'null'
  str_origin = 'null'
  if food in category['국_탕']:
    str_category = '국_탕'
  elif food in category['메인반찬']:
    str_category = '메인반찬'
  elif food in category['면_만두']:
    str_category = '면_만두'
  elif food in category['밥_죽_떡']:
    str_category = '밥_죽_떡'
  elif food in category['빵']:
    str_category = '빵'
  elif food in category['양식']:
    str_category = '양식'
  elif food in category['찌개']:
    str_category = '찌개'
  if food in set_noodle:
    str_subcategory = '국수류'
  if food in set_pasta:
    str_subcategory = '파스타'
  if food in set_meat:
    str_main_ingre = '육류'
  elif food in set_seafood:
    str_main_ingre = '해산물'
  elif food in set_chicken:
    str_main_ingre = '닭고기'
  if food in set_japanese:
    str_origin = '일식'
  elif food in set_chinese:
    str_origin = '중식'
  elif food in list(set(category['양식']) - set(set_japanese)):
    str_origin = '양식'
  wtr.writerow([food, str_category, str_subcategory,str_main_ingre, str_origin])
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