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


def show_tsne(df, filename='menu2vec_tsne.png'):
  #tsne = TSNE(n_components=2, perplexity=10)
  #X_tsne = tsne.fit_transform(X_in)  # tsne로 차원 축소

  #df = pd.DataFrame(X_tsne, index=vocab, columns=['x', 'y'])

  fig = plt.figure()
  fig.set_size_inches(10, 10)
  ax = fig.add_subplot(1, 1, 1)
  for i in range(len(X_tsne)):
    if Label_flag[Label[i]] == 0:
      ax.scatter(df['x'][i], df['y'][i], s=S[i], c=C[i], label=Label[i])
      Label_flag[Label[i]] = 1
    else:
      ax.scatter(df['x'][i], df['y'][i],  s=S[i], c=C[i])

  for word, pos in df.iterrows():
    if word not in vocab_notin:
      ax.annotate(word, pos, fontproperties=fontprop, size=5)

  plt.legend()
  plt.xlabel("T-sne attribute 0")
  plt.ylabel("T-sne attribute 1")

  fig_tsne = plt.gcf()
  plt.show(loc=(1.0, 1.0)) # plot을 출력
  fig_tsne.savefig('./tsne_image/' + filename) # plot을 이미지 파일로 저장


# 폳더별로 menu의 category 분류하기
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

set_soup = list(set(category['국_탕'] + category['찌개']))

set_main_meat = ['갈비찜', '고추잡채','닭갈비', '돈까스', '돼지갈비찜', '떡갈비','불고기', '소갈비찜', '소불고기', '수육', '제육볶음', '콩나물불고기', '탕수육' ,'찜닭', '치킨']
set_main_seafood = ['고등어조림', '골뱅이무침', '갈치조림','낙지볶음','오징어볶음','주꾸미볶음','코다리조림']
set_main_etc = ['두부김치',  '마파두부', '순대볶음', '월남쌈', '잡채']
set_noodle = ['국수','김치비빔국수', '냉면', '라면', '바지락칼국수', '볶음라면', '볶음우동', '비빔국수', '비빔면',
              '열무비빔국수', '우동', '잔치국수', '짜장면', '짬뽕', '쫄면', '칼국수', '콩국수']
set_pasta = ['까르보나라', '스파게티', '알리오올리오', '오일파스타', '크림스파게티', '토마토스파게티', '토마토파스타', '크림파스타']
set_rice = ['계란볶음밥',  '김밥', '김치볶음밥', '꼬마김밥', '단호박죽', '덮밥', '리조또',
            '밥', '볶음밥', '비빔밥', '새우볶음밥', '쌈밥', '오므라이스', '유부초밥', '전복죽', '주먹밥', '죽', '짜장밥', '참치김밥', '초밥', '카레', '카레라이스', '콩나물밥']
set_ricecake = ['국물떡볶이', '궁중떡볶이', '기름떡볶이','떡', '떡꼬치', '떡볶이']
set_bread = category['빵']
set_western = category['양식']
menu2vec = menu_embedding.load_menu2vec()
vocab = list(menu2vec.index_to_key)
X = menu2vec[vocab]
X_set = ['국물류', '메인_육류', '메인_해산물', '메인_기타', '국수류', '파스타','밥', '떡', '빵', '양식']
vocab_x = list(set(set_soup+set_main_meat+set_main_seafood+set_main_etc+set_noodle+set_pasta+set_rice+set_ricecake+set_bread+set_western))
vocab_notin = list(set(vocab) - set(vocab_x))
C = []
S = []
Label = []
Label_flag = {}

for food in menu2vec.index_to_key:
  S.append(10)
  if food in set_soup:
    C.append('violet')
    Label.append(X_set[0])
    Label_flag[X_set[0]] = 0
  elif food in set_main_meat:
    C.append('red')
    Label.append(X_set[1])
    Label_flag[X_set[1]] = 0
  elif food in set_main_seafood:
    C.append('blue')
    Label.append(X_set[2])
    Label_flag[X_set[2]] = 0
  elif food in set_main_etc:
    C.append('slategray')
    Label.append(X_set[3])
    Label_flag[X_set[3]] = 0
  elif food in set_noodle:
    C.append('brown')
    Label.append(X_set[4])
    Label_flag[X_set[4]] = 0
  elif food in set_pasta:
    C.append('seagreen')
    Label.append(X_set[5])
    Label_flag[X_set[5]] = 0
  elif food in set_rice:
    C.append('yellow')
    Label.append(X_set[6])
    Label_flag[X_set[6]] = 0
  elif food in set_ricecake:
    C.append('orange')
    Label.append(X_set[7])
    Label_flag[X_set[7]] = 0
  elif food in set_bread:
    C.append('darkgoldenrod')
    Label.append(X_set[8])
    Label_flag[X_set[8]] = 0
  elif food in set_western:
    C.append('springgreen')
    Label.append(X_set[9])
    Label_flag[X_set[9]] = 0
  else:
    C.append('black')
    Label.append('')
    Label_flag[''] = 0
tsne = TSNE(n_components=2, perplexity=10)
X_tsne = tsne.fit_transform(X)  # tsne로 차원 축소
df = pd.DataFrame(X_tsne, index=vocab, columns=['x', 'y'])
show_tsne(df, filename='menu2vec_tsne_all.png')


set_western = [food for food in category['양식']]
set_chinese = ['마파두부', '탕수육', '짜장면', '고추잡채', '짬뽕', '계란볶음밥', '볶음밥', '짜장밥']
set_japanese = ['밀푀유나베', '돈까스', '볶음우동', '우동', '유부초밥', '주먹밥', '초밥', '카레라이스']
set_korean = ['갈비탕', '감자국', '감자탕', '계란국', '국', '김치콩나물국', '꽃게탕', '닭개장', '닭곰탕', '닭볶음탕', '된장국', '떡국', '떡만두국', '만두국', '미역국',  '배추된장국', '북어국', '삼계탕', '소고기무국', '소고기미역국', '시금치된장국',  '오이냉국', '오징어무국', '육개장', '콩나물국', '탕', '홍합탕',
              '갈비찜', '갈치조림', '고등어조림', '골뱅이무침', '구이', '낙지볶음', '닭갈비', '돼지갈비찜', '두부김치', '불고기', '소갈비찜', '소불고기', '수육', '순대볶음', '오징어볶음', '잡채', '제육볶음', '주꾸미볶음', '찜', '찜닭', '코다리조림', '콩나물불고기',
              '김치비빔국수', '냉면', '라면', '만두', '바지락칼국수', '비빔국수', '비빔만두', '비빔면', '수제비', '열무비빔국수', '잔치국수', '쫄면', '칼국수', '콩국수',
              '계란볶음밥', '국물떡볶이', '궁중떡볶이', '기름떡볶이', '김밥', '김치볶음밥', '꼬마김밥', '단호박죽', '덮밥', '떡', '떡꼬치', '떡볶이', '볶음밥', '비빔밥', '새우볶음밥', '쌈밥', '전복죽', '죽', '참치김밥', '초밥', '콩나물밥',
              '감자고추장찌개', '감자짜글이', '고추장찌개', '김치찌개', '꽁치김치찌개', '냉이된장찌개', '달래된장찌개', '동태찌개', '돼지고기고추장찌개', '돼지고기김치찌개',
              '된장찌개', '두부찌개', '바지락순두부찌개', '부대찌개', '비지찌개', '순두부찌개','스팸김치찌개', '애호박찌개', '오징어찌개', '우렁된장찌개', '전찌개',
              '짜글이', '찌개', '차돌박이된장찌개', '참치김치찌개', '청국장', '청국장찌개', '콩나물찌개', '콩비지찌개']


vocab_y = list(set(set_western + set_chinese + set_japanese + set_korean))
vocab_notin = list(set(vocab) - set(vocab_y))
Y = []
Y_set = ['양식', '중식', '일식', '한식']
C = []
S = []
Label = []
Label_flag = {}
for food in vocab:
  Y.append(menu2vec[food])
  S.append(10)
  if food in set_western:
    C.append('blue')
    Label.append(Y_set[0])
    Label_flag[Y_set[0]] = 0
  elif food in set_chinese:
    C.append('yellow')
    Label.append(Y_set[1])
    Label_flag[Y_set[1]] = 0
  elif food in set_japanese:
    C.append('red')
    Label.append(Y_set[2])
    Label_flag[Y_set[2]] = 0
  elif food in set_korean:
    C.append('green')
    Label.append(Y_set[3])
    Label_flag[Y_set[3]] = 0
  else:
    C.append('black')
    Label.append('')
    Label_flag[''] = 1

show_tsne(df, 'menu2vec_tsne_origin.png')

