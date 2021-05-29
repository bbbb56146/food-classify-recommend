# import gensim.models
from gensim.models import FastText
from gensim.models import KeyedVectors
import csv
import os

# filepath 폴더에 저장된 레시피데이터를 이용하여 FastText모델 학습, 학습된 모델을 return
def recipe_to_ingre2vec (filepath='../recipe_data/'):
    recipe_sentences = []  # csv파일로 부터 읽어온 documents 저장
    recipe_folder = os.listdir(filepath)  # recipe_data폴더에 들어있는 파일(폴더) 목록 list
    for i, folder in enumerate(recipe_folder):
        csv_filepath = os.listdir(filepath + folder)  # 해당 폴더에 들어있는 csv파일 목록 list
        for j, csv_file in enumerate(csv_filepath):
            fi = open(filepath + folder + '/' + csv_file, 'rt', encoding='UTF8')
            rdr = csv.reader(fi)
            for k, row in enumerate(rdr):
                if k == 0:
                    continue
                elif k % 2 == 0:
                    recipe_sentences.append(row)
            fi.close()

    model_ingredient = FastText(sg=1, window=10 * 1000000, vector_size=100,
                                min_count=3)  # item2vec로 사용하기 위해 windowsize를 크게 설정
    model_ingredient.build_vocab(recipe_sentences)
    model_ingredient.train(recipe_sentences, epochs=10, total_examples=model_ingredient.corpus_count)

    print("length of ingex2vec: %i" % (len(model_ingredient.wv.index_to_key)))
    print("Ingre2vec embedding finished!")
    return model_ingredient

# ingre2vec 모델과 wv를 저장
def save_ingre2vec(ingre2vec, filepath='./', filename='_model_ingredient'):
    ingre2vec.save(filepath + filename)
    ingre2vec.wv.save(filepath + filename + '_wv')

# 저장된 ingre2vec모델을 불러오기
def load_ingre2vec_model(ingre2vec, filepath='./', filename='_model_ingredient'):
    return FastText.load(filepath + filename)

# 저장된 ingre2vec의 wv를 불러오기
def load_ingre2vec_wv(ingre2vec, filepath='./', filename='_model_ingredient_wv'):
    return KeyedVectors.load(filepath + filename)

'''
ingre2vec = recipe_to_ingre2vec('../recipe_data/') # recipe_data 폴더에 있는 레시피를 이용하여 모델 학습
save_ingre2vec(ingre2vec, filepath='./') # 학습된 모델과 wv를 저장

similarity = ingre2vec.wv.most_similar(positive=['소세지'])
print(similarity)
'''
