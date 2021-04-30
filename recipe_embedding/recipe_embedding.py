import gensim.models
from gensim.models import FastText
from gensim.models import KeyedVectors
import csv
import os

recipe_sentences = [] # csv파일로 부터 읽어온 documents 저장
direction = 'recipe_data/'
recipe_folder = os.listdir(direction) # recipe_data폴더에 들어있는 파일(폴더) 목록 list
for i, folder in enumerate(recipe_folder):
    csv_filepath = os.listdir(direction + folder) # 해당 폴더에 들어있는 csv파일 목록 list
    for j, csv_file in enumerate(csv_filepath):
        fi = open(direction+folder+'/'+csv_file, 'rt', encoding='UTF8')
        rdr = csv.reader(fi)
        for k, row in enumerate(rdr):
            if k == 0:
                continue
            elif k % 2 == 0:
                recipe_sentences.append(row)
        fi.close()

model_ingredient = FastText(sg=1, window = 10 * 1000000, vector_size=100, min_count=3) # item2vec로 사용하기 위해 windowsize를 크게 설정
model_ingredient.build_vocab(recipe_sentences)
model_ingredient.train(recipe_sentences, epochs = 10, total_examples=model_ingredient.corpus_count)

model_ingredient.save("./_model_ingredient") #학습한 모델 저장
model_ingredient.wv.save("./_model_ingredient_wv") #학습한 모델의 wv 저장

similarity = model_ingredient.wv.most_similar(positive=['소세지'])
print(similarity)

