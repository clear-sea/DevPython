# write by clear-sea
import ttkbootstrap as ttk
import tkinter as tk
from ttkbootstrap.dialogs import Messagebox
from tkinter import filedialog as fd
import sys,os
import Widgets
import docWidgets as doc

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
    global isFile_Opening,isFile_Saved,editor

    isFile_Saved=False
    isFile_Opening=True

    editor.text.pack(fill=tk.BOTH,anchor=tk.NW)

def openFile():
    # 打开文件
    global editor,fileName
    fileName=fd.askopenfilename(title="打开文件")

    if fileName!="": # 如果文件名不为空
        mainWindow.title(fileName+" -"+title)
        #context
        editor.readFile(fileName)
        editor.text.pack(fill=tk.BOTH,anchor=tk.NW)

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
    global editor,isFile_Opening

    if isFile_Opening:
        isFile_Opening=False
        # 删除文本框内容并隐藏它
        editor.text.delete(tk.INSERT,tk.END)
        editor.text.pack_forget()
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
        doc.Title(window,1,"DevPython")
        doc.Paragraph(window,"相当于Python3自带的IDEA++\n")
        doc.Title(window,1,"作者")
        doc.Paragraph(window,"\n作者：清澈的海水\n使用tkinter和ttkbootstrap写界面")
        doc.Link(window,"https://github.com/clear-sea/DevPython","GitHub项目地址")

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

        doc.Title(window,1,"快捷键")
        doc.Paragraph(window,"Ctrl+N:新建文件\nCtrl+S:保存文件\nCtrl+Shift+S:文件另存为\n")

def showSetting():
    pass

def run():
    result=os.popen("python "+fileName)
    print(result.read())
    result.close()

def debug():
    pass

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
mainMenuBar.add_cascade(label="文件",menu=fileMenu)
mainMenuBar.add_cascade(label="运行",menu=runMenu)
mainMenuBar.add_cascade(label="其他",menu=otherMenu)

mainWindow.config(menu=mainMenuBar)

#Main frame area
mainFrame=ttk.Frame(mainWindow,width=Width,height=Height)
mainFrame.pack(anchor=tk.NW,fill=tk.BOTH)
# 文本编辑框
editor=Widgets.Editor(mainFrame,mainFont,Width)
editor.text.pack_forget()
# shell shell=Widgets.Shell(mainFrame,Width)

# 绑定快捷键
editor.text.bind("<Control-KeyPress-s>",lambda event:editor.writeFile(fileName))
editor.text.bind("<Control-KeyPress-S>",lambda event:saveasFile())
editor.text.bind("<F11>",lambda event:run())
# editor.text.bind("<Key>",lambda event:mainWindow.title("*"+fileName+"- "+title))

mainWindow.bind("<Control-KeyPress-o>",lambda event:openFile())
mainWindow.bind("<Control-KeyPress-n>",lambda event:newFile())
# 终端参数
if len(sys.argv)>1:
    isFile_Opening=True
    #context
    editor.readFile(sys.argv[1])
    editor.text.pack(fill=tk.BOTH,anchor=tk.NW)

#mainloop
mainWindow.mainloop()
