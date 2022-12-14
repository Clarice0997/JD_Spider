from tkinter import *
from tkinter.ttk import *

# 调用Tk()创建主窗口
root_window = Tk()
# 设置窗体居中显示
SW = root_window.winfo_screenwidth()
SH = root_window.winfo_screenheight()
DW = 600
DH = 400
root_window.geometry("%dx%d+%d+%d" % (DW, DH, (SW - DW) / 2, (SH - DH) / 2))
# 窗口名
root_window.title("京东爬虫")
# 关闭窗口拉伸
root_window.resizable(False,False)

def runSpiderHandler(*args):
    try:
        # 获取需要爬取的商品名
        GoodName = searchGoodName.get()
        # 判断商品名是否为空
        if GoodName.strip() == '':
            print('商品名为空')
            # 赋值
            result.set(GoodName)
        else:
            print('商品名不为空')
    except ValueError:
        # 打印错误
        print(ValueError)
        pass

# 商品名输入框
goodNameLabel = Label(root_window, text="请输入要爬取的商品名：",font=('微软雅黑',12)).grid(row=0,column=0)
searchGoodName = StringVar()
goodNameInput = Entry(root_window, width=45, textvariable=searchGoodName).grid(row=0,column=1)
# 爬虫按钮
runSpider = Button(root_window,width=10, text="爬取数据",command=runSpiderHandler).grid(row=0,column=2,sticky=E)

# 结果
result = StringVar()
Label(root_window, textvariable=result).grid(row=1,column=0,sticky=W)

# 开启主循环，让窗口处于显示状态
root_window.mainloop()
