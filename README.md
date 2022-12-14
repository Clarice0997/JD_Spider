# 京东商城爬虫

![](https://img.shields.io/badge/Python-3.11-green.svg)

#### 京东官网 - <https://www.jd.com>

## 需求

设计一个**图形界面**，可以**输入一个商品名称**，从京东商城上抓取搜索到的商品信息（**至少包括商品标题、详情页url、品牌、店铺名称、商品名称、商品评价数、评价的文本**），并**保存**到MongoDB数据库或redis数据库中，能展示**评价数最高**且**商品名称相同**的前3个商品的评价词云图。

## 需求分析

1. 设计图形界面，可以使用 **tkinter** 进行图形化界面设计
2. 用户可以输入商品名称，图形化界面中需要输入框和按钮用于实现此功能，输入框获得商品名称，按钮点击运行爬虫
3. 需要获得数据至少包括（**商品标题、详情页url、品牌、店铺名称、商品名称、商品评价数、评价的文本**），这些数据需要分别从商品搜索页和商品详细页进行爬取，其中部分数据需要进行特殊处理才能取得

    - 详细页url：网站中的url并不完整，需要进行urljoin拼接才能获得完整url（//item.jd.com/13836773522.html）
    - 商品名称：商品名称和商品标题不能一概而论，商品名称在商品详细页，需要下滑后动态加载
    - 品牌：商品详细页，需要下滑后动态加载
    - 评价文本：商品详细页，点击商品评价按钮后动态加载，存在分页，一页10条数据

4. 保存数据到**MongoDB或者Redis**，在 **pipelines** 中进行以上操作
5. 展示评论数最高的，名称相同的三个商品的评价词云图，包含俩个条件：1.评价数最高；2.商品名称（**型号**）相同 使用 **wordcloud** 生成词云图

## 数据结构设计

### 爬取字段数据结构

| 字段名 | 数据类型 | 字段描述 |
| ----- | ----- | ----- |
| GoodName | Numbers | 爬取商品名 |
| Good_id | Numbers | 商品ID |
| Good_title | String | 商品标题 |
| Good_price | Numbers | 商品价格 |
| Good_url | String | 商品url |
| Good_brand | String | 商品品牌 |
| Good_shopName | String | 店铺名 |
| Good_name | String | 商品名称 |
| Good_commentCount | Numbers | 商品评论数 |
| Good_comment | List | 商品评价文本 |

### 程序数据结构

| 字段名 | 数据类型 | 字段描述 |
| ----- | ----- | ----- |
| GoodName | String | 爬取商品名 |
| lable_value | String | 爬虫状态文本 |
| host | String | MongoDB IP |
| port | Numbers | MongoDB 端口 |
| db_name | String | 数据库名 |
| maxCommentCount | Numbers | 最高评论条数 |
| queryModel | String | 最高评论商品名 |
| commentStr | String | 最高评论评论字符串 |
| text | String | 评论分词处理后字符串 |
| stopwords | List | 词云过滤词集合 |
| USER_AGENTS | List | 随机请求头列表 |
| url | String | 发起请求的网址 |
| js | Dict | 解析json结果 |

## 模块设计

### 爬虫模块

1. 配置Scrapy框架运行环境，配置变量
2. 设置随机请求头中间件、搜索页随机下滑中间件
3. 运行爬虫程序
4. 爬取搜索页商品基本信息
5. 根据商品ID构建商品详细页URL
6. 解析商品详细页json获得品牌名和商品型号
7. 根据商品ID构建商品评论页URL
8. 解析商品详细页json获得商品评论和评论数
9. 构建Item 传递pipelines
10. pipelines存入MongoDB

### 图形界面模块

1. 通过tkinter制作GUI界面，通过输入框获得爬取商品名，将商品名传入爬虫模块，运行爬虫程序
2. 运行词云模块
3. 将生成的词云图展示在GUI界面

### 词云模块

1. 爬虫程序运行完成后，连接MongoDB数据库
2. 通过嵌套查询获得评论数最高的，名称相同的三个商品的评价文本
3. 对评论文本进行预处理，进行分词操作，删除其中的语气词和虚词
4. 生成词云图保存图片
