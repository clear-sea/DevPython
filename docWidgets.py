# 这个文件定义一些用于显示文档的控件
import ttkbootstrap as ttk
import tkinter as tk
import webbrowser

class Title:
    def __init__(self,parent,mode:int,context:str) -> None:
        self.font=("微软雅黑",23-mode)
        self.text=tk.Label(parent,text=context+'\n',font=self.font)
        self.text.pack(fill=tk.X)

class Paragraph:
    def __init__(self,parent,context) -> None:
        self.font=("微软雅黑",14)
        self.text=tk.Label(parent,text=context+'\n',font=self.font)
        self.text.pack(fill=tk.X)

class Link:
    def __init__(self,parent,link,context) -> None:
        self.font=("微软雅黑",14,"underline")
        self.text=tk.Label(parent,text=context+'\n',font=self.font,fg="skyblue")
        self.text.pack(side=tk.LEFT)
        self.text.bind("<Button-1>",lambda event:webbrowser.open(link))
        self.text.pack(fill=tk.X)