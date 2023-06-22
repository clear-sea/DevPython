import ttkbootstrap as ttk
from ttkbootstrap.constants import *
root = ttk.Window(size=(500,200))
f = ttk.Frame(root).pack(fill=BOTH, expand=YES)
text_content = '''
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
'''

##滚动文本框
from ttkbootstrap.scrolled import ScrolledText
st = ScrolledText(f, padding=5, height=10, autohide=True)
st.pack(fill=BOTH, expand=YES)
st.insert(END, text_content)

root.mainloop()


