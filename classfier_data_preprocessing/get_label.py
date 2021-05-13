## 레이블(클래스)을 얻기 위해 작성한 프로그램
import os

path_dir = 'origin/'
ans=[]
first_folder_list = os.listdir(path_dir)
print(first_folder_list)
for i ,folder in enumerate(first_folder_list):
    second_path = os.listdir(path_dir+folder)
    ans+=second_path
    print(second_path)


while '.DS_Store' in ans:
    ans.remove(".DS_Store")
print(ans)
print(len(ans))