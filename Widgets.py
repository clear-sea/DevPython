'''这个文件定义了编辑器内用到的控件:Editor和Shell'''
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.scrolled import ScrolledText
import tkinter as tk
# 导入以下两个模块用于语法高亮
import idlelib.colorizer as idc
import idlelib.percolator as idp
# 导入sys和os
import sys,os

#Editor
class Editor:
    def __init__(self,parent,font,width,height=400):
        self.font=font
        self.parent=parent
        self.width=width
        self.height=height
        # 带有滚动条的文本框
        self.text=ScrolledText(parent,font=self.font,width=self.width,height=self.height,undo=True,autohide=True)
        self.text.pack(fill=tk.X,anchor=tk.NW,side=tk.TOP)

        # 文本内容
        self.context=self.text.get("1.0",tk.END)

        # 绑定弹出菜单的操作
        self.popupMenu=ttk.Menu(self.text,tearoff=False)
        self.popupMenu.add_command(label="剪切", command=self.cut,accelerator="Ctrl+X")
        self.popupMenu.add_command(label="复制", command=self.copy,accelerator="Ctrl+C")
        self.popupMenu.add_command(label="粘贴", command=self.paste,accelerator="Ctrl+V")
        self.popupMenu.add_separator()
        self.popupMenu.add_command(label="撤销", command=self.text.edit_undo,accelerator="Ctrl+Z")
        self.popupMenu.add_command(label="恢复", command=self.text.edit_redo,accelerator="Ctrl+Shift+Z")

        # 弹出菜单和绑定键盘事件
        self.text.bind("<Button-3>",self.popup)
        self.text.bind("<Control-KeyPress-z>",lambda event:self.text.edit_undo())
        self.text.bind("<Control-KeyPress-Z>",lambda event:self.text.edit_redo())

    def readFile(self,fileName):
        # 读取文件并将内容插入文本框
        self.clearAll()
        # 判断是否为代码文件
        ext=os.path.splitext(fileName)[-1] # 获取后缀名
        if ext in (".py",".pyw",".cpp",".h",".c",".hpp"):
            self.syntaxHighlighting() # 启用语法高亮
        elif ext not in (".py",".pyw",".cpp",".h",".c",".hpp",".txt",".json",".css",".html",".js"):
            Messagebox.show_warning("不能打开二进制文件","警告")
        # 试文件编码
        try: # 试试utf-8
            with open(fileName,"r",encoding="utf-8") as file:
                self.text.insert(tk.INSERT,file.read()) # 把文件内容插入到文本框
        except UnicodeDecodeError: # 再试试gbk
            with open(fileName,"r",encoding="gbk") as file:
                self.text.insert(tk.INSERT,file.read()) # 把文件内容插入到文本框
            
            try: # 再试试ansi
                with open(fileName,"r",encoding="ansi") as file:
                    self.text.insert(tk.INSERT,file.read()) # 把文件内容插入到文本框
            except: # 没辙了，显示错误
                Messagebox.show_error("文件编码错误","错误")

    def writeFile(self,fileName):
        # 写入文件
        context=self.text.get(1.0,tk.END) # 获取文本框所有内容

        with open(fileName,"w",encoding="utf-8") as file:
            file.write(context)

    def clearAll(self):
        self.text.delete(1.0,tk.END)

    def syntaxHighlighting(self):
        # 语法高亮
        p = idp.Percolator(self.text)
        d = idc.ColorDelegator()
        p.insertfilter(d)

    # 定义三个编辑操作
    def copy(self):
        self.text.event_generate("<<Copy>>")
    def cut(self):
        self.text.event_generate("<<Cut>>")
    def paste(self):
        self.text.event_generate("<<Paste>>")

    def popup(self,event):
        self.popupMenu.post(event.x_root,event.y_root)

    def haveChanged(self):
        newContext=self.text.get(1.0,tk.END)
        if newContext!=self.context:
            self.context=newContext
            return True
        else:
            return False

class Shell:
    def __init__(self,parent,width,height=200):
        self.parent=parent
        self.width=width
        self.height=height

        self.shell=tk.Text(self.parent,bg="black",fg="white",height=150)
        self.shell.pack(fill=tk.X,expand=True,side=tk.BOTTOM)
        self.shell.bind("<Return>",self.execute(self.shell.get(tk.INSERT,tk.END)))

    def execute(self,cmd):
        self.shell.insert(tk.INSERT,cmd+'\n')
        result=os.popen(cmd)
        self.shell.insert(tk.INSERT,result.read()+'\n')
        result.close()