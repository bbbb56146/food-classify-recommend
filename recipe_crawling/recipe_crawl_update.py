import urllib
import urllib.request
from bs4 import BeautifulSoup
import csv
import os

# 해당 주소(url_pre + url_href)에서 recipie의 제목과 재료를 크롤링
def crawl_from_url(url_href):
    url_pre = "https://www.10000recipe.com"
    url = url_pre + url_href
    req = urllib.request.urlopen(url)
    res = req.read()

    soup = BeautifulSoup(res, 'html.parser')  # BeautifulSoup 객체생성

    title_codes = soup.find('div', 'view2_summary')
    if title_codes == None:
        return
    title_codes = title_codes.find('h3')
    recipe_title.append(title_codes.get_text())

    ingre_tmp = []

    ingre_codes = soup.find('div', 'cont_ingre2')
    if ingre_codes == None:
        del recipe_title[len(recipe_title)-1]
        return
    ingre_codes = ingre_codes.find_all('li')
    for i in range(len(ingre_codes)):
        ingre_tmp.append(ingre_codes[i].get_text())
        ingre_tmp[i] = ingre_tmp[i].split('\n')[0]
        ingre_tmp[i] = ingre_tmp[i].split('  ')[0]
        ingre_tmp[i] = ingre_tmp[i].split('(')[0]
    recipe_ingre.append(ingre_tmp)

# 메인페이지(main_url)에서 표시된 각 recipe의 주소(href) 얻기
def crawl_href(keyword, order, page):
    url_pre = "https://www.10000recipe.com/recipe/list.html?q="
    main_url = url_pre + urllib.parse.quote(keyword) + "&order=" + order + "&page=" + str(page)
    main_req = urllib.request.urlopen(main_url)
    main_res = main_req.read()
    main_soup = BeautifulSoup(main_res, 'html.parser')  # BeautifulSoup 객체생성

    addr_codes = main_soup.find('ul', 'common_sp_list_ul ea4')
    if addr_codes == None:
        return
    addr_codes = addr_codes.find_all('a', 'common_sp_link')
    for addr_code in addr_codes:
        recipe_href.append(addr_code.get('href'))

# 폴더 생성
def createdir(direction):
    if not os.path.exists(direction):
        os.makedirs(direction)


# 새로 crawling할 음식들 목록 지정!
keywords = ['마라탕', '쌀국수', '가지볶음', '오믈렛']

# 각 keyword(음식 메뉴)에 대해 진행
for i, keyword in enumerate(keywords):
    recipe_href = []    # 각 레시피 페이지의 주소 뒷부분을 저장
    recipe_title = []   # 각 레시피 페이지의 제목을 저장
    recipe_ingre = []   # 각 레시피의 재료 목록을 저장

    print(keyword)  # 현재 keyword 출력
    # 추천순(reco), 5번째 page까지 recipe주소(href) crawling
    for i in range(1, 6):
        crawl_href(keyword, "reco", i)

    # 해당 주소에서 레시피 정보(title, ingredients) crawling
    for i, href in enumerate(recipe_href):
        print(i, end='\t')
        print("https://www.10000recipe.com" + href)
        if len(recipe_title) != len(recipe_ingre):
            print("Error!")
            break
        else:
            crawl_from_url(href)
    print(len(recipe_title))    # 해당 keyword에 대한 크롤링이 완료되면, 크롤링한 페이지 수를 출력

    # csv파일로 저장
    direction = './New_csv/'
    createdir(direction)
    csv_wr = open(direction + '/recipe_'+ keyword + '.csv', 'w', encoding='UTF8')
    wtr = csv.writer(csv_wr, lineterminator='\n')
    wtr.writerow([keyword, "추천순", len(recipe_title)])
    for i in range(len(recipe_title)):
        wtr.writerow([recipe_title[i], "https://www.10000recipe.com"+recipe_href[i]])
        wtr.writerow(recipe_ingre[i])
    csv_wr.close()

    '''
    csv_rd = open(direction + '/recipe_'+ keyword + '.csv', 'r', encoding='UTF8')
    rdr = csv.reader(csv_rd)
    for row in rdr:
        print(row)
    csv_rd.close()
    '''