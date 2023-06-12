import tkinter as tk
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import *
import idlelib.colorizer as idc
import idlelib.percolator as idp

def PythonIDEA(title:str=...) -> None:
    """Return None,run python codes"""
    root = tk.Tk()
    root.title(str(title))
    root.geometry('1300x900')
    frame = tk.Frame(root)
    button = tk.Button(frame, text='Exit IDEA',bg='#252424',fg='white')
    button1 = tk.Button(frame, text='New file',bg='#252424',fg='white')
    button2 = tk.Button(frame, text='Open file',bg='#252424',fg='white')
    button3 = tk.Button(frame, text='Save file',bg='#252424',fg='white')
    button4 = tk.Button(frame, text=' ▶ ',bg='#252424',fg='#41cc32')
    button5 = tk.Button(frame, text='Clean python 3.10',bg='#252424',fg='white')
    button6 = tk.Button(frame, text=' ■ ', bg='#252424',fg='#f50000')
    button.pack(side=tk.LEFT)
    button1.pack(side=tk.LEFT)
    button2.pack(side=tk.LEFT)
    button3.pack(side=tk.LEFT)
    button4.pack(side=tk.LEFT)
    button6.pack(side=tk.LEFT)
    button5.pack(side=tk.RIGHT)
    frame.pack(side=tk.TOP, fill=tk.BOTH)
    global textPad
    textPad = ScrolledText(bg='#252424',fg='black',font=('黑体',16))
    textPad.pack(fill=tk.BOTH, expand=1)
    textPad.focus_set()
    global filename
    filename = 'hellow_world.py'
    def btnfunc01():
        global textPad, filename
        textPad.delete(1.0, tk.END)
        filename = 'hellow_world.py'
    def btnfunc02():
        global textPad, filename
        filename2 = askopenfilename(defaultextension='.py')
        if filename2 != '':
            textPad.delete(1.0, tk.END)
            f = open(filename2, 'r', encoding='utf-8', errors='ignore')
            textPad.insert(1.0, f.read())
            f.close()
            filename = filename2
    def btnfunc03():
        global textPad, filename
        filename = asksaveasfilename(initialfile=filename, defaultextension='.py')
        if filename != '':
            fh = open(filename, 'w', encoding='utf-8', errors='ignore')
            msg = textPad.get(1.0, tk.END)
            fh.write(msg)
            fh.close()
    button['command'] = lambda: root.destroy()
    button1['command'] = lambda: btnfunc01()
    button2['command'] = lambda: btnfunc02()
    button3['command'] = lambda: btnfunc03()
    frame2 = tk.LabelFrame(root, text='python 3.10', height=100)
    frame2.pack(fill=tk.BOTH, expand=1)
    global textMess
    textMess = ScrolledText(frame2, bg='#252424', height=10)
    textMess.pack(fill=tk.BOTH, expand=1)
    def clearMess():
        global textMess
        textMess.delete(1.0, tk.END)
    def colorprint(txt, color='black'):
        global textMess
        if textMess != None:
            if color != 'black':
                textMess.tag_config(color, foreground=color)
            textMess.insert(tk.END, txt, color)
            textMess.see(tk.END)
    def goto():
        global textPad, textMess
        try:
            msg = textPad.get(1.0, tk.END)
            mg = globals()
            ml = locals()
            exec(msg, mg, ml)
        except Exception as e:
            colorprint('\n'+str(e)+'\n','red')
    def key(event):
        goto()
    button4['command'] = lambda: goto()
    button5['command'] = lambda: clearMess()
    root.bind('<F11>',key)
    idc.color_config(textPad)
    textPad.focus_set()
    textPad.config(bg='white',fg='black')
    p = idp.Percolator(textPad)
    d = idc.ColorDelegator()
    p.insertfilter(d)
    root.mainloop()
    return None

# Pyt

