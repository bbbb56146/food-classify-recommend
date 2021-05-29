# food-classify-recommend
- recipe_embedding/ : ingre2vec, menu2vec생성 관련 <br/>
&nbsp;&nbsp;- ingre_embedding.py : recipe_data -> ingre2vec 생성 관련된 모듈 <br/>
&nbsp;&nbsp;- menu_embedding.py : ingre2vec -> menu2vec 생성 관련된 모듈 <br/>
&nbsp;&nbsp;- embedding_process : 위의 모듈들을 이용하여 recipe data로부터 menu2vec를 생성하는 code <br/>
- recipe_crawling/ : recipe data crawling 관련 <br/>
- KakaoLocalApi.py : Kakao API 사용에 관련된 모듈 <br/>    
- recommend_foods.py : food_preference dictionary와 menu2vec를 이용하여 음식 추천 <br/>