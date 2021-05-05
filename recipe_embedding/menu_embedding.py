import gensim.models
from gensim.models import FastText
from gensim.models import KeyedVectors
import csv
import os
import numpy as np
"""
# 불러오기
model_ingredient_loaded = FastText.load('./_model_ingredient') #모델 로드
wv_ingredient_loaded = KeyedVectors.load('./_model_ingredient_wv') #wv 로드

#csv 파일 탐색 :
recipe_sentences = []

menu_name ="" #메뉴명 문자열
menu_dict = {} #메뉴 딕셔너리
#int recipe_tot #csv 파일 속 레시피 수
direction = '../recipe_data/'
print(os.listdir(direction))
recipe_folder = os.listdir(direction)
for i, folder in enumerate(recipe_folder):  #폴더 속 탐색
  csv_filepath = os.listdir(direction + folder)
  for j, csv_file in enumerate(csv_filepath): #csv 파일 속 탐색
    fi = open(direction+folder+'/'+csv_file, 'rt',encoding='UTF8')
    rdr = csv.reader(fi)
    #recipe_idx = 0
    for k, row in enumerate(rdr):
      if k == 0:
        menu_name = row[0] #메뉴 이름
        recipe_tot = row[2]
        continue
      elif k % 2 == 0:
        #레시피별 벡터 계산(wv 활용)
        #일단 가장 추천이 많은 첫번째 레시피만 사용
        #recipe_idx+=1 # 레시피 인덱스 증가
        recipe_vec = [0 for i in range(100)] # 100 : wv size
        for l, ingredient in enumerate(row):
          recipe_vec = [(recipe_vec[i] + model_ingredient_loaded.wv[ingredient][i])/len(row) for i in range(100)]
        menu_dict[menu_name] = recipe_vec
        break
    fi.close()

  print(len(menu_dict))
  for key, value in menu_dict.items():
    print(key, value)
"""

def get_menu2vec(loaded_wv):
  menu2vec = KeyedVectors(vector_size=100) # menu embedding 결과를 저장

  menu_name = ""  # 메뉴명 문자열
  menu_dict = {}  # 메뉴 딕셔너리
  # int recipe_tot #csv 파일 속 레시피 수
  direction = './recipe_data/'
  print(os.listdir(direction))
  recipe_folder = os.listdir(direction)
  for i, folder in enumerate(recipe_folder):  # 폴더 속 탐색
    csv_filepath = os.listdir(direction + folder)
    for j, csv_file in enumerate(csv_filepath):  # csv 파일 속 탐색
      fi = open(direction + folder + '/' + csv_file, 'rt', encoding='UTF8')
      rdr = csv.reader(fi)
      # recipe_idx = 0
      recipe_vec = [0 for i in range(100)]  # 100 : wv size
      for k, row in enumerate(rdr):
        if k == 0:
          menu_name = row[0]  # 메뉴 이름
          recipe_tot = row[2]
          continue
        elif k % 2 == 0:
          # 레시피별 벡터 계산(wv 활용)
          # 모든 레시피 평균 구하기
          # recipe_idx+=1 # 레시피 인덱스 증가
          tmp_vec = [0 for i in range(100)]  # 100 : wv size
          for l, ingredient in enumerate(row):
            tmp_vec = [(recipe_vec[i] + loaded_wv[ingredient][i]) / len(row) for i in range(100)]
          recipe_vec = [(recipe_vec[i]*((k/2)-1) + tmp_vec[i]) / (k/2) for i in range(100)]
          #menu_dict[menu_name] = recipe_vec
      menu2vec.add_vector(menu_name, recipe_vec)
      fi.close()

  print("length of menu2vec: %i" %(len(menu_dict)))
  return menu2vec

def save_menu2vec(menu2vec, filepath = './recipe_embedding/', filename = '_menu2vec_wv'):
  menu2vec.save(filepath + filename)

def load_menu2vec(filepath = './recipe_embedding/', filename = '_menu2vec_wv'):
  return KeyedVectors.load(filepath + filename)
