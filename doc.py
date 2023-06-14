from ttkbootstrap import ScrolledText
import webbrowser

titleFont=("微软雅黑",20,"bold") # 标题字体
pFont=("微软雅黑",10) # 段落字体
linkFont=("微软雅黑",10,"underline") # 超链接字体

class Document(ScrolledText):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.links=[] # 用于储存链接
        self.links_index=0

        self.tag_config("title",font=titleFont)
        self.tag_config("p",font=pFont)
        self.tag_config("link",font=linkFont,foreground="skyblue")

        # 超链接点击实现
        self.tag_bind("link", "<Enter>", lambda event:self.config(cursor="arrow"))
        self.tag_bind("link", "<Leave>", lambda event:self.config(cursor="xterm"))
        self.tag_bind("link", "<Button-1>", self.click)

    def click(self,event):
        webbrowser.open(self.links[self.links_index])
        self.links_index+=1