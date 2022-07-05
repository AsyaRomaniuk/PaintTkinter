from tkinter.messagebox import askokcancel
from tkinter.filedialog import *
from tkinter.colorchooser import *
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from tkcolorpicker import askcolor
from functools import partial
from belfrywidgets import ToolTip


# http://www.ilnurgi1.ru/docs/python/modules/tkinter/canvas.html
def PASS(event=None):
    pass


text = None
star = None
rtrian = None
trian = None
ell = None
rect = None
line = None
draw = None
point = None
item = None

sz = 4
sz2 = 4
cl = "black"
bgcl = "white"
ft = ".keyboard"
penactfill = "red"
theme = "tk"
cursor = "arrow"
gridA = 50
ftsz = 8
fs = 8
cx = 0
cy = 0
prx = 0
pry = 0
ComponentsAreHidden = False
ButtonColorsAreOpen = False
DrawingIs = False
GridIs = False
PointIs = False
FillIs = False
FullScreenedIs = False
EnteringIs = False
BtnClList = ["black", "red", "blue", "white", "yellow",
             "green", "lime", "aqua", "purple", "brown",
             "cyan", "grey", "gray", "snow", "pink",
             "magenta", "orange", "lightgreen", "grey20",
             "darkblue", "lightblue", "gold", "silver",
             "chocolate", "lightpink", "hotpink", "navy",
             "olive", "azure", "violet"]
GridItems = []
CanvasItems = []

"""
def greet_all(names: list[str]) -> None: 
    for name in names: 
        print("Hello", name) 
"""


class Modal(Toplevel):

    def SetCursor(self):
        global cursor
        cursor = self.cb["values"][self.cb.current()]
        self.btn.config(cursor=cursor)

    def SetTheme(self):
        global theme
        theme = self.cb["values"][self.cb.current()]
        MAIN.config(theme=theme)

    def SetFont(self):
        global ft
        ft = self.cb["values"][self.cb.current()]
        textvar.config(text=ft, font=(ft, 14))
        textvar.pack(padx=20, fill="x")

    def __init__(self):
        pass

    def CancelTheme(self):
        MAIN.config(theme=self.th)
        self.destroy()

    def CancelCursor(self):
        global cursor
        cursor = self.var
        self.destroy()

    def CancelFont(self):
        global ft
        ft = self.var
        textvar.forget()
        self.destroy()

    def GetAndExit(self):
        global cursor
        cursor = self.cb["values"][self.cb.current()]
        C.config(cursor=self.cb["values"][self.cb.current()])
        self.destroy()

    def GetAndExit2(self):
        global theme
        theme = self.cb["values"][self.cb.current()]
        MAIN.config(theme=self.cb["values"][self.cb.current()])
        self.destroy()

    def GetAndExit3(self):
        global ft
        ft = self.cb["values"][self.cb.current()]
        textvar.forget()
        self.destroy()

    def Create(self, cbval, frametext, list, func, func2, func3):
        self.th = MAIN["theme"]
        self.var = cbval
        Toplevel.__init__(self, MAIN)
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", func3)
        self.transient(MAIN)
        self.title(frametext)
        self.grab_set()
        self.lf = ttk.LabelFrame(self, text=frametext)
        self.cb = ttk.Combobox(self.lf, values=list)
        self.cb.set(cbval)
        self.cb.pack(side=LEFT, padx=8, pady=4)
        self.btn = ttk.Button(self.lf, text="Set", command=func)
        self.btn.pack(side=RIGHT, padx=8, pady=4)
        self.fr = ttk.Frame(self)
        self.lbtn = ttk.Button(self.fr, text="OK", command=func2)
        self.lbtn.pack(side=LEFT, padx=10, pady=4)
        self.rbtn = ttk.Button(self.fr, text="Cancel", command=func3)
        self.rbtn.pack(side=RIGHT, padx=10, pady=4)
        self.fr.pack(side=BOTTOM, fill="x")
        self.lf.pack(padx=10, pady=6)
        self.mainloop()


class Text():
    """Draws text"""

    def __init__(self):
        self.rectangle = None
        self.text = None
        self.moving = False
        self.click = False
        self.x = 0
        self.y = 0
        self.xe = 0
        self.ye = 0

    def Config(self, **kwargs):
        C.itemconfig(self.text, kwargs)

    def coords(self, x, y):
        global ft
        self.xe, self.ye = x, y
        C.itemconfig(self.text, font=(ft, int((y - self.y) / 2)))
        C.coords(self.rectangle, self.x, self.y, x, y)
        C.coords(self.text, self.x + (x - self.x) / 2, self.y + (y - self.y) / 2)

    def PlaceEntry(self, event):
        global EnteringIs
        EnteringIs = True
        self.ent.config(state="normal")
        self.ent.place(x=self.x + (self.xe - self.x) / 2,
                       y=self.y + (self.ye - self.y) / 2)

    def UnplaceEntry(self, event):
        global EnteringIs
        EnteringIs = False
        self.ent.config(state="disabled")
        self.ent.place_forget()

    def Pressed(self, event):
        global prx, pry
        C.bind("<B1-Motion>", PASS)
        C.config(cursor="fleur")
        C.itemconfig(self.text, fill="grey", activefill="grey")
        prx, pry = event.x, event.y

    def Moving(self, event):
        global prx, pry
        C.move(self.text, event.x - prx, event.y - pry)
        prx, pry = event.x, event.y

    def Released(self, event):
        global cursor
        if not self.click:
            self.click = True
            C.tag_bind(self.text, "<B1-Motion>", self.Moving)
        else:
            self.click = False
            C.config(cursor=cursor)
            C.itemconfig(self.text, fill=self.color, activefill=self.activefill)
            C.tag_unbind(self.text, "<B1-Motion>")
            ComboboxChanged()

    def Kill(self):
        global cursor, EnteringIs
        EnteringIs = False
        self.ent.destroy()
        C.delete(self.text)
        if self.click:
            C.config(cursor=cursor)
            ComboboxChanged()
        del self

    def Create(self, coords, color, actfill, textfont):
        global FillIs
        self.x, self.y = coords
        self.activefill = actfill
        self.color = color
        self.ent = ttk.Entry(C, font=14)
        self.ent.bind("<Enter>", self.PlaceEntry)
        self.ent.bind("<Return>", lambda e: C.itemconfig(self.text, text=self.ent.get()))
        self.rectangle = C.create_rectangle(self.x, self.y, self.x, self.y, dash=(7, 1, 1, 1), outline="grey")
        self.text = C.create_text(self.x, self.y, text="Text", activefill=actfill, fill="grey", font=textfont)
        C.tag_bind(self.text, "<Enter>", self.PlaceEntry)
        C.tag_bind(self.text, "<Leave>", self.UnplaceEntry)
        C.tag_bind(self.text, "<Button-2>", lambda e: self.Kill())
        C.tag_bind(self.text, "<ButtonPress-1>", self.Pressed)
        C.tag_bind(self.text, "<ButtonRelease-1>", self.Released)


'''class Figure():
    """Parent of vector figures"""
    def __init__(self):
        self.figure = None
        self.moving = False
        self.click = False
        self.xb = 0
        self.yb = 0

    def Config(self, **kwargs):
        C.itemconfig(self.figure, kwargs)

    def DeleteRectangle(self):
        C.delete(self.rectangle)

    def Pressed(self, event):
        global prx, pry
        C.bind("<B1-Motion>", PASS)
        C.config(cursor="fleur")
        C.itemconfig(self.figure, outline="grey", activeoutline="grey")
        prx, pry = event.x, event.y

    def Moving(self, event):
        global prx, pry
        C.move(self.figure, event.x - prx, event.y - pry)
        prx, pry = event.x, event.y

    def Released(self, event):
        global cursor
        if not self.click:
            self.click = True
            C.tag_bind(self.figure, "<B1-Motion>", self.Moving)
        else:
            self.click = False
            C.config(cursor=cursor)
            C.itemconfig(self.figure, outline=self.color, activeoutline=self.activefill)
            C.tag_unbind(self.figure, "<B1-Motion>")
            ComboboxChanged()

    def Kill(self, event):
        global cursor
        C.delete(self.figure)
        if self.click:
            C.config(cursor=cursor)
            ComboboxChanged()
        del self

    def Active(self, event, state=True):
        global cursor
        if state:
            C.config(cursor="hand2")
        else:
            C.config(cursor=cursor)

    def BindFigure(self):
        C.tag_bind(self.figure, "<Button-2>", self.Kill)
        C.tag_bind(self.figure, "<ButtonPress-1>", self.Pressed)
        C.tag_bind(self.figure, "<ButtonRelease-1>", self.Released)
        C.tag_bind(self.figure, "<Enter>", lambda e: self.Active(e, True))
        C.tag_bind(self.figure, "<Leave>", lambda e: self.Active(e, False))

    def Create(self, coords, color, actfill, width):
        self.xb, self.yb = coords
        self.activefill = actfill
        self.color = color
        self.rectangle = C.create_rectangle(self.xb, self.yb, self.xb, self.yb, dash=(7, 1, 1, 1), outline="grey")
        self.figure = C.create_line((self.xb, self.yb), (self.xb, self.yb), activefill=actfill, dash=(7, 1, 1, 1),
                                    width=width, activedash=(7, 1, 1, 1), fill="grey")
        self.BindFigure()


class Line(Figure):
    def __init__(self, type):
        Figure.__init__(self)
        self.type = type

    def coords(self, x, y):
        C.coords(self.rectangle, self.xb, self.yb, x, y)
        C.coords(self.figure, self.xb, self.yb, x, y)'''


class Star():
    """Draws vector star"""

    def __init__(self):
        self.rectangle = None
        self.star = None
        self.moving = False
        self.click = False
        self.xb = 0
        self.yb = 0

    def Config(self, **kwargs):
        C.itemconfig(self.star, kwargs)

    def coords(self, xe, ye):
        global sz2
        xside, yside = xe - self.xb, ye - self.yb
        xcen, ycen = self.xb + xside / 2, self.yb + yside / 2
        C.coords(self.rectangle, self.xb, self.yb, xe, ye)
        C.coords(self.star,
                 xcen, self.yb,
                 xcen + xside * sz2 / 100, ycen - yside * sz2 / 100,
                 xe, ycen,
                 xcen + xside * sz2 / 100, ycen + yside * sz2 / 100,
                 xcen, ye,
                 xcen - xside * sz2 / 100, ycen + yside * sz2 / 100,
                 self.xb, ycen,
                 xcen - xside * sz2 / 100, ycen - yside * sz2 / 100)

    def Pressed(self, event):
        global prx, pry
        C.bind("<B1-Motion>", PASS)
        C.config(cursor="fleur")
        C.itemconfig(self.star, outline="grey", activeoutline="grey")
        prx, pry = event.x, event.y

    def Moving(self, event):
        global prx, pry
        C.move(self.star, event.x - prx, event.y - pry)
        prx, pry = event.x, event.y

    def Released(self, event):
        global cursor
        if not self.click:
            self.click = True
            C.tag_bind(self.star, "<B1-Motion>", self.Moving)
        else:
            self.click = False
            C.config(cursor=cursor)
            C.itemconfig(self.star, outline=self.color, activeoutline=self.activefill)
            C.tag_unbind(self.star, "<B1-Motion>")
            ComboboxChanged()

    def Kill(self):
        global cursor
        C.delete(self.star)
        if self.click:
            C.config(cursor=cursor)
            ComboboxChanged()
        del self

    def Create(self, coords, color, actfill, width):
        global FillIs, CanvasItems
        self.xb, self.yb = coords
        self.activefill = actfill
        self.color = color
        self.rectangle = C.create_rectangle(self.xb, self.yb, self.xb, self.yb, dash=(7, 1, 1, 1), outline="grey")
        self.star = C.create_polygon((self.xb, self.yb), (self.xb, self.yb), (self.xb, self.yb), (self.xb, self.yb),
                                     (self.xb, self.yb), (self.xb, self.yb), (self.xb, self.yb), (self.xb, self.yb),
                                     activeoutline=actfill, width=width, activedash=(7, 1, 1, 1), outline="grey",
                                     fill="", dash=(7, 1, 1, 1))
        C.tag_bind(self.star, "<Button-2>", lambda e: self.Kill())
        C.tag_bind(self.star, "<ButtonPress-1>", self.Pressed)
        C.tag_bind(self.star, "<ButtonRelease-1>", self.Released)


class RightTriangle():
    """Draws vector right triangle"""

    def __init__(self):
        self.rectangle = None
        self.righttriangle = None
        self.moving = False
        self.click = False
        self.xb = 0
        self.yb = 0

    def Config(self, **kwargs):
        C.itemconfig(self.righttriangle, kwargs)

    def coords(self, xe, ye):
        C.coords(self.rectangle, self.xb, self.yb, xe, ye)
        C.coords(self.righttriangle,
                 self.xb, self.yb,
                 self.xb, ye,
                 xe, ye)

    def Pressed(self, event):
        global prx, pry
        C.bind("<B1-Motion>", PASS)
        C.config(cursor="fleur")
        C.itemconfig(self.righttriangle, outline="grey", activeoutline="grey")
        prx, pry = event.x, event.y

    def Moving(self, event):
        global prx, pry
        C.move(self.righttriangle, event.x - prx, event.y - pry)
        prx, pry = event.x, event.y

    def Released(self, event):
        global cursor
        if not self.click:
            self.click = True
            C.tag_bind(self.righttriangle, "<B1-Motion>", self.Moving)
        else:
            self.click = False
            C.config(cursor=cursor)
            C.itemconfig(self.righttriangle, outline=self.color, activeoutline=self.activefill)
            C.tag_unbind(self.righttriangle, "<B1-Motion>")
            ComboboxChanged()

    def Kill(self):
        global cursor
        C.delete(self.righttriangle)
        if self.click:
            C.config(cursor=cursor)
            ComboboxChanged()
        del self

    def Create(self, coords, color, actfill, width):
        global FillIs
        self.xb, self.yb = coords
        self.activefill = actfill
        self.color = color
        self.rectangle = C.create_rectangle(self.xb, self.yb, self.xb, self.yb, dash=(7, 1, 1, 1), outline="grey")
        self.righttriangle = C.create_polygon((self.xb, self.yb), (self.xb, self.yb), (self.xb, self.yb),
                                              activeoutline=actfill, width=width, activedash=(7, 1, 1, 1),
                                              outline="grey", fill="", dash=(7, 1, 1, 1))
        C.tag_bind(self.righttriangle, "<Button-2>", lambda e: self.Kill())
        C.tag_bind(self.righttriangle, "<ButtonPress-1>", self.Pressed)
        C.tag_bind(self.righttriangle, "<ButtonRelease-1>", self.Released)


class Triangle():
    """Draws vector triangle"""

    def __init__(self):
        self.rectangle = None
        self.triangle = None
        self.moving = False
        self.click = False
        self.xb = 0
        self.yb = 0

    def Config(self, **kwargs):
        C.itemconfig(self.triangle, kwargs)

    def coords(self, xe, ye):
        xcen = self.xb + (xe - self.xb) / 2
        C.coords(self.rectangle, self.xb, self.yb, xe, ye)
        C.coords(self.triangle,
                 xcen, self.yb,
                 xe, ye,
                 self.xb, ye)

    def Pressed(self, event):
        global prx, pry
        C.bind("<B1-Motion>", PASS)
        C.config(cursor="fleur")
        C.itemconfig(self.triangle, outline="grey", activeoutline="grey")
        prx, pry = event.x, event.y

    def Moving(self, event):
        global prx, pry
        C.move(self.triangle, event.x - prx, event.y - pry)
        prx, pry = event.x, event.y

    def Released(self, event):
        global cursor
        if not self.click:
            self.click = True
            C.tag_bind(self.triangle, "<B1-Motion>", self.Moving)
        else:
            self.click = False
            C.config(cursor=cursor)
            C.itemconfig(self.triangle, outline=self.color, activeoutline=self.activefill)
            C.tag_unbind(self.triangle, "<B1-Motion>")
            ComboboxChanged()

    def Kill(self):
        global cursor
        C.delete(self.triangle)
        if self.click:
            C.config(cursor=cursor)
            ComboboxChanged()
        del self

    def Create(self, coords, color, actfill, width):
        global FillIs
        self.xb, self.yb = coords
        self.activefill = actfill
        self.color = color
        self.rectangle = C.create_rectangle(self.xb, self.yb, self.xb, self.yb, dash=(7, 1, 1, 1), outline="grey")
        self.triangle = C.create_polygon((self.xb, self.yb), (self.xb, self.yb), (self.xb, self.yb),
                                         activeoutline=actfill, width=width, activedash=(7, 1, 1, 1), outline="grey",
                                         fill="", dash=(7, 1, 1, 1))
        C.tag_bind(self.triangle, "<Button-2>", lambda e: self.Kill())
        C.tag_bind(self.triangle, "<ButtonPress-1>", self.Pressed)
        C.tag_bind(self.triangle, "<ButtonRelease-1>", self.Released)


class Ellipse():
    """Draws vector ellipse"""

    def __init__(self):
        self.ellipse = None
        self.rectangle = None
        self.moving = False
        self.click = False
        self.x = 0
        self.y = 0

    def Config(self, **kwargs):
        C.itemconfig(self.ellipse, kwargs)

    def coords(self, x, y):
        C.coords(self.rectangle, self.x, self.y, x, y)
        C.coords(self.ellipse, self.x, self.y, x, y)

    def Pressed(self, event):
        global prx, pry
        C.bind("<B1-Motion>", PASS)
        C.config(cursor="fleur")
        C.itemconfig(self.ellipse, outline="grey", activeoutline="grey")
        prx, pry = event.x, event.y

    def Moving(self, event):
        global prx, pry
        C.move(self.ellipse, event.x - prx, event.y - pry)
        prx, pry = event.x, event.y

    def Released(self, event):
        global cursor
        if not self.click:
            self.click = True
            C.tag_bind(self.ellipse, "<B1-Motion>", self.Moving)
        else:
            self.click = False
            C.config(cursor=cursor)
            C.itemconfig(self.ellipse, outline=self.color, activeoutline=self.activefill)
            C.tag_unbind(self.ellipse, "<B1-Motion>")
            ComboboxChanged()

    def Kill(self):
        global cursor
        C.delete(self.ellipse)
        if self.click:
            C.config(cursor=cursor)
            ComboboxChanged()
        del self

    def Create(self, coords, color, actfill, width):
        global FillIs
        self.x, self.y = coords
        self.activefill = actfill
        self.color = color
        self.rectangle = C.create_rectangle(self.x, self.y, self.x, self.y, dash=(7, 1, 1, 1), outline="grey")
        self.ellipse = C.create_oval(self.x, self.y, self.x, self.y,
                                     activeoutline=actfill, width=width, activedash=(7, 1, 1, 1), outline="grey",
                                     dash=(7, 1, 1, 1))
        C.tag_bind(self.ellipse, "<Button-2>", lambda e: self.Kill())
        C.tag_bind(self.ellipse, "<ButtonPress-1>", self.Pressed)
        C.tag_bind(self.ellipse, "<ButtonRelease-1>", self.Released)


class Rectangle():
    """Draws vector rectangle"""

    def __init__(self):
        self.rectangle = None
        self.moving = False
        self.click = False
        self.x = 0
        self.y = 0

    def Config(self, **kwargs):
        C.itemconfig(self.rectangle, kwargs)

    def coords(self, x, y):
        C.coords(self.rectangle, self.x, self.y, x, y)

    def Pressed(self, event):
        global prx, pry
        C.bind("<B1-Motion>", PASS)
        C.config(cursor="fleur")
        C.itemconfig(self.rectangle, outline="grey", activeoutline="grey")
        prx, pry = event.x, event.y

    def Moving(self, event):
        global prx, pry
        C.move(self.rectangle, event.x - prx, event.y - pry)
        prx, pry = event.x, event.y

    def Released(self, event):
        global cursor
        if not self.click:
            self.click = True
            C.tag_bind(self.rectangle, "<B1-Motion>", self.Moving)
        else:
            self.click = False
            C.config(cursor=cursor)
            C.itemconfig(self.rectangle, outline=self.color, activeoutline=self.activefill)
            C.tag_unbind(self.rectangle, "<B1-Motion>")
            ComboboxChanged()

    def Kill(self):
        global cursor
        C.delete(self.rectangle)
        if self.click:
            C.config(cursor=cursor)
            ComboboxChanged()
        del self

    def Create(self, coords, color, actfill, width):
        global FillIs
        self.x, self.y = coords
        self.activefill = actfill
        self.color = color
        self.rectangle = C.create_rectangle(self.x, self.y, self.x, self.y,
                                            activeoutline=actfill, width=width, activedash=(7, 1, 1, 1), outline="grey",
                                            dash=(7, 1, 1, 1))
        C.tag_bind(self.rectangle, "<Button-2>", lambda e: self.Kill())
        C.tag_bind(self.rectangle, "<ButtonPress-1>", self.Pressed)
        C.tag_bind(self.rectangle, "<ButtonRelease-1>", self.Released)


class Line():
    """Draws vector line"""

    def __init__(self):
        self.rectangle = None
        self.line = None
        self.moving = False
        self.click = False
        self.x = 0
        self.y = 0

    def Config(self, **kwargs):
        C.itemconfig(self.line, kwargs)

    def coords(self, x, y):
        C.coords(self.rectangle, self.x, self.y, x, y)
        C.coords(self.line, self.x, self.y, x, y)

    def Pressed(self, event):
        global prx, pry
        C.bind("<B1-Motion>", PASS)
        C.config(cursor="fleur")
        C.itemconfig(self.line, fill="grey", activefill="grey")
        prx, pry = event.x, event.y

    def Moving(self, event):
        global prx, pry
        C.move(self.line, event.x - prx, event.y - pry)
        prx, pry = event.x, event.y

    def Released(self, event):
        global cursor
        if not self.click:
            self.click = True
            C.tag_bind(self.line, "<B1-Motion>", self.Moving)
        else:
            self.click = False
            C.config(cursor=cursor)
            C.itemconfig(self.line, fill=self.color, activefill=self.activefill)
            C.tag_unbind(self.line, "<B1-Motion>")
            ComboboxChanged()

    def Kill(self):
        global cursor
        C.delete(self.line)
        if self.click:
            C.config(cursor=cursor)
            ComboboxChanged()
        del self

    def Create(self, coords, color, actfill, width):
        global FillIs
        self.x, self.y = coords
        self.activefill = actfill
        self.color = color
        self.rectangle = C.create_rectangle(self.x, self.y, self.x, self.y, dash=(7, 1, 1, 1), outline="grey")
        self.line = C.create_line(self.x, self.y, self.x, self.y,
                                  activefill=actfill, width=width, activedash=(7, 1, 1, 1), fill="grey",
                                  dash=(7, 1, 1, 1))
        C.tag_bind(self.line, "<Button-2>", lambda e: self.Kill())
        C.tag_bind(self.line, "<ButtonPress-1>", self.Pressed)
        C.tag_bind(self.line, "<ButtonRelease-1>", self.Released)


class Draw():
    """Draws"""

    def __init__(self):
        self.draw = None
        self.moving = False
        self.click = False

    def Config(self, **kwargs):
        C.itemconfig(self.draw, kwargs)

    def coords(self, x, y):
        C.coords(self.draw, *C.coords(self.draw), x, y)

    def Pressed(self, event):
        global prx, pry
        C.bind("<B1-Motion>", PASS)
        C.config(cursor="fleur")
        C.itemconfig(self.draw, fill="grey", activefill="grey")
        prx, pry = event.x, event.y

    def Moving(self, event):
        global prx, pry
        C.move(self.draw, event.x - prx, event.y - pry)
        prx, pry = event.x, event.y

    def Released(self, event):
        global cursor
        if not self.click:
            self.click = True
            C.tag_bind(self.draw, "<B1-Motion>", self.Moving)
        else:
            self.click = False
            C.config(cursor=cursor)
            C.itemconfig(self.draw, fill=self.color, activefill=self.activefill)
            C.tag_unbind(self.draw, "<B1-Motion>")
            ComboboxChanged()

    def Kill(self):
        global cursor
        C.delete(self.draw)
        if self.click:
            C.config(cursor=cursor)
            ComboboxChanged()
        del self

    def Create(self, coords, color, actfill, width):
        self.color = color
        self.activefill = actfill
        self.draw = C.create_line(*coords, fill=color,
                                  activefill=actfill, width=width, activedash=(5, 1))
        C.tag_bind(self.draw, "<Button-2>", lambda e: self.Kill())
        C.tag_bind(self.draw, "<ButtonPress-1>", self.Pressed)
        C.tag_bind(self.draw, "<ButtonRelease-1>", self.Released)


class Point():
    """Moving point in canvas"""

    def __init__(self):
        self.point = None

    def Create(self, event, color, size):
        global PointIs

        def PointMoving(event):
            global cx, cy
            LC.config(text=f"[X:{event.x};Y:{event.y}]")
            C.move(self.point, event.x - cx, event.y - cy)
            cx, cy = event.x, event.y

        PointIs = True
        self.point = C.create_oval((event.x + size / 2, event.y + size / 2), (event.x - size / 2, event.y - size / 2),
                                   fill=color, outline=color)
        C.bind("<Motion>", PointMoving)

    def Destroy(self):
        global PointIs
        PointIs = False
        C.delete(self.point)
        C.bind("<Motion>", PenEvMotion)


def CreatePoint(event, cl, sz):
    pass


#    global point
#    point.Create(event, color=cl, size=sz)
#    #C.config(cursor="none")

def EvLeave(event):
    #    global point
    #    point.Destroy()
    LC.config(text="Coordinates")


def EvCallback(event):
    global ComponentsAreHidden, ButtonColorsAreOpen, GridIs, EnteringIs
    if not EnteringIs:
        if (event.char.lower() == "h") or (event.char.lower() == "р"):
            if ComponentsAreHidden:
                ComponentsAreHidden = False
                MAIN.config(menu=M)
                FrameT.pack(side=TOP, fill="x")
                FrameL.pack(side=LEFT, fill="y")
                FrameR.pack(side=RIGHT, fill="y")
                FrameC.forget()
                FrameC.pack(fill=BOTH, expand=1)
                FrameB.pack(side=BOTTOM, fill="x")
                if ButtonColorsAreOpen:
                    FrameBC.pack(side=TOP, fill="x")
            else:
                ComponentsAreHidden = True
                MAIN.config(menu=EM)
                M.forget()
                FrameT.forget()
                FrameL.forget()
                FrameR.forget()
                FrameB.forget()
                if ButtonColorsAreOpen:
                    FrameBC.forget()
        elif (event.char.lower() == "g") or (event.char.lower() == "п"):
            Grid(False) if GridIs else Grid(True)


def TextMouseDown1(event):
    global DrawingIs, sz, cl, cx, cy, text, ft
    DrawingIs = True
    cx, cy = event.x, event.y
    text = Text()
    text.Create(coords=(event.x, event.y,), color=cl, actfill=penactfill, textfont=ft)


def TextEvMotion(event):
    global DrawingIs, cl, sz, cx, cy, penactfill, text
    LC.config(text=f"[X:{event.x};Y:{event.y}]")
    if DrawingIs:
        text.coords(event.x, event.y)
        text.moving = True
    cx, cy = event.x, event.y


def TextMouseUp1(event):
    global DrawingIs, sz, cl, cx, cy, penactfill, text, CanvasItems
    DrawingIs = False
    cx, cy = event.x, event.y
    text.coords(event.x, event.y)
    C.delete(text.rectangle)
    if not text.moving:
        C.delete(text.text)
        text.ent.destroy()
        del text
    else:
        C.itemconfig(text.text, fill=cl)


def StarMouseDown1(event):
    global DrawingIs, sz, cl, cx, cy, penactfill, star
    DrawingIs = True
    cx, cy = event.x, event.y
    star = Star()
    star.Create(coords=(event.x, event.y,), actfill=penactfill, width=sz, color=cl)


def StarEvMotion(event):
    global DrawingIs, cl, sz, cx, cy, penactfill, star
    LC.config(text=f"[X:{event.x};Y:{event.y}]")
    if DrawingIs:
        star.coords(event.x, event.y)
        star.moving = True
    cx, cy = event.x, event.y


def StarMouseUp1(event):
    global DrawingIs, sz, cl, cx, cy, penactfill, star, CanvasItems, FillIs
    DrawingIs = False
    cx, cy = event.x, event.y
    star.coords(event.x, event.y)
    C.delete(star.rectangle)
    if not star.moving:
        C.delete(star.star)
    else:
        star.Config(outline=cl, dash=())
        if FillIs:
            star.Config(fill=cl)


def RightTriangleMouseDown1(event):
    global DrawingIs, sz, cl, cx, cy, penactfill, rtrian
    DrawingIs = True
    cx, cy = event.x, event.y
    rtrian = RightTriangle()
    rtrian.Create(coords=(event.x, event.y,), actfill=penactfill, width=sz, color=cl)


def RightTriangleEvMotion(event):
    global DrawingIs, cl, sz, cx, cy, penactfill, rtrian
    LC.config(text=f"[X:{event.x};Y:{event.y}]")
    if DrawingIs:
        rtrian.coords(event.x, event.y)
        rtrian.moving = True
    cx, cy = event.x, event.y


def RightTriangleMouseUp1(event):
    global DrawingIs, sz, cl, cx, cy, penactfill, trian, CanvasItems, FillIs
    DrawingIs = False
    cx, cy = event.x, event.y
    rtrian.coords(event.x, event.y)
    C.delete(rtrian.rectangle)
    if not rtrian.moving:
        C.delete(rtrian.righttriangle)
    else:
        rtrian.Config(outline=cl, dash=())
        if FillIs:
            rtrian.Config(fill=cl)


def TriangleMouseDown1(event):
    global DrawingIs, sz, cl, cx, cy, penactfill, trian
    DrawingIs = True
    cx, cy = event.x, event.y
    trian = Triangle()
    trian.Create(coords=(event.x, event.y,), actfill=penactfill, width=sz, color=cl)


def TriangleEvMotion(event):
    global DrawingIs, cl, sz, cx, cy, penactfill, trian
    LC.config(text=f"[X:{event.x};Y:{event.y}]")
    if DrawingIs:
        trian.coords(event.x, event.y)
        trian.moving = True
    cx, cy = event.x, event.y


def TriangleMouseUp1(event):
    global DrawingIs, sz, cl, cx, cy, penactfill, trian, CanvasItems, FillIs
    DrawingIs = False
    cx, cy = event.x, event.y
    trian.coords(event.x, event.y)
    C.delete(trian.rectangle)
    if not trian.moving:
        C.delete(trian.triangle)
    else:
        trian.Config(outline=cl, dash=())
        if FillIs:
            trian.Config(fill=cl)


def EllipseMouseDown1(event):
    global DrawingIs, sz, cl, cx, cy, penactfill, ell
    DrawingIs = True
    cx, cy = event.x, event.y
    ell = Ellipse()
    ell.Create(coords=(event.x, event.y,), actfill=penactfill, width=sz, color=cl)


def EllipseEvMotion(event):
    global DrawingIs, cx, cy, ell
    LC.config(text=f"[X:{event.x};Y:{event.y}]")
    if DrawingIs:
        ell.coords(event.x, event.y)
        ell.moving = True
    cx, cy = event.x, event.y


def EllipseMouseUp1(event):
    global DrawingIs, cl, cx, cy, ell, CanvasItems, FillIs
    DrawingIs = False
    cx, cy = event.x, event.y
    ell.coords(event.x, event.y)
    C.delete(ell.rectangle)
    if not ell.moving:
        C.delete(ell.ellipse)
    else:
        ell.Config(outline=cl, dash=())
        if FillIs:
            ell.Config(fill=cl)


def RectangleMouseDown1(event):
    global DrawingIs, sz, cl, cx, cy, penactfill, rect
    DrawingIs = True
    cx, cy = event.x, event.y
    rect = Rectangle()
    rect.Create(coords=(event.x, event.y,), actfill=penactfill, width=sz, color=cl)


def RectangleEvMotion(event):
    global DrawingIs, cx, cy, rect
    LC.config(text=f"[X:{event.x};Y:{event.y}]")
    if DrawingIs:
        rect.coords(event.x, event.y)
        rect.moving = True
    cx, cy = event.x, event.y


def RectangleMouseUp1(event):
    global DrawingIs, cl, cx, cy, rect, CanvasItems, FillIs
    DrawingIs = False
    cx, cy = event.x, event.y
    rect.coords(event.x, event.y)
    if not rect.moving:
        C.delete(rect.rectangle)
    else:
        rect.Config(outline=cl, dash=())
        if FillIs:
            rect.Config(fill=cl)


def LineMouseDown1(event):
    global DrawingIs, sz, cl, cx, cy, penactfill, line
    DrawingIs = True
    cx, cy = event.x, event.y
    line = Line()
    line.Create(coords=(event.x, event.y,), actfill=penactfill, width=sz, color=cl)


def LineEvMotion(event):
    global DrawingIs, cx, cy, line
    LC.config(text=f"[X:{event.x};Y:{event.y}]")
    if DrawingIs:
        line.coords(event.x, event.y)
        line.moving = True
    cx, cy = event.x, event.y


def LineMouseUp1(event):
    global DrawingIs, cl, cx, cy, line, CanvasItems, FillIs
    DrawingIs = False
    cx, cy = event.x, event.y
    line.coords(event.x, event.y)
    C.delete(line.rectangle)
    if not line.moving:
        C.delete(line.rectangle)
        C.delete(line.line)
    else:
        line.Config(fill=cl, dash=())
        if FillIs:
            rect.Config(fill=cl)


def PenMouseDown1(event):
    global DrawingIs, sz, cl, cx, cy, penactfill, draw
    DrawingIs = True
    cx, cy = event.x, event.y
    draw = Draw()
    draw.Create(coords=(event.x, event.y, event.x, event.y,), actfill=penactfill, width=sz, color=cl)


def PenEvMotion(event):
    global DrawingIs, cl, sz, cx, cy, penactfill, draw
    LC.config(text=f"[X:{event.x};Y:{event.y}]")
    if DrawingIs:
        draw.coords(event.x, event.y)
        draw.moving = True
    cx, cy = event.x, event.y


def PenMouseUp1(event):
    global DrawingIs, sz, cl, cx, cy, penactfill, draw, CanvasItems
    DrawingIs = False
    cx, cy = event.x, event.y
    draw.coords(event.x, event.y)
    if not draw.moving:
        C.delete(draw.draw)
    else:
        pass


def SetColor(mode, color=None):
    global cl, bgcl
    if mode == "color":
        a = askcolor(color=cl, parent=MAIN)
        if a[0] != None:
            cl = a[1]
            Bcl.configure(bg=cl)
    elif mode == "bgcolor":
        a = askcolor(color=bgcl, parent=MAIN)
        if a[0] != None:
            bgcl = a[1]
            Bbgcl.configure(bg=bgcl)
            C.configure(bg=bgcl)
    elif mode == "buttons":
        cl = color
        Bcl.configure(bg=cl)
    elif mode == "menucolor":
        cl = color
        Bcl.configure(bg=cl)
    elif mode == "menubgcolor":
        bgcl = color
        Bbgcl.configure(bg=bgcl)
        C.configure(bg=bgcl)


def SetSize(val, mode=0):
    global sz, sz2
    if mode == 0:
        sz = val
        SBsz.set(sz)
    elif mode == 1:
        sz2 = val
        SBsz2.set(sz2)


def SetFont(font):
    global ft
    ft = font


def SizeChanged(mode):
    global sz, sz2
    if mode == "sz":
        sz = int(SBsz.get())
        Lsz["text"] = f"Size({sz})"
    elif mode == "sz2":
        sz2 = int(SBsz2.get())
        Lsz2["text"] = f"Size2({sz2})"


def ComboboxChanged(event=None):
    if CB.current() == 0:
        C.bind("<ButtonPress-1>", PenMouseDown1)
        C.bind("<B1-Motion>", PenEvMotion)
        C.bind("<ButtonRelease-1>", PenMouseUp1)
    if CB.current() == 1:
        C.bind("<ButtonPress-1>", LineMouseDown1)
        C.bind("<B1-Motion>", LineEvMotion)
        C.bind("<ButtonRelease-1>", LineMouseUp1)
    elif CB.current() == 2:
        C.bind("<ButtonPress-1>", RectangleMouseDown1)
        C.bind("<B1-Motion>", RectangleEvMotion)
        C.bind("<ButtonRelease-1>", RectangleMouseUp1)
    elif CB.current() == 3:
        C.bind("<ButtonPress-1>", EllipseMouseDown1)
        C.bind("<B1-Motion>", EllipseEvMotion)
        C.bind("<ButtonRelease-1>", EllipseMouseUp1)
    elif CB.current() == 4:
        C.bind("<ButtonPress-1>", TriangleMouseDown1)
        C.bind("<B1-Motion>", TriangleEvMotion)
        C.bind("<ButtonRelease-1>", TriangleMouseUp1)
    elif CB.current() == 5:
        C.bind("<ButtonPress-1>", RightTriangleMouseDown1)
        C.bind("<B1-Motion>", RightTriangleEvMotion)
        C.bind("<ButtonRelease-1>", RightTriangleMouseUp1)
    elif CB.current() == 6:
        C.bind("<ButtonPress-1>", StarMouseDown1)
        C.bind("<B1-Motion>", StarEvMotion)
        C.bind("<ButtonRelease-1>", StarMouseUp1)
    elif CB.current() == 7:
        C.bind("<ButtonPress-1>", TextMouseDown1)
        C.bind("<B1-Motion>", TextEvMotion)
        C.bind("<ButtonRelease-1>", TextMouseUp1)
    elif CB.current() == 8:
        C.unbind("<ButtonPress-1>")
        C.unbind("<B1-Motion>")
        C.unbind("<ButtonRelease-1>")


def GridSettings():
    global gridA

    def SetGridA(event):
        val = sc1.get()
        ent1["state"] = "normal"
        ent1.delete(0, END)
        ent1.insert(0, str(int(val)))
        ent1["state"] = "readonly"
        for i in range(0, len(linesx)):
            linesx[i].coords(val * i, 0, val * i, maxy)
        for i in range(0, len(linesy)):
            linesx[i].coords(0, val * i, maxx, val * i)

    def Setl(event):
        l.config(text=f"[X:{event.x};Y:{event.y}]")
        if (event.x < 90) and (event.y < 30):
            l.place(x=event.x + 20, y=event.y + 10)
        elif event.x < 90:
            l.place(x=event.x + 20, y=event.y - 30)
        elif event.y < 30:
            l.place(x=event.x - l.winfo_width(), y=event.y + 10)
        else:
            l.place(x=event.x - l.winfo_width(), y=event.y - 30)

    t = Toplevel(MAIN)
    t.resizable(False, False)
    t.title("Grid settings")
    # t.protocol("WM_DELETE_WINDOW", PASS)
    t.transient(MAIN)
    t.grab_set()
    linesx, linesy = [], []
    lf = ttk.LabelFrame(t, text="Settings")
    f = ttk.Frame(lf, relief=RIDGE)
    c = Canvas(f, width=400, height=300, cursor="crosshair")
    c.bind("<Motion>", Setl)
    c.bind("<Enter>", lambda event: Setl(event))
    c.bind("<Leave>", lambda event: l.place_forget())
    maxx, maxy = int(c["width"]), int(c["height"])
    lx, ly = maxx // gridA, maxy // gridA
    for i in range(1, lx):
        gridline = c.create_line((i * gridA, 0), (i * gridA, maxy))
        linesx.insert(0, gridline)
    for i in range(1, ly):
        gridline = c.create_line((0, i * gridA), (maxx, i * gridA))
        linesy.insert(0, gridline)
    c.pack(padx=2, pady=2)
    l = ttk.Label(c, text="", width=14)
    f.pack(side=LEFT, padx=20, pady=20)
    ent1 = ttk.Entry(lf, state="readonly", width=3)
    ent1.insert(0, str(gridA))
    ent1.pack(side=RIGHT, pady=30, anchor=N)
    sc1 = ttk.Scale(lf, from_=10, to=150, cursor="hand2", command=SetGridA)
    sc1.set(gridA)
    sc1.pack(side=RIGHT, padx=10, pady=30, anchor=N)
    lf.pack(padx=10, pady=10)
    t.mainloop()


def GetFont():
    global ft
    fonts = ['System', 'Terminal', 'Fixedsys', 'Modern', 'Roman', 'Script', ".keyboard",
             'Courier', 'Marlett', 'Arial', 'Bahnschrift', 'Calibri', 'Cambria',
             'Candara', 'Consolas', 'Constantia', 'Corbel', 'Courier', 'Ebrima',
             'Gabriola', 'Gadugi', 'Georgia', 'Impact', 'MingLiU-ExtB', '@MingLiU-ExtB',
             'PMingLiU-ExtB', '@PMingLiU-ExtB', 'MingLiU_HKSCS-ExtB', '@MingLiU_HKSCS-ExtB',
             'SimSun', '@SimSun', 'NSimSun', '@NSimSun', 'SimSun-ExtB', '@SimSun-ExtB',
             'Sylfaen', 'Symbol', 'Tahoma', 'Verdana', 'Webdings', 'Wingdings',
             'Century', 'Wingdings 2', 'Wingdings 3', 'Pristina', 'Papyrus',
             'Mistral', 'Garamond', 'Algerian', 'Bauhaus 93', 'Broadway', 'Centaur',
             'Chiller', 'Harrington', 'Jokerman', 'Magneto', 'Onyx', 'Parchment',
             'Playbill', 'Ravie', 'Stencil', 'Vivaldi', 'Rockwell', 'Perpetua',
             'Haettenschweiler', 'Gigi', 'Forte', 'Elephant', 'Castellar']
    modal = Modal()
    modal.Create(ft, "Fonts", fonts, modal.SetFont, modal.GetAndExit3, modal.CancelFont)


def GetTheme():
    global theme
    themes = ["alt",
              "aquativo", "arc", "breeze", "black", "blue", "clam", "classic", "clearlooks", "default",
              "equilux", "itft1", "keramik", "kroc", "plastik", "radiance", "scidblue", "scidgreen",
              "scidgrey", "scidmint", "scidpink", "scidpurple", "scidsand", "smog", "tk", "ubuntu", "winnative",
              "winxpblue", "yaru"]
    modal = Modal()
    modal.Create(theme, "Themes", themes, modal.SetTheme, modal.GetAndExit2, modal.CancelTheme)


def GetCursor():
    global cursor
    cursors = ['X_cursor', 'arrow', 'based_arrow_down', 'based_arrow_up', 'boat',
               'bogosity', 'bottom_left_corner', 'bottom_right_corner', 'bottom_side',
               'bottom_tee', 'box_spiral', 'center_ptr', 'circle', 'clock', 'coffee_mug',
               'cross', 'cross_reverse', 'crosshair', 'diamond_cross', 'dot', 'dotbox',
               'double_arrow', 'draft_large', 'draft_small', 'draped_box', 'exchange',
               'fleur', 'gobbler', 'gumby', 'hand1', 'hand2', 'heart', 'icon', 'iron_cross',
               'left_ptr', 'left_side', 'left_tee', 'leftbutton', 'll_angle', 'lr_angle',
               'man', 'middlebutton', 'mouse', 'none', 'pencil', 'pirate', 'plus', 'question_arrow',
               'right_ptr', 'right_side', 'right_tee', 'rightbutton', 'rtl_logo', 'sailboat',
               'sb_down_arrow', 'sb_h_double_arrow', 'sb_left_arrow', 'sb_right_arrow',
               'sb_up_arrow', 'sb_v_double_arrow', 'shuttle', 'sizing', 'spider', 'spraycan',
               'star', 'target', 'tcross', 'top_left_arrow', 'top_left_corner', 'top_right_corner',
               'top_side', 'top_tee', 'trek', 'ul_angle', 'umbrella', 'ur_angle', 'watch', 'xterm']

    modal = Modal()
    modal.Create(cursor, "Cursors", cursors, modal.SetCursor, modal.GetAndExit, modal.CancelCursor)


def ShowBtnColors():
    global ButtonColorsAreOpen
    if ButtonColorsAreOpen:
        ButtonColorsAreOpen = False
        Bclsopen.configure(text="˄")
        FrameBC.forget()
    else:
        ButtonColorsAreOpen = True
        Bclsopen.configure(text="˅")
        FrameBC.pack(side=TOP, fill="x")


def Grid(mode):
    global GridIs, GridItems, gridA
    if mode and not GridIs:
        GridIs = True
        maxx, maxy = MAIN.winfo_screenwidth(), MAIN.winfo_screenheight()
        lx, ly = maxx // gridA, maxy // gridA
        for i in range(1, lx):
            gridline = C.create_line((i * gridA, 0), (i * gridA, maxy))
            GridItems.insert(-1, gridline)
        for i in range(1, ly):
            gridline = C.create_line((0, i * gridA), (maxx, i * gridA))
            GridItems.insert(-1, gridline)
    elif not mode and GridIs:
        GridIs = False
        for i in GridItems:
            C.delete(i)


def ThemeChange(theme):
    MAIN.configure(theme=theme)


def FullScreen():
    global FullScreenedIs
    if FullScreenedIs:
        FullScreenedIs = False
        MAIN.attributes('-fullscreen', False)
    else:
        FullScreenedIs = True
        MAIN.attributes('-fullscreen', True)


def Clear(ask=False):
    global GridIs, CanvasItems
    if not ask:
        C.delete(ALL)
        CanvasItems = []
        if GridIs:
            Grid(False)
            Grid(True)
    else:
        if askokcancel("Clearing", "Do you want to clear the sheet?"):
            C.delete(ALL)
            CanvasItems = []
            if GridIs:
                Grid(False)
                Grid(True)


def DelLastItem():
    global CanvasItems
    C.delete(CanvasItems[-1])


def SetCursor(val):
    global cursor
    cursor = val
    C.configure(cursor=val)


def SetFill(fill):
    global FillIs
    FillIs = True if fill else False


def AddTooltips():
    ToolTip(LC, "Text").waittime = 1000  # Coordinates
    ToolTip(CB, "Text").waittime = 1000  # Combobox
    ToolTip(Lsz, "Text").waittime = 1000  # Label size
    ToolTip(Lsz2, "Text").waittime = 1000  # Label size2
    ToolTip(SBsz, "Text").waittime = 1000  # Scale sz
    ToolTip(SBsz2, "Text").waittime = 1000  # Scale sz2
    ToolTip(QuitBtn, "Text").waittime = 1000  # Button quit
    # ...


MAIN = ThemedTk(theme=theme)

try:
    MAIN.call('wm', 'iconphoto', MAIN._w, PhotoImage(file='python.png'))
except:
    pass

w, h = MAIN.winfo_screenwidth(), MAIN.winfo_screenheight()
MAIN.geometry("%dx%d+0+0" % (w, h))
MAIN.attributes('-fullscreen', False)
MAIN.title("Picture")
MAIN.state("zoomed")
MAIN.tkraise()
MAIN.bind("<Key>", EvCallback)
MAIN.bind("<Escape>", lambda e: MAIN.iconify())
MAIN.protocol("WM_DELETE_WINDOW", lambda: MAIN.destroy())
MAIN.configure(cursor="arrow")

FrameT = ttk.Frame(MAIN)
FrameL = ttk.Frame(MAIN)
FrameC = ttk.Frame(MAIN)
FrameR = ttk.Frame(MAIN)
FrameBC = ttk.Frame(MAIN)
FrameB = ttk.Frame(MAIN)

LC = ttk.Label(FrameT, font=("Arial", 8), text="Coordinates", cursor="hand2", width=15)
LC.pack(side=LEFT, padx=10)

cboxstyle = ttk.Style()
cboxstyle.configure("W.TCombobox", fieldbackground="silver", foreground="silver",
                    background="silver", fieldforeground="silver")

CB = ttk.Combobox(FrameT, style="W.TCombobox", state="readonly",
                  values=["Pencil", "Line", "Rectangle", "Ellipse", "Triangle", "Right triangle", "Star", "Text",
                          "None"])
CB.current(0)
CB.bind("<<ComboboxSelected>>", ComboboxChanged)
CB.pack(side=LEFT, padx=10)

Lsz = ttk.Label(FrameT, font=(".keyboard", 8), width=9, text=f"Size({sz})", cursor="hand2")
Lsz.bind("<Button-3>", PASS)
Lsz.pack(side=LEFT, padx=4)

SBsz = ttk.Scale(FrameT, from_=1, to=100, cursor="hand2", command=lambda e: SizeChanged(mode="sz"))
SBsz.set(sz)
SBsz.pack(side=LEFT, padx=4)

Lsz2 = ttk.Label(FrameT, font=(".keyboard", 8), width=9, text=f"Size2({sz2})", cursor="hand2")
Lsz2.bind("<Button-3>", PASS)
Lsz2.pack(side=LEFT, padx=4)

SBsz2 = ttk.Scale(FrameT, from_=1, to=200, cursor="hand2", command=lambda e: SizeChanged(mode="sz2"))
SBsz2.set(sz2)
SBsz2.pack(side=LEFT, padx=4)

qstyle = ttk.Style()
qstyle.configure("W.TButton", background="red")

QuitBtn = ttk.Button(FrameT, text="Quit", cursor="hand2", command=lambda: MAIN.destroy(), style="W.TButton")
QuitBtn.pack(side=RIGHT)

Bbgcl = Button(FrameT, text="Background", cursor="hand2", command=lambda: SetColor(mode="bgcolor"),
               bg=bgcl)
Bbgcl.pack(side=RIGHT, padx=10)

Bcl = Button(FrameT, text="Colour", cursor="hand2", command=lambda: SetColor(mode="color"),
             bg=cl)
Bcl.pack(side=RIGHT, padx=6)

LBtnClose = ttk.Button(FrameL, text="x", cursor="hand2", width=1, command=lambda: FrameL.forget())
LBtnClose.pack()

LBtnOpen = ttk.Button(FrameL, text=">", cursor="hand2", width=1, command=PASS)
LBtnOpen.pack(pady=20)

RBtnClose = ttk.Button(FrameR, text="x", cursor="hand2", width=1, command=lambda: FrameR.forget())
RBtnClose.pack(anchor=W)

RBtnOpen = ttk.Button(FrameR, text="<", cursor="hand2", width=1, command=PASS)
RBtnOpen.pack(pady=20, anchor=W)

textvar = ttk.Label(FrameR, text=ft, font=(ft, 14))

for i in BtnClList:
    btncl = Button(FrameBC, width=3, cursor="hand2", bg=i,
                   command=partial(SetColor, mode="buttons", color=i))
    btncl.pack(side=RIGHT, padx=4)

L2 = ttk.Label(FrameB, text="Pencil")
L2.bind("<Button-3>", PASS)
L2.pack(side=LEFT)

Bclsopen = ttk.Button(FrameB, text="˄", cursor="hand2", width=1, command=lambda: ShowBtnColors())
Bclsopen.pack(side=RIGHT, padx=6)

MBackground = Menu(tearoff=0, bd=20, bg="#424242", fg="white")
MBackground.add_command(activebackground="white", activeforeground="black", label="White",
                        command=lambda: SetColor("menubgcolor", color="white"))
MBackground.add_command(activebackground="red", label="Red", command=lambda: SetColor("menubgcolor", color="red"))
MBackground.add_command(activebackground="maroon", label="Maroon",
                        command=lambda: SetColor("menubgcolor", color="maroon"))
MBackground.add_command(activebackground="orange", label="Orange",
                        command=lambda: SetColor("menubgcolor", color="orange"))
MBackground.add_command(activebackground="brown", label="Brown", command=lambda: SetColor("menubgcolor", color="brown"))
MBackground.add_command(activebackground="grey", label="Grey", command=lambda: SetColor("menubgcolor", color="grey"))
MBackground.add_command(activebackground="yellow", label="Yellow",
                        command=lambda: SetColor("menubgcolor", color="yellow"))
MBackground.add_command(activebackground="green", label="Green", command=lambda: SetColor("menubgcolor", color="green"))
MBackground.add_command(activebackground="indigo", label="Indigo",
                        command=lambda: SetColor("menubgcolor", color="indigo"))
MBackground.add_command(activebackground="blue", label="Blue", command=lambda: SetColor("menubgcolor", color="blue"))
MBackground.add_command(activebackground="aqua", label="Aqua", command=lambda: SetColor("menubgcolor", color="aqua"))
MBackground.add_command(activebackground="violet", label="Violet",
                        command=lambda: SetColor("menubgcolor", color="violet"))
MBackground.add_command(activebackground="purple", label="Purple",
                        command=lambda: SetColor("menubgcolor", color="purple"))
MBackground.add_command(activebackground="pink", label="Pink", command=lambda: SetColor("menubgcolor", color="pink"))
MBackground.add_command(activebackground="black", label="Black", command=lambda: SetColor("menubgcolor", color="black"))
MBackground.add_separator()
MBackground.add_command(label="Palette", command=lambda: SetColor(mode="bgcolor"))

MColor = Menu(tearoff=0, bd=20, bg="#424242", fg="white")
MColor.add_command(activebackground="white", activeforeground="black", label="White",
                   command=lambda: SetColor("menucolor", color="white"))
MColor.add_command(activebackground="red", label="Red", command=lambda: SetColor("menucolor", color="red"))
MColor.add_command(activebackground="maroon", label="Maroon", command=lambda: SetColor("menucolor", color="maroon"))
MColor.add_command(activebackground="orange", label="Orange", command=lambda: SetColor("menucolor", color="orange"))
MColor.add_command(activebackground="brown", label="Brown", command=lambda: SetColor("menucolor", color="brown"))
MColor.add_command(activebackground="grey", label="Grey", command=lambda: SetColor("menucolor", color="grey"))
MColor.add_command(activebackground="yellow", label="Yellow", command=lambda: SetColor("menucolor", color="yellow"))
MColor.add_command(activebackground="green", label="Green", command=lambda: SetColor("menucolor", color="green"))
MColor.add_command(activebackground="indigo", label="Indigo", command=lambda: SetColor("menucolor", color="indigo"))
MColor.add_command(activebackground="blue", label="Blue", command=lambda: SetColor("menucolor", color="blue"))
MColor.add_command(activebackground="aqua", label="Aqua", command=lambda: SetColor("menucolor", color="aqua"))
MColor.add_command(activebackground="violet", label="Violet", command=lambda: SetColor("menucolor", color="violet"))
MColor.add_command(activebackground="purple", label="Purple", command=lambda: SetColor("menucolor", color="purple"))
MColor.add_command(activebackground="pink", label="Pink", command=lambda: SetColor("menucolor", color="pink"))
MColor.add_command(activebackground="black", label="Black", command=lambda: SetColor("menucolor", color="black"))
MColor.add_separator()
MColor.add_command(label="Palette", command=lambda: SetColor(mode="color"))

MSize = Menu(tearoff=0, bd=20, bg="#424242", fg="white")
MSize.add_command(label="1pix", command=lambda: SetSize(1, mode=0))
MSize.add_command(label="2pix", command=lambda: SetSize(2, mode=0))
MSize.add_command(label="4pix", command=lambda: SetSize(4, mode=0))
MSize.add_command(label="6pix", command=lambda: SetSize(6, mode=0))
MSize.add_command(label="8pix", command=lambda: SetSize(8, mode=0))
MSize.add_command(label="10pix", command=lambda: SetSize(10, mode=0))
MSize.add_command(label="12pix", command=lambda: SetSize(12, mode=0))
MSize.add_command(label="14pix", command=lambda: SetSize(14, mode=0))
MSize.add_command(label="16pix", command=lambda: SetSize(16, mode=0))
MSize.add_command(label="18pix", command=lambda: SetSize(18, mode=0))
MSize.add_command(label="20pix", command=lambda: SetSize(20, mode=0))
MSize.add_command(label="24pix", command=lambda: SetSize(24, mode=0))
MSize.add_command(label="28pix", command=lambda: SetSize(28, mode=0))
MSize.add_command(label="34pix", command=lambda: SetSize(34, mode=0))
MSize.add_command(label="40pix", command=lambda: SetSize(40, mode=0))
MSize.add_command(label="50pix", command=lambda: SetSize(50, mode=0))
MSize.add_command(label="60pix", command=lambda: SetSize(60, mode=0))
MSize.add_command(label="72pix", command=lambda: SetSize(72, mode=0))
MSize.add_separator()
MSize.add_command(label="Set size", command=PASS)

MShapesW = Menu(tearoff=0, bd=20, bg="#424242", fg="white")
MShapesW.add_command(label="l", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="M", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="n", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="o", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="p", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="q", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="r", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="u", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="v", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="w", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="J", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="K", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="L", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="M", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="N", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="O", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="R", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="S", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="T", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="U", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="V", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="W", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="X", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="Y", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="Z", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="1", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="2", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="3", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="4", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="5", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="6", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="7", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="8", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="9", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="0", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="(", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label=")", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="*", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="%", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="[", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="]", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="{", font=("Wingdings", 18), command=PASS)
MShapesW.add_command(label="}", font=("Wingdings", 18), command=PASS)

MFigures = Menu(tearoff=0, bd=20, bg="#424242", fg="white")
MFigures.add_cascade(label="Shapes", menu=MShapesW)
MFigures.add_command(label="Left diagonal-Circle, Mouse right button", command=PASS)
MFigures.add_command(label="Circle, Mouse right button", command=PASS)
MFigures.add_command(label="Rainbow-circle, Mouse right button", command=PASS)
MFigures.add_command(label="Oval, Mouse right button", command=PASS)
MFigures.add_command(label="Square, Mouse right button", command=PASS)
MFigures.add_command(label="Rainbow-square, Mouse right button", command=PASS)
MFigures.add_command(label="Rectangle, Mouse right button", command=PASS)
MFigures.add_command(label="Rhombus, Mouse right button", command=PASS)
MFigures.add_command(label="Line, Mouse right button", command=PASS)
MFigures.add_command(label="Center-line, Mouse right button, Mouse middle button", command=PASS)
MFigures.add_command(label="Dashed line, Mouse right button", command=PASS)
MFigures.add_command(label="Polygon, Mouse right button, Mouse middle button", command=PASS)
MFigures.add_command(label="Equilateral, Mouse right button", command=PASS)
MFigures.add_command(label="Rainbow-equilateral, Mouse right button", command=PASS)
MFigures.add_command(label="Pencil, Mouse right button, Mouse middle button", command=PASS)
MFigures.add_command(label="Rope, Mouse right button", command=PASS)
MFigures.add_command(label="Plus, Mouse right button", command=PASS)
MFigures.add_command(label="Cross, Mouse right button", command=PASS)
MFigures.add_command(label="Felt-pen, Mouse right button, Mouse middle button", command=PASS)
MFigures.add_command(label="Rainbow, Mouse right button, Mouse middle button", command=PASS)
MFigures.add_command(label="Text, Mouse right button", command=PASS)

MGeometry = Menu(tearoff=0, bd=20, bg="#424242", fg="white")
MGeometry.add_command(label=f"Default({w}x{h})", command=PASS)
MGeometry.add_command(label="Height", command=PASS)
MGeometry.add_command(label="Length", command=PASS)

MAuthor = Menu(tearoff=0, bd=20, bg="#424242", fg="white")
MAuthor.add_command(label="More")

MTransperency = Menu(tearoff=0, bd=20, bg="#424242", fg="white")
MTransperency.add_command(label="1", command=lambda: MAIN.wm_attributes('-alpha', 0.01))
MTransperency.add_command(label="10", command=lambda: MAIN.wm_attributes('-alpha', 0.1))
MTransperency.add_command(label="20", command=lambda: MAIN.wm_attributes('-alpha', 0.2))
MTransperency.add_command(label="30", command=lambda: MAIN.wm_attributes('-alpha', 0.3))
MTransperency.add_command(label="40", command=lambda: MAIN.wm_attributes('-alpha', 0.4))
MTransperency.add_command(label="50", command=lambda: MAIN.wm_attributes('-alpha', 0.5))
MTransperency.add_command(label="60", command=lambda: MAIN.wm_attributes('-alpha', 0.6))
MTransperency.add_command(label="70", command=lambda: MAIN.wm_attributes('-alpha', 0.7))
MTransperency.add_command(label="80", command=lambda: MAIN.wm_attributes('-alpha', 0.8))
MTransperency.add_command(label="90", command=lambda: MAIN.wm_attributes('-alpha', 0.9))
MTransperency.add_command(label="100", command=lambda: MAIN.wm_attributes('-alpha', 1))

MGrid = Menu(tearoff=0, bd=20, bg="#424242", fg="white")
MGrid.add_command(label="On", command=lambda: Grid(True))
MGrid.add_command(label="Off", command=lambda: Grid(False))

MWindow = Menu(tearoff=0, bd=20, bg="#424242", fg="white")
MWindow.add_command(label="Full screen", command=FullScreen)
MWindow.add_cascade(label="Window size", menu=MGeometry)
MWindow.add_cascade(label="Transparency", menu=MTransperency)
MWindow.add_command(label="Themes", command=GetTheme)

MFile = Menu(tearoff=0, bd=20, bg="#424242", fg="white")
MFile.add_command(label="Function", command=PASS)
MFile.add_command(label="Coordinates", command=PASS)
MFile.add_command(label="Random", command=PASS)
MFile.add_command(label="Clear", command=Clear)
MFile.add_cascade(label="Picture size", menu=MGeometry)
MFile.add_cascade(label="Grid", menu=MGrid)
MFile.add_command(label="Grid settings", command=GridSettings)
MFile.add_command(label="Hotkeys", command=PASS)
MFile.add_command(label="Text size", command=PASS)
MFile.add_command(label="Save at format PostScript", command=PASS)
MFile.add_command(label="Python regime", command=PASS)
MFile.add_separator()
MFile.add_command(label="Close the picture", command=PASS)

MLanguage = Menu(tearoff=0, bd=20, bg="#424242", fg="white")
MLanguage.add_command(activebackground="blue", label="English", command=PASS)
MLanguage.add_command(label="Ukrainian", command=PASS)
MLanguage.add_command(label="Russian", command=PASS)

MFill = Menu(tearoff=0, bd=20, bg="#424242", fg="white")
MFill.add_command(label="On", command=lambda: SetFill(True))
MFill.add_command(label="Off", command=lambda: SetFill(False))

MSize2 = Menu(tearoff=0, bd=20, bg="#424242", fg="white")
MSize2.add_command(label="10pix", command=lambda: SetSize(10, mode=1))
MSize2.add_command(label="25pix", command=lambda: SetSize(25, mode=1))
MSize2.add_command(label="50pix", command=lambda: SetSize(50, mode=1))
MSize2.add_command(label="75pix", command=lambda: SetSize(75, mode=1))
MSize2.add_command(label="100pix", command=lambda: SetSize(100, mode=1))
MSize2.add_command(label="150pix", command=lambda: SetSize(150, mode=1))
MSize2.add_command(label="200pix", command=lambda: SetSize(200, mode=1))
MSize2.add_separator()
MSize2.add_command(label="Set size2", command=PASS)

MFonts = Menu(tearoff=0, bd=20, bg="#424242", fg="white")
MFonts.add_command(label="All fonts", command=GetFont)
MFonts.add_separator()
MFonts.add_command(label="Default", font=".Keyboard", command=lambda: SetFont(".Keyboard"))
MFonts.add_command(label="Algerian", font="Algerian", command=lambda: SetFont("Algerian"))
MFonts.add_command(label="Arial", font="Arial", command=lambda: SetFont("Arial"))
MFonts.add_command(label="Calibri", font="Calibri", command=lambda: SetFont("Calibri"))
MFonts.add_command(label="Corbel", font="Corbel", command=lambda: SetFont("Corbel"))
MFonts.add_command(label="Impact", font="Impact", command=lambda: SetFont("Impact"))
MFonts.add_command(label="Forte", font="Forte", command=lambda: SetFont("Forte"))
MFonts.add_command(label="Broadway", font="Broadway", command=lambda: SetFont("Broadway"))
MFonts.add_command(label="CASTELLAR", font="CASTELLAR", command=lambda: SetFont("CASTELLAR"))
MFonts.add_command(label="Centaur", font="Centaur", command=lambda: SetFont("Centaur"))
MFonts.add_command(label="Chiller", font="Chiller", command=lambda: SetFont("Chiller"))
MFonts.add_command(label="Constantia", font="Constantia", command=lambda: SetFont("Constantia"))
MFonts.add_command(label="Gabriola", font="Gabriola", command=lambda: SetFont("Gabriola"))
MFonts.add_command(label="Gigi", font="Gigi", command=lambda: SetFont("Gigi"))
MFonts.add_command(label="Fixedsys", font="Fixedsys", command=lambda: SetFont("Fixedsys"))
MFonts.add_command(label="Georgia", font="Georgia", command=lambda: SetFont("Georgia"))
MFonts.add_command(label="Modern", font="Modern", command=lambda: SetFont("Modern"))
MFonts.add_command(label="System", font="System", command=lambda: SetFont("System"))
MFonts.add_command(label="Verdana", font="Verdana", command=lambda: SetFont("Verdana"))
MFonts.add_command(label="Vivaldi", font="Vivaldi", command=lambda: SetFont("Vivaldi"))
MFonts.add_command(label="Stencil", font="Stencil", command=lambda: SetFont("Stencil"))
MFonts.add_command(label="Rockwell", font="Rockwell", command=lambda: SetFont("Rockwell"))
MFonts.add_command(label="Papyrus", font="Papyrus", command=lambda: SetFont("Papyrus"))
MFonts.add_command(label="Roman", font="Roman", command=lambda: SetFont("Roman"))
MFonts.add_command(label="Parchment", font="Parchment", command=lambda: SetFont("Parchment"))
MFonts.add_command(label="Playbill", font="Playbill", command=lambda: SetFont("Playbill"))
MFonts.add_command(label="Pristina", font="Pristina", command=lambda: SetFont("Pristina"))
MFonts.add_command(label="Mistral", font="Mistral", command=lambda: SetFont("Mistral"))
MFonts.add_command(label="Jokerman", font="Jokerman", command=lambda: SetFont("Jokerman"))
MFonts.add_command(label="Harrington", font="Harrington", command=lambda: SetFont("Harrington"))
MFonts.add_command(label="Lato", font="Lato", command=lambda: SetFont("Lato"))
MFonts.add_command(label="Ravie", font="Ravie", command=lambda: SetFont("Ravie"))
MFonts.add_command(label="Times New Roman", font="Times", command=lambda: SetFont("Times"))
MFonts.add_command(label="Onyx", font="Onyx", command=lambda: SetFont("Onyx"))
MFonts.add_command(label="Oswald", font="Oswald", command=lambda: SetFont("Oswald"))
MFonts.add_command(label="Magneto", font="Magneto", command=lambda: SetFont("Magneto"))
MFonts.add_command(label="Script", font="Script", command=lambda: SetFont("Script"))
MFonts.add_command(label="Symbol", font="Symbol", command=lambda: SetFont("Symbol"))
MFonts.add_command(label="Webdings", font="Webdings", command=lambda: SetFont("Webdings"))
MFonts.add_command(label="Wingdings", font="Wingdings", command=lambda: SetFont("Wingdings"))
MFonts.add_command(label="Wingdings 2", font="Wingdings 2", command=lambda: SetFont("Wingdings 2"))
MFonts.add_command(label="Wingdings 3", font="Wingdings 3", command=lambda: SetFont("Wingdings 3"))

MProperties = Menu(tearoff=0, bd=20, bg="#424242", fg="white")
MProperties.add_cascade(label="Size", menu=MSize)
MProperties.add_cascade(label="Size2", menu=MSize2)
MProperties.add_cascade(label="Colour", menu=MColor)
MProperties.add_cascade(label="Background", menu=MBackground)
MProperties.add_cascade(label="Fill", menu=MFill)
MProperties.add_cascade(label="Font", menu=MFonts)
MProperties.add_command(label="Text", command=PASS)

MCursor = Menu(tearoff=0, bd=20, bg="#424242", fg="white")
MCursor.add_command(label="Default(Arrow)", command=lambda: SetCursor("arrow"))
MCursor.add_command(label="Circle", command=lambda: SetCursor("circle"))
MCursor.add_command(label="Dot", command=lambda: SetCursor("dot"))
MCursor.add_command(label="Cross", command=lambda: SetCursor("cross"))
MCursor.add_command(label="Dotbox", command=lambda: SetCursor("dotbox"))
MCursor.add_command(label="Plus", command=lambda: SetCursor("plus"))
MCursor.add_command(label="Spraycan", command=lambda: SetCursor("spraycan"))
MCursor.add_command(label="Target", command=lambda: SetCursor("target"))
MCursor.add_command(label="Tcross", command=lambda: SetCursor("tcross"))
MCursor.add_separator()
MCursor.add_command(label="More", command=GetCursor)

MRightClick = Menu(tearoff=0, bd=20, bg="#424242", fg="white")
MRightClick.add_command(label="Remove last item", command=PASS)
MRightClick.add_command(label="Clear", command=lambda: Clear(ask=True))

M = Menu(MAIN)
M.add_cascade(label="Window", menu=MWindow)
M.add_cascade(label="Picture", menu=MFile)
M.add_cascade(label="Properties", menu=MProperties)
M.add_cascade(label="Figures", menu=MFigures)
M.add_cascade(label="Cursor", menu=MCursor)
M.add_cascade(label="Author", menu=MAuthor)
M.add_cascade(label="Languages", menu=MLanguage)

EM = Menu(MAIN)

C = Canvas(FrameC, background=bgcl)
# point = Point()
C.focus_set()
C.config(cursor=cursor)
C.bind('<Up>', PASS)
C.bind('<Down>', PASS)
C.bind('<Left>', PASS)
C.bind('<Right>', PASS)
C.bind("<Button-1>", PASS)
C.bind("<Button-3>", lambda e: MRightClick.post(e.x_root, e.y_root))
C.bind("<Motion>", PenEvMotion)
C.bind("<ButtonPress-1>", PenMouseDown1)
C.bind("<B1-Motion>", PenEvMotion)
C.bind("<ButtonRelease-1>", PenMouseUp1)
C.bind("<Enter>", lambda e, cl=cl, sz=sz: CreatePoint(e, cl, sz))
C.bind("<Leave>", EvLeave)
C.pack(fill=BOTH, expand=1)

AddTooltips()

FrameT.pack(side=TOP, fill="x")
FrameL.pack(side=LEFT, fill="y")
FrameR.pack(side=RIGHT, fill="y")
FrameC.pack(fill=BOTH, expand=1)
FrameB.pack(side=BOTTOM, fill="x")

MAIN.config(menu=M)
MAIN.mainloop()
