import ttkbootstrap as ttk
import tkinter as tk
from ttkbootstrap.dialogs import Messagebox
from tkinter import filedialog as fd
import sys
import os
import Editor

isFile_Opening=False # 记录是否有文件被打开。如果有，下面用notebook实现多页；如果没有，下面不显示文本框

def readFile(fileName):
    # 读取文件
    try:
        with open(fileName,"r",encoding="utf-8") as file:
            context=file.read()
    except UnicodeDecodeError:
        with open(fileName,"r",encoding="gbk") as file:
            context=file.read()
    return context

def writeFile(fileName,context):
    # 写入文件
    with open(fileName,"w",encoding="utf-8") as file:
        file.write(context)

def openFile():
    # 打开文件
    global pages,isFile_Opening
    fileName=fd.askopenfilename(title="打开文件")
    

    if fileName!="":
        isFile_Opening=True

        pages.pack(fill=tk.BOTH,side=tk.LEFT,anchor=tk.NW)

        editor=ttk.Text(mainFrame,width=Width,height=Height,font=mainFont)
        pages.add(text=os.path.basename(fileName),child=editor)
        #context
        context=readFile(fileName)
        editor.insert("insert",context)

def openDir():
    # 打开目录
    dirName=fd.askdirectory(title="打开文件夹")

def saveasFile():
    # 另存为
    fileName=fd.asksaveasfilename(title="另存为")
    pass

def saveFile():
    # 保存
    pass

def showAbout():
    # 显示关于信息
    Messagebox.show_info("关于DevPython\n作者：清澈的海水\n使用ttkbootstrap写界面\nGitHub项目地址:https://github.com/clear-sea/DevPython","关于")

def showHelp():
    # 显示帮助信息
    Messagebox.show_info("这里是帮助","帮助")

def run():
    pass

def debug():
    pass

# main
if __name__=="__main__":
    # 读取配置
    with open("settings.json","r",encoding="utf-8") as setting_file:
        settings=eval(setting_file.read())

    mainFont=(settings["text"]["text-font"],settings["text"]["text-size"]) # font
    # 创建主窗口
    Width,Height=800,600

    mainWindow=ttk.Window(title="Python Editor",size=(Width,Height))
    mainWindow.iconbitmap("images/icon.ico")
    
    screenWidth=mainWindow.winfo_screenwidth() # screen width
    screenHeight=mainWindow.winfo_screenheight() # screen height

    posX=int((screenWidth-Width)/2)
    posY=int((screenHeight-Height)/2)

    mainWindow.geometry(f"+{posX}+{posY}")
    # 菜单
    mainMenuBar=ttk.Menu(mainWindow) # 主菜单
    # 文件菜单
    fileMenu=ttk.Menu(mainMenuBar,tearoff=0)
    fileMenu.add_command(label="打开文件",command=openFile)
    fileMenu.add_command(label="打开文件夹",command=openDir)
    fileMenu.add_command(label="保存",command=saveFile)
    fileMenu.add_command(label="另存为",command=saveasFile)
    fileMenu.add_separator()
    fileMenu.add_command(label="关闭",command=quit)
    # 运行菜单
    runMenu=ttk.Menu(mainMenuBar,tearoff=0)
    runMenu.add_command(label="运行",command=run)
    runMenu.add_command(label="调试",state="disabled",command=debug)
    # 帮助菜单
    helpMenu=ttk.Menu(mainMenuBar,tearoff=0)
    helpMenu.add_command(label="帮助",command=showHelp)
    helpMenu.add_separator()
    helpMenu.add_command(label="关于",command=showAbout)
    # 主菜单
    mainMenuBar.add_cascade(label="文件",menu=fileMenu)
    mainMenuBar.add_cascade(label="运行",menu=runMenu)
    mainMenuBar.add_cascade(label="帮助",menu=helpMenu)
    mainWindow.config(menu=mainMenuBar)

    #Main frame area
    mainFrame=ttk.Frame(mainWindow,width=Width,height=Height-20)
    mainFrame.pack(anchor=tk.NW,fill=tk.X)
    # 分页
    pages=ttk.Notebook(mainFrame,width=Width,height=Height)
    # 终端参数
    if len(sys.argv)>1:
        isFile_Opening=True

        pages.pack(fill=tk.BOTH,side=tk.LEFT,anchor=tk.NW)

        editor=ttk.Text(mainFrame,width=Width,height=Height,font=mainFont)
        pages.add(text=os.path.basename(sys.argv[1]),child=editor)
        #context
        context=readFile(sys.argv[1])
        editor.insert("insert",context)
    #mainloop
    mainWindow.mainloop()