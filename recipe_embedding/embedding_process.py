from gensim.models import FastText
from gensim.models import KeyedVectors

import ingre_embedding
import menu_embedding


ingre2vec = ingre_embedding.recipe_to_ingre2vec(filepath='../recipe_data/') # recipe_data 폴더에 있는 레시피를 이용하여 모델 학습
ingre_embedding.save_ingre2vec(ingre2vec, filepath='./', filename='_model_ingredient') # 학습된 모델과 wv를 저장

menu2vec = menu_embedding.get_menu2vec(ingre2vec.wv, filepath='../recipe_data/') # ingre2vec의 wv를 이용하여 menu 임베딩
menu_embedding.save_menu2vec(menu2vec, filepath='./', filename='_menu2vec_wv') # menu2vec 저장

print("========")
print("length of ingex2vec: %i" % (len(ingre2vec.wv.index_to_key)))
print("number of sentences: %i" %(ingre2vec.corpus_count))
print("number of words: %i" %(ingre2vec.corpus_total_words))
print("length of menu2vec: %i" %(len(menu2vec.index_to_key)))
# similarity = ingre2vec.wv.most_similar(positive=['소세지'])
# print(similarity)