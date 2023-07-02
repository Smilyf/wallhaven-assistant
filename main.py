import requests
import json
import os
import datetime
import inspect
# 获取当前模块文件的路径
current_module_file = inspect.getfile(inspect.currentframe())

# 获取文件所在的目录路径
current_directory_path = os.path.dirname(os.path.abspath(current_module_file))

now = str(datetime.datetime.today().date())

with open(current_directory_path+"\\parm.json", 'r') as file:
    parm=json.loads(file.read())
categories=parm["categories"] 
purity=parm["purity"]
topRange=parm["topRange"]  
sorting=parm["sorting"]
order=parm["order"]
ai_art_filter=parm["ai_art_filter"]
apikey=parm["apikey"]
url = "https://wallhaven.cc/api/v1/search?"
string=f"categories={categories}&purity={purity}&topRange={topRange}&sorting={sorting}&order={order}&ai_art_filter={ai_art_filter}&apikey={apikey}&page="
if apikey == "":
    string=f"categories={categories}&purity={purity}&topRange={topRange}&sorting={sorting}&order={order}&ai_art_filter={ai_art_filter}&page="
url +=string
save_path= 'D:\\壁纸\\'+str(purity)+'\\'
url_list = []

def download_image(url, save_path,num):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path+ now+"\\"+link.split('/')[-1], 'wb') as file:
            file.write(response.content)
        with open(save_path + "list.json", 'r') as file:
            list_images=json.loads(file.read())
            list_images[url]=now
            
        with open(save_path + "list.json", 'w') as file:
            file.write(json.dumps(list_images))
        
        with open(save_path + now +"\\"+"list_day.json", 'r') as file:  
            list_day=json.loads(file.read())
            list_day[url.split('/')[-1]]=" "
        with open(save_path + now +"\\"+"list_day.json", 'w') as file:  
            file.write(json.dumps(list_day)) 
        print('第{}张图片下载完成'.format(num))
        return True
    else:
        print('第{}张图片下载失败'.format(num))
        return False

a = os.path.exists(save_path + now)
if a:
    print("文件夹已存在,下一步")
else:
    os.makedirs(save_path + now)
    with open(save_path + now +"\\"+"list_day.json", 'w') as file:
        # 可以在这里执行一些操作，如写入内容等
        file.write("{}")
        print("list_day.json文件建立成功")
    print("day文件夹建立成功")

list_images=json.loads("{}")
a = os.path.exists(save_path + "list.json")
if a:
    with open(save_path + "list.json", 'r+') as file:
        list_images=json.loads(file.read())
    print("list.json文件已存在,下一步")
else:
    # 使用 'w' 模式打开文件，如果文件不存在则创建新文件
    with open(save_path + "list.json", 'w') as file:
        # 可以在这里执行一些操作，如写入内容等
        file.write("{}")
        print("list.json文件建立成功")

for page in range(1, 2):
    res = requests.get(url + str(page))
    paper = json.loads(res.content)
    for x in paper["data"]:
        path=x["path"]
        if list_images.get(path) is  None:
            url_list.append(x["path"])
            list_images[path]=str(now)
        
print("图片链接获取完毕，图片数量："+str(len(url_list)))

num=1
for link in url_list:
    print(link)
    if  download_image(link, save_path,num):
        num+=1
    else:
        break
print("文件路径:{}".format(save_path + now))

