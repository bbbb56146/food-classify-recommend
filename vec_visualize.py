from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
from gensim.models import KeyedVectors
import os
from recipe_embedding import menu_embedding

mpl.rcParams['axes.unicode_minus'] = False

font_path = r'C:\Users\daraH\Downloads\NanumFontSetup_TTF_GOTHIC\NanumGothic.ttf'
font_name = fm.FontProperties(fname=font_path).get_name()
plt.rc('font', family=font_name)
fontprop = fm.FontProperties(fname=font_path)

def show_tsne():
  tsne = TSNE(n_components=2, perplexity=10)
  X = tsne.fit_transform(X_show)

  df = pd.DataFrame(X, index=vocab_show, columns=['x', 'y'])
  fig = plt.figure()
  fig.set_size_inches(10, 10)
  ax = fig.add_subplot(1, 1, 1)
  ax.scatter(df['x'], df['y'], s=S, c=C, label=Label)

  for word, pos in df.iterrows():
    ax.annotate(word, pos, fontproperties=fontprop, size=5)

  plt.legend()
  plt.xlabel("T-sne attribute 0")
  plt.ylabel("T-sne attribute 1")
  plt.show(loc=(1.0, 1.0))
  #plt.savefig('./menu2vec_tsne.png')

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

menu2vec = menu_embedding.load_menu2vec()
vocab = list(menu2vec.index_to_key)
X = menu2vec[vocab]

C = []
S = []
Label = []
for food in menu2vec.index_to_key:
  S.append(10)
  if food in category['국_탕']:
    C.append('violet')
    Label.append('Set1')
  elif food in category['메인반찬']:
    C.append('green')
    Label.append('Set2')
  elif food in category['면_만두']:
    C.append('blue')
    Label.append('Set3')
  elif food in category['밥_죽_떡']:
    C.append('black')
    Label.append('Set4')
  elif food in category['빵']:
    C.append('brown')
    Label.append('Set5')
  elif food in category['양식']:
    C.append('springgreen')
    Label.append('Set6')
  elif food in category['찌개']:
    C.append('red')
    Label.append('Set7')

sz = 210
X_show = X[:sz,:]
vocab_show = vocab[:sz]
show_tsne()