import itchat
from pyecharts import Pie
import re,jieba
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud,ImageColorGenerator
import numpy as np
import PIL.Image as Image
itchat.auto_login(hotReload=True)
itchat.dump_login_status()

data=pd.DataFrame()
columns=['NickName', 'Sex', 'Province', 'City', 'Signature']
friends=itchat.get_friends(update=True)[:]
print(friends)
my=friends[0]
def echart_pie(friends):
    total = len(friends) - 1
    male = female = other = 0
    for friend in friends[1:]:
        sex=friend["Sex"]
        if sex==1:
            male+=1
        elif sex==2:
            female+=1
        else:
            other+=1
        attr = ["男性","女性","其他"]
        v1=[float(male) / total * 100,float(female) / total * 100,float(other) / total * 100]
        pie=Pie(my["NickName"]+"的微信好友性别比例",title_pos="center")
        pie.add("性别",attr,v1,center=[50,50],is_random=True, radius=[30, 75], rosetype='area',
                is_legend_show=False, is_label_show=True)
        pie.render()
echart_pie(friends)

def plot_cloud(columns):
    for col in columns:
        val = []
        for i in friends[1:]:  # friends[0]是自己的信息，因此我们要从[1:]开始
            val.append(i[col])
        data[col] = pd.Series(val)

    siglist = []
    for i in data['Signature']:
        signature = i.strip().replace('emoji','').replace('span','').replace('class','')
        rep = re.compile('1f\d+\w*|[<>/=]')  # 具体含义另行查看
        signature = rep.sub('', signature)
        siglist.append(signature)
    text = ''.join(siglist)
    word_list = jieba.cut(text, cut_all=True)
    word_space_split = ' '.join(word_list)
    coloring = np.array(Image.open("D:/pachong/weixin/qqq.jpg"))  #这个路径可以改，最好还是不要改
    my_wordcloud = WordCloud(background_color="white", max_words=2000,
                             mask=coloring, max_font_size=100, random_state=42, scale=2,
                             font_path="C:/Windows/Fonts/simkai.ttf").generate(word_space_split)
    image_colors = ImageColorGenerator(coloring)
    plt.imshow(my_wordcloud.recolor(color_func=image_colors))
    plt.imshow(my_wordcloud)
    plt.axis("off")
    plt.show()

# plot_cloud(columns)

# [{},{}]
# total_list=[]
# person_dict={}
from pyecharts import Map
map_province=[]
map_prodic={}
map_attr=[]
map_val=[]
def plot_location(friends):
    for friend in friends[1:]:
        map_province.append(friend['Province'])
        while '' in map_province:
            map_province.remove('')  # 删除空字符
    map_dict=set(map_province)
    for mdi in map_dict:
        map_prodic[mdi]=map_province.count(mdi)
    print(map_prodic)
    for province_key in map_prodic:
        map_attr.append(province_key)
        map_val.append(map_prodic[province_key])
    print(map_attr)
    print(map_val)
    # 开始绘制
    map = Map(my["NickName"]+"的微信好友位置分布图", width=1200, height=600,title_pos='center')
    map.add("", map_attr, map_val, is_visualmap=True,visual_range=[0,120],visual_text_color='#000', is_map_symbol_show=False, is_label_show=True)
    map.render()

# plot_location(friends)

import pymysql.cursors
def save_mysql(friends):
    connection=pymysql.connect(host='localhost',user='XXXX',password='XXXX',db='myWeinxinData',charset='utf8mb4')
    try:
        for friend in friends[1:]:
            with connection.cursor() as cursor:
                sql = "insert into `key_Info`(`UserName`,`NickName`,`Sex`,`HeadImgUrl`,`Province`,`City`,`Signature`)values(%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql, (
                friend['UserName'], friend['Sex'], friend['NickName'], friend['HeadImgUrl'], friend['Province'], friend['City'],
                friend['Signature']))
                connection.commit()
    finally:
        connection.close()

# save_mysql(friends)
