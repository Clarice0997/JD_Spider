from tkinter import *
from tkinter.ttk import *
import time
import threading
import multiprocessing
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import psutil
from PIL import Image, ImageTk
import pymongo
import jieba
import wordcloud


# 运行爬虫按钮点击事件
def runSpiderHandler(*args):
    try:
        # 获取需要爬取的商品名
        GoodName = searchGoodName.get()
        # 判断商品名是否为空
        if GoodName.strip() == '':
            print('商品名为空')
            return
        else:
            # 赋值
            lable_value.set('运行状态：运行中')
            print(f'爬取商品关键词：{GoodName}')
            # 指定爬虫程序
            scrapyProcess = multiprocessing.Process(target=startCrawl, args=(GoodName,))
            # 运行爬虫程序
            scrapyProcess.start()
            print(scrapyProcess.pid)
            # 循环线程
            while scrapyProcess.pid in psutil.pids():
                time.sleep(0.5)
            # 爬虫程序运行完毕，处理数据
            lable_value.set('运行状态：分析数据')
            time.sleep(2)
            # 运行绘制词云图函数
            drawWordle(GoodName)

    except ValueError as e:
        # 打印错误
        print("错误信息---" + str(e))
        lable_value.set('运行状态：爬取失败')
        pass


# 运行爬虫函数
def startCrawl(GoodName):
    # 获得爬虫设置
    process = CrawlerProcess(get_project_settings())
    # 指定爬虫程序
    process.crawl('jd_spider', GoodName)
    # 启动爬虫
    process.start()


# 绘制词云图函数
def drawWordle(GoodName):
    # MongoDB数据库配置
    host = 'localhost'
    port = 27017
    db_name = 'JDShop'
    # 连接MongoDB数据库
    client = pymongo.MongoClient(host=host, port=port)
    # 指定数据库和集合
    db = client[db_name]
    collection = db['Goods']

    # 定义变量
    maxCommentCount = 0
    queryModel = ''
    commentStr = ''

    # 查询最高评论数
    for item in collection.aggregate([{"$match": {"GoodName": GoodName}},{"$group": {"_id": "$GoodName", "maxComment": {"$max": "$Good_commentCount"}}}]):
        maxCommentCount = item['maxComment']

    # 查询最高评论数商品名
    for item in collection.find({"GoodName": GoodName,"Good_commentCount": maxCommentCount}).limit(1):
        queryModel = item['Good_name']

    # 根据最高评论数商品名查询评论数据
    for item in collection.find({"GoodName": GoodName,"Good_name": queryModel}).limit(3):
        commentStr = commentStr + item['Good_comment']

    # 中文分词
    ls = jieba.lcut(commentStr)
    text = ' '.join(ls)
    # 过滤词
    stopwords = ["的", "是", "了", "说", "和", "很", "就", "你", "也", "还", "就是", "还是", "而且", "可以", "非常","找", '更', "都", "等等", '按', '给']

    # 实例化词云
    wc = wordcloud.WordCloud(font_path="msyh.ttc", width=580, height=330, background_color='white', max_words=20,stopwords=stopwords)
    # 加载词云文本
    wc.generate(text)
    # 保存词云文件
    wc.to_file("词云图.png")  

    # 读取保存的词云图
    img_open = Image.open("词云图.png")
    # 生成ImageTK兼容的图片
    img_png = ImageTk.PhotoImage(img_open.resize((580, 330)))
    # 词云图Label
    Label(root_window, image=img_png).grid(row=2, column=0, columnspan=3, sticky=E)

    # 改变运行状态文本
    lable_value.set('运行状态：分析完毕')


# 函数线程守护 避免tkinter界面卡死
def thread_it(func, *args):
    # 打包函数进线程
    t = threading.Thread(target=func, args=args)
    # 守护线程
    t.daemon = True
    # 启动
    t.start()


# 初始化图形界面函数
def init_GUI():
    global root_window
    # 调用Tk()创建主窗口
    root_window = Tk()
    # 设置窗体居中显示
    SW = root_window.winfo_screenwidth()
    SH = root_window.winfo_screenheight()
    DW = 600
    DH = 400
    root_window.geometry("%dx%d+%d+%d" % (DW, DH, (SW - DW) / 2, (SH - DH) / 2))
    # 窗口标题
    root_window.title("京东爬虫")
    # 关闭窗口拉伸
    root_window.resizable(False, False)
    # 商品名输入框
    global searchGoodName, goodNameInput
    Label(root_window, text="请输入要爬取的商品名：", font=('微软雅黑', 12)).grid(row=0, column=0)
    searchGoodName = StringVar()
    goodNameInput = Entry(root_window, width=45, textvariable=searchGoodName).grid(row=0, column=1)
    # 爬虫按钮
    Button(root_window, width=10, text="爬取数据", command=lambda: thread_it(runSpiderHandler)).grid(row=0, column=2,sticky=E)

    # 处理状态
    global lable_value
    lable_value = StringVar()
    lable_value.set('运行状态：未启动')
    Label(root_window, textvariable=lable_value, font=('微软雅黑', 12)).grid(row=1, column=0, sticky=W)

    # 使窗口处于显示状态
    root_window.mainloop()


# 主函数
if __name__ == "__main__":
    init_GUI()
