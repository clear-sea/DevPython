import tkinter as tk
 
root = tk.Tk()
 
text = tk.Text(root, width=40, height=5)
text.pack()

text.tag_config("tag1", background="yellow", foreground="red")  # 旧的 Tag

# 注意，与下边的调用顺序没有关系
text.insert("insert", "I love Python.com!", "tag1")
    
root.mainloop()


