import itchat
from pyecharts import Pie
import re,jieba
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud,ImageColorGenerator
import numpy as np
import PIL.Image as Image
# 通过如下命令登陆，即使程序关闭，一定时间内重新开启也可以不用重新扫码。该方法会生成一个静态文件 itchat.pkl ，用于存储登陆的状态
itchat.auto_login(hotReload=True)
# 导出设置
itchat.dump_login_status()
data=pd.DataFrame()
columns=['NickName', 'Sex', 'Province', 'City', 'Signature']
friends=itchat.get_friends(update=True)[:]
print(friends)
my=friends[0]

# 绘制男女比例饼图
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
        # render()方法会生成一个render.html，然后在浏览器运行就出现图形
        pie.render()
echart_pie(friends)

# 绘制词云
def plot_cloud(columns):
    # 通过循环得到第一列索引，后面列名分别为columns的各个元素，类似于数据库表
    for col in columns:
        val = []
        for i in friends[1:]:  # friends[0]是自己的信息，因此我们要从[1:]开始
            val.append(i[col])
        data[col] = pd.Series(val)

    siglist = []
    for i in data['Signature']:
        # 正则替换---strip()去除空格，replace替换特殊字符
        signature = i.strip().replace('emoji','').replace('span','').replace('class','')
        rep = re.compile('1f\d+\w*|[<>/=]')
        signature = rep.sub('', signature)
        siglist.append(signature)
    text = ''.join(siglist)
    word_list = jieba.cut(text, cut_all=True)
    word_space_split = ' '.join(word_list)
    # PIL：Python Imaging Library，图像处理标准库，打开一个jpg图像文件
    # numpy创建数组，临时存储打开的图片
    coloring = np.array(Image.open("D:/pachong/weixin/qqq.jpg"))
    my_wordcloud = WordCloud(background_color="white", max_words=2000,
                             mask=coloring, max_font_size=100, random_state=42, scale=2,
                             font_path="C:/Windows/Fonts/simkai.ttf").generate(word_space_split)
    image_colors = ImageColorGenerator(coloring)
    plt.imshow(my_wordcloud.recolor(color_func=image_colors))
    plt.imshow(my_wordcloud)
    plt.axis("off")
    plt.show()

plot_cloud(columns)



# 绘制省份地图
# [{},{}]
# total_list=[]
# person_dict={}
from pyecharts import Map
map_province=[]
map_prodic={}
map_attr=[]
map_val=[]
def plot_location(friends):
    ## 通过循环实现将所有好友所在省份加到列表中，并且去除空字符
    for friend in friends[1:]:
        map_province.append(friend['Province'])
        while '' in map_province:
            map_province.remove('')  # 删除空字符
    # 将上述列表通过set变为字典，去重
    map_dict=set(map_province)
    # 生成一个key为省份，value为省份出现总数的字典
    for mdi in map_dict:
        map_prodic[mdi]=map_province.count(mdi)
    print(map_prodic)
    # 通过循环将上述的字典拆分为两个列表，分别围殴map_attr,map_val,用于下面pyecharts绘制图形
    for province_key in map_prodic:
        map_attr.append(province_key)
        map_val.append(map_prodic[province_key])
    print(map_attr)
    print(map_val)
    # 开始绘制
    map = Map(my["NickName"]+"的微信好友位置分布图", width=1200, height=600,title_pos='center')
    map.add("", map_attr, map_val, is_visualmap=True,visual_range=[0,120],visual_text_color='#000', is_map_symbol_show=False, is_label_show=True)
    map.render()

plot_location(friends)

# 好友核心数据存储至Mysql
import pymysql.cursors
def save_mysql(friends):
    # 数据库链接，记得更换XXXX处为你的
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

# 使用就取消注释
# save_mysql(friends)
