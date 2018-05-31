# Python3.6+pyecharts实现微信好友的数据分析
![](http://p20tr36iw.bkt.clouddn.com/wordcloud.png)
## 相关库学习

### 1.itchat安装及使用
```python
# 安装
pip install itchat
# 通过如下命令登陆，即使程序关闭，一定时间内重新开启也可以不用重新扫码。该方法会生成一个静态文件 itchat.pkl ，用于存储登陆的状态
itchat.auto_login(hotReload=True)
# 导出设置
itchat.dump_login_status()

```

### 2.pandas安装及使用

```python
# 安装
pip install pandas
```

#### 2.1DataFrame使用

```python
# DataFrame使用
DataFrame 是一个表格型的数据结构。它提供有序的列和不同类型的列值。
input:
import pandas as pd
a=pd.DataFrame()
output:
Empty DataFrame
Columns: []
Index: []
# key为列，value为值
input:
data=[{'name':'a','id':1},{'name':'b','id':2}]
da=pd.DataFrame(data)
da
output:
   id name
0   1    a
1   2    b
# columns可以指定列顺序，如果加入的列没有，则数据显示为NaN
input:
da=pd.DataFrame(data,columns=['id','name','test'])
da
output:
   id name  test
0   1    a   NaN
1   2    b   NaN
# DataFrame支持以字典索引的方式获取数据，还可以以属性的方法获取
input:
da['id']
output:
0    1
1    2
Name: id, dtype: int64
input:
da.name
output:
0    a
1    b
Name: name, dtype: object
# 取多列
input:
da[['id','name']]
output:
   id name
0   1    a
1   2    b
# 修改列的值：
input:
da.name='c'
da
output:
   id name  test
0   1    c   NaN
1   2    c   NaN
# 修改行的值:
input:
da[:1]=5
da
output:
   id name  test
0   5    5   5.0
1   2    c   NaN
# 修改某一具体数据
input:
da['name'][1]=8
output:
SettingWithCopyWarning:
A value is trying to be set on a copy of a slice from a DataFrame
input:
da
output:
id name  test
0   5    5   5.0
1   2    8   NaN
# 虽然上述报错了，会发现结果正如我们想要的修改了相应的值，针对报错问题解决办法采用了loc
input:
da.loc[1,'name']=10
output:
id  name  test
0   5     5   5.0
1   2    10   NaN
# 删除某一列:
input:
del da['test']
da
output:
   id  name
0   5     5
1   2    10
```

#### 2.2Series使用

```python
# Series是一个一维数组对象，类似与Numpy，但又不同，Series为一个带索引的一维数组对象,将 Python 数组转换成 Series 对象
# numpy的array操作
import numpy as np
input:
np.array([1,2,3])
output:
array([1, 2, 3])
# Series操作
input:
pd.Series(['12','as'])
output:
0    12
1    as
dtype: object
# Series，先来熟悉一下DataFrame
input:
pd.DataFrame([1,2,3],index=['a','b','c'],columns=['number'])
output:
   number
a       1
b       2
c       3
# 而Series操作同上，默认index从0计数,但没有columns，不能指定列名
input:
pd.Series([121,22,32],index=[1,2,3])
output:
1    121
2     22
3     32
dtype: int64
# 取值
input:
sr[1]
output:
121
# 取多个值
input:
sr[[1,2]]
output:
1    121
2     22
dtype: int64
# 修改
input:
sr[1]=86
sr
output:
1    86
2    22
3    32
dtype: int64
# 单独获取 Series 对象的索引或者数组内容的时候，可以使用 index 和 values 属性
input:
sr.index
output:
Int64Index([1, 2, 3], dtype='int64')
input:
sr.values
output:
array([86, 22, 32], dtype=int64)
# 对Series对象运算---只改变值，不改变索引,并且sr整体也不变，只是获得一个临时对象来存储sr*2
input:
sr*2
output:
1    172
2     44
3     64
dtype: int64
input:
sr
output:
1    86
2    22
3    32
# 索引出小于60的数据
input:
sr[sr<=60]
output:
2    22
3    32
dtype: int64
```
### 3.PIL、matplotlib、WordCloud(深入学习见后篇)

```python
# Python Imaging Library，图像处理标准库，打开一个jpg图像文件
# 打开图片
import PIL.Image as Image
coloring=Image.open("D:/pachong/weixin/qqq.jpg")



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
```
### 4.项目Demo功能详解
```python
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
```

### 5.相关问题

>pyecharts绘图中地图无法显示问题

```
# echarts-countries-pypkg 是全球国家地图
pip install echarts-countries-pypkg
# echarts-china-provinces-pypkg是中国省级地图
pip install echarts-china-provinces-pypkg
# echarts-china-cities-pypkg是中国城市地图
pip install echarts-china-cities-pypkg
```

### 6.参考文章
[1.Python - pandas DataFrame 数据选取，修改，切片](https://blog.csdn.net/yoonhee/article/details/76168253)

[2.pandas DataFrame中经常出现SettingWithCopyWarning](
http://sofasofa.io/forum_main_post.php?postid=1001449)

[3.Numpy 的创建 array](
https://morvanzhou.github.io/tutorials/data-manipulation/np-pd/2-2-np-array/)

[4.利用Python进行数据分析(7) pandas基础: Series和DataFrame的简单介绍](https://www.cnblogs.com/sirkevin/p/5741853.html
)

[5.利用python进行微信好友数据分析](https://blog.csdn.net/xxzj_zz2017/article/details/79463984)

[6.解决pyecharts绘图中地图无法显示问题(亲自试验，绝对有效)](https://blog.csdn.net/xiamoyanyulrq/article/details/80025105)

[7.用 Python 制作微信好友个性签名词云图](https://www.jianshu.com/p/ea11eac3d2ad?utm_campaign=maleskine&utm_content=note&utm_medium=seo_notes&utm_source=recommendation)

[8.wordcloud安装](https://blog.csdn.net/u012942818/article/details/75144001)

### 7.欢迎Start:[My Project Here](https://github.com/Light-City/weixinAnalysis)
