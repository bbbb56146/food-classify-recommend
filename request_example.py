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

for key in json_object.keys():
  if key == 'info':
    continue
  print(key)
  print("MetaData : {}".format(json_object[key]['meta']))
  for document in json_object[key]['documents']:
    print(document)

for info in json_object['info']:
  print(info) #추천메뉴, 유사도, 추천 가게 수


'''
params = {}
req = requests.get('http://127.0.0.1:8000/frc_api/', params=food_freq)
json_object = json.loads(req.text)
#print(json_object)

for key in json_object.keys():
  print(key)
  print("MetaData : {}".format(json_object[key]['meta']))
  for document in json_object[key]['documents']:
    print(document)
'''

'''
array_1 = '{"A" : 1, "B" : 15, "C": 9 }'
json_data = json.loads(array_1)
print(json_data)
print(json_data['A'])


array_2 = {
    'food_pref_dict': {}
}
array_2['food_pref_dict']['닭갈비'] = 6
array_2['food_pref_dict']['오일파스타'] = 8
array_2['food_pref_dict']['김밥'] = 3
array_2['food_pref_dict']['된장찌개'] = 5
array_2['food_pref_dict']['쌀국수'] = 2

with open('array_2.json', 'w', encoding='UTF-8') as f:
    json.dump(array_2, f, ensure_ascii=False)

json_data = open('array_2.json', 'r', encoding='UTF-8').read()
print(json_data)
'''