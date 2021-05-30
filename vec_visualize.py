from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
from IPython.display import display
import os
from recipe_embedding import menu_embedding

# matplotlib 폰트관련 설정
mpl.rcParams['axes.unicode_minus'] = False
font_path = r'C:\Windows\Fonts\malgunsl.ttf'
font_name = fm.FontProperties(fname=font_path).get_name()
plt.rc('font', family=font_name)
fontprop = fm.FontProperties(fname=font_path)


def show_tsne(X_in, vocab):
  tsne = TSNE(n_components=2, perplexity=10)
  X = tsne.fit_transform(X_in)  # tsne로 차원 축소

  df = pd.DataFrame(X, index=vocab, columns=['x', 'y'])

  fig = plt.figure()
  fig.set_size_inches(10, 10)
  ax = fig.add_subplot(1, 1, 1)
  for i in range(len(X_in)):
    if Label_flag[Label[i]] == 0:
      ax.scatter(df['x'][i], df['y'][i], s=S[i], c=C[i], label=Label[i])
      Label_flag[Label[i]] = 1
    else:
      ax.scatter(df['x'][i], df['y'][i],  s=S[i], c=C[i])

  for word, pos in df.iterrows():
    ax.annotate(word, pos, fontproperties=fontprop, size=5)

  plt.legend()
  plt.xlabel("T-sne attribute 0")
  plt.ylabel("T-sne attribute 1")

  fig_tsne = plt.gcf()
  plt.show(loc=(1.0, 1.0)) # plot을 출력
  fig_tsne.savefig('./menu2vec_tsne.png') # plot을 이미지 파일로 저장


# menu의 category 분류하기
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
Label_flag = {}
X_set = ['국_탕', '메인반찬', '면_만두', '밥_죽_떡', '빵', '양식', '찌개']
for food in menu2vec.index_to_key:
  S.append(10)
  if food in category['국_탕']:
    C.append('violet')
    Label.append(X_set[0])
    Label_flag[X_set[0]] = 0
  elif food in category['메인반찬']:
    C.append('green')
    Label.append(X_set[1])
    Label_flag[X_set[1]] = 0
  elif food in category['면_만두']:
    C.append('blue')
    Label.append(X_set[2])
    Label_flag[X_set[2]] = 0
  elif food in category['밥_죽_떡']:
    C.append('black')
    Label.append(X_set[3])
    Label_flag[X_set[3]] = 0
  elif food in category['빵']:
    C.append('brown')
    Label.append(X_set[4])
    Label_flag[X_set[4]] = 0
  elif food in category['양식']:
    C.append('springgreen')
    Label.append(X_set[5])
    Label_flag[X_set[5]] = 0
  elif food in category['찌개']:
    C.append('red')
    Label.append(X_set[6])
    Label_flag[X_set[6]] = 0

sz = 210
X_show = X[:sz,:]
vocab_show = vocab[:sz]
show_tsne(X, vocab)