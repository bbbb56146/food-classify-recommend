import json
import requests

food_freq = {}
food_freq['닭갈비'] = 6
food_freq['오일파스타'] = 8
food_freq['김밥'] = 3
food_freq['된장찌개'] = 5
food_freq['쌀국수'] = 2

user_feedback = {}
user_feedback['닭갈비'] = 4
user_feedback['김밥'] = 13
user_feedback['떡볶이'] = 7

params_dict = {}

params_dict['food_freq'] = json.dumps(food_freq, ensure_ascii=False) # food_freq dictionary를 json으로 바꾼 값
params_dict['user_feedback'] = json.dumps(user_feedback, ensure_ascii=False) # user_feedback dictionary를 json으로 바꾼 값
print(params_dict)

req = requests.get('http://127.0.0.1:5000//method', params=params_dict)
json_object = json.loads(req.text)
print(json_object)

for info in json_object['info']:
  print(info) #추천메뉴, 유사도, 추천 가게 수

for data in json_object['data']:
    print(data['menuName'])
    print("Metadata : {}".format(data['meta']))
    for doc in data['document']:
      print(doc)
    print("\n")





