# write by clear-sea
import ttkbootstrap as ttk
import tkinter as tk
from ttkbootstrap.dialogs import Messagebox
from tkinter import filedialog as fd
import sys,os
import Widgets
import doc

isFile_Opening=False # 记录是否有文件被打开
isFile_Saved=True # 记录文件是否保存
isHelpWindow_Opening=False # 记录帮助窗口是否已经被打开
isSettingWindow_Opening=False # 记录设置窗口是否已经被打开
isAboutWindow_opening=False # 记录关于窗口是否已经被打开

fileName="" # 记录打开的文件名
title="DevPython" # 窗口默认标题

mainWindow=mainFont=mainFrame=None

def newFile():
    # 创建新文件
    global isFile_Opening,isFile_Saved,editor,shell

    isFile_Saved=False
    isFile_Opening=True

    editor.text.pack(fill=tk.X,anchor=tk.NW,side=tk.TOP)
    shell.shell.pack(fill=tk.X,expand=True,side=tk.BOTTOM)

def openFile():
    # 打开文件
    global editor,fileName,editor,isFile_Opening
    fileName=fd.askopenfilename(title="打开文件")

    if fileName!="": # 如果文件名不为空
        isFile_Opening=True

        mainWindow.title(fileName+" -"+title)
        #context
        editor.readFile(fileName)
        editor.text.pack(fill=tk.X,anchor=tk.NW,side=tk.TOP)
        # shell
        shell.shell.pack(fill=tk.X,expand=True,side=tk.BOTTOM)

def openDir():
    # 打开目录
    dirName=fd.askdirectory(title="打开文件夹")
    pass

def saveasFile():
    # 另存为
    global editor,fileName,isFile_Opening

    if isFile_Opening:
        fileName=fd.asksaveasfilename(title="另存为")
        editor.writeFile(fileName)
        mainWindow.title(fileName+" -"+title)
    else:
        Messagebox.show_error("当前没有打开文件","错误")

def saveFile():
    # 保存
    global editor,fileName,isFile_Opening

    if isFile_Opening:
        editor.writeFile(fileName)
        mainWindow.title(fileName+" -"+title)
    else:
        Messagebox.show_error("当前没有打开文件","错误")

def closeFile():
    #关闭当前文本框
    global editor,isFile_Opening,shell

    if isFile_Opening:
        isFile_Opening=False
        # 删除文本框内容并隐藏它
        editor.text.delete(tk.INSERT,tk.END)
        editor.text.pack_forget()
        # 隐藏shell
        shell.shell.pack_forget()
    else:
        Messagebox.show_error("当前没有打开文件","错误")


def showAbout():
    # 显示关于信息
    global mainWindow,isAboutWindow_opening
    
    def on_close():
        global isAboutWindow_opening
        window.destroy()
        isAboutWindow_opening=False

    if isAboutWindow_opening==False:
        isAboutWindow_opening=True

        window=ttk.Toplevel(mainWindow)
        window.title("关于")

        window.protocol("WM_DELETE_WINDOW",on_close)

        document=doc.Document(window)
        document.insert(tk.INSERT,"DevPython\n","title")
        document.insert(tk.INSERT,"相当于Python3自带的IDEA++\n","p")
        document.insert(tk.INSERT,"关于\n","title")
        document.insert(tk.INSERT,"作者：清澈的海水\n使用tkinter和ttkbootstrap写界面\n","p")
        document.insert(tk.INSERT,"GitHub项目地址","link")
        document.links.append("https://github.com/clear-sea/DevPython")

        document.pack(fill="both",expand=True)
        document.config(state="disabled")

def showHelp():
    # 显示帮助信息
    global isHelpWindow_Opening

    def on_close():
        global isHelpWindow_Opening
        window.destroy()
        isHelpWindow_Opening=False

    if isHelpWindow_Opening==False:
        isHelpWindow_Opening=True
        window=ttk.Toplevel(mainWindow)
        window.title("帮助")

        window.protocol("WM_DELETE_WINDOW",on_close)

        docunment=doc.Document(window)
        docunment.insert(tk.INSERT,"快捷键\n","title")
        docunment.insert(tk.INSERT,"Ctrl+N:新建文件\nCtrl+S:保存文件\nCtrl+Shift+N:打开新窗口\nCtrl+Shift+S:文件另存为\nCtrl+O:打开文件\nF11:运行代码文件\n","p")

        docunment.pack(fill=tk.BOTH,expand=True)
        docunment.config(state="disabled")

def showSetting():
    pass

def run():
    # 运行文件
    global editor,fileName

    editor.writeFile(fileName) # 先保存文件
    result=os.popen("python "+fileName)
    print(result.read())
    result.close()

def debug():
    # 调试
    pass

def startNewWindow():
    # 启动新窗口
    ext=os.path.splitext(__file__)[-1]
    if ext==".pyw":
        os.system("python "+__file__) # 如果是以python源代码文件运行
    else:
        os.system("start "+__file__) # 如果打包成了可执行程序

def changeTitle(event):
    # 如果文件被更改，在窗口标题前加上"·"
    global mainWindow,editor,fileName
    if editor.haveChanged():
        mainWindow.title("·"+fileName+" -"+title)
# main
# 读取配置
with open("settings.json","r",encoding="utf-8") as setting_file:
    settings=eval(setting_file.read())

mainFont=(settings["text"]["text-font"],settings["text"]["text-size"]) # font
# 创建主窗口
Width,Height=800,600

mainWindow=ttk.Window(title=title,size=(Width,Height))
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

fileMenu.add_command(label="新建文件",command=newFile,accelerator="Ctrl+N")
fileMenu.add_separator()
fileMenu.add_command(label="打开文件",command=openFile,accelerator="Ctrl+O")
fileMenu.add_command(label="打开文件夹",command=openDir)
fileMenu.add_separator()
fileMenu.add_command(label="保存",command=saveFile,accelerator="Ctrl+S")
fileMenu.add_command(label="另存为",command=saveasFile,accelerator="Ctrl+Shift+S")
fileMenu.add_separator()
fileMenu.add_command(label="打开新窗口",command=startNewWindow,accelerator="Ctrl+Shift+N")
fileMenu.add_separator()
fileMenu.add_command(label="关闭文件",command=closeFile)
fileMenu.add_command(label="退出",command=quit)
# 运行菜单
runMenu=ttk.Menu(mainMenuBar,tearoff=0)
runMenu.add_command(label="运行",command=run)
fileMenu.add_separator()
runMenu.add_command(label="调试",state="disabled",command=debug)
# 帮助菜单
otherMenu=ttk.Menu(mainMenuBar,tearoff=0)
otherMenu.add_command(label="设置",command=showSetting)
otherMenu.add_separator()
otherMenu.add_command(label="帮助",command=showHelp)
otherMenu.add_separator()
otherMenu.add_command(label="关于",command=showAbout)
# 主菜单
mainMenuBar.add_cascade(label="文件(F)",menu=fileMenu)
mainMenuBar.add_cascade(label="运行(R)",menu=runMenu)
mainMenuBar.add_cascade(label="其他(O)",menu=otherMenu)

mainWindow.config(menu=mainMenuBar)

#主框
mainFrame=ttk.Frame(mainWindow,width=Width,height=Height)
mainFrame.pack(anchor=tk.NW,fill=tk.BOTH)
# 文本编辑框
editor=Widgets.Editor(mainFrame,mainFont,Width)
editor.text.pack_forget()
# shell
shell=Widgets.Shell(mainFrame,Width)
shell.shell.pack_forget()

# 绑定快捷键
editor.text.bind("<Control-KeyPress-s>",lambda event:editor.writeFile(fileName))
editor.text.bind("<Control-KeyPress-S>",lambda event:saveasFile())
editor.text.bind("<F11>",lambda event:run())
editor.text.bind("<Key>",changeTitle) # 如果文件被更改，在窗口标题前加上"·"

mainWindow.bind("<Control-KeyPress-o>",lambda event:openFile())
mainWindow.bind("<Control-KeyPress-n>",lambda event:newFile())
mainWindow.bind("<Control-KeyPress-N>",lambda event:startNewWindow())
# 终端参数
if len(sys.argv)>1:
    isFile_Opening=True
    #context
    editor.readFile(sys.argv[1])
    editor.text.pack(fill=tk.BOTH,anchor=tk.NW)

#mainloop
mainWindow.mainloop()
