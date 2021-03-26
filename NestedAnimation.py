"""
NestedAnimation - Python Tkinter
By A.D.Tejpal - 26-Mar-2021

This progam demonstrates bouncing shapes as well as a center
piece having animation within animation.

Binding of mouse click event is also covered.

Mouse Control:
Single Click: Toggle Different Styles Of Central Shape
Double Click: Toggle Stop / Start Of  Animation.
"""
import tkinter as tk

canv_wd=800
canv_ht=560
time_delay=50

def run():
    global canv_wd, canv_ht, time_delay
    global mlist
    
    root = tk.Tk()
    root.title("Nested Animation And Bouncing Shapes")
    canv = tk.Canvas(root, width=canv_wd, height=canv_ht)
    canv.pack()

    # bind left mouse click-single
    canv.bind('<Button-1>', lambda e:canv_click(e,"sclick"))

    # bind left mouse click-ddouble
    canv.bind('<Double-1>', lambda e:canv_click(e,"dclick"))

    mlist = [{"canv":canv, "canv_wd":canv_wd,
        "canv_ht":canv_ht, "time_delay":time_delay,
        "cnum":1, "cwd":20, "cht":20, "cgrow":True,
        "move":True, "arc_start":0, "arc_ang":50, "arc_step":10}]

    ct = 0
    for s in [{"shape_code":"r", "shape_wd":15,
        "shape_ht":10, "shape_step":5},
        {"shape_code":"o", "shape_wd":40,
         "shape_ht":30, "shape_step":1}]:

        for clr in ["blue", "red", "green", "black"]:
            d = {}
            d.update(s)
            d["shape_clr"]=clr
            d["shape_left"]=50*ct
            d["shape_top"]=30*ct
            d["goingR"]=True
            d["goingD"]=False            

            ct = ct + 1
            mlist.append(d)
            
    animate_a()
    root.mainloop()

def animate_a():
    global mlist

    cdict = mlist[0]
    canv = cdict["canv"]
    move = cdict["move"]

    animate_b()
    redraw_all()

    if move:
        time_delay = cdict["time_delay"]
        canv.after(time_delay, animate_a)
 
def animate_b():
    global mlist

    cdict = mlist[0]
    for mdict in mlist[1:]:
        if mdict["goingR"]:
            if (mdict["shape_left"] + mdict["shape_wd"]
                > cdict["canv_wd"]):
                mdict["goingR"] = False
            else:
                move_right(mdict)
        else:
            if (mdict["shape_left"] < 0): 
                mdict["goingR"] = True
            else:
                move_left(mdict)

        if mdict["goingD"]:
            if (mdict["shape_top"] + mdict["shape_ht"]
                > cdict["canv_ht"]):
                mdict["goingD"] = False
            else:
                move_down(mdict)
        else:
            if (mdict["shape_top"] < 0):
                mdict["goingD"] = True
            else:
                move_up(mdict)

def move_left(mdict):
    mdict["shape_left"] -= mdict["shape_step"]

def move_right(mdict):
    mdict["shape_left"] += mdict["shape_step"]

def move_up(mdict):
    mdict["shape_top"] -= mdict["shape_step"]

def move_down(mdict):
    mdict["shape_top"] += mdict["shape_step"]

def redraw_all():
    global canv_wd, canv_ht
    global mlist

    cdict = mlist[0]
    canv = cdict["canv"]
    canv.delete("all")

    txt_x_factor= 0.05
    txt_y_factor= 0.95
    txt_coords = (int(txt_x_factor * canv_wd),
                int(txt_y_factor * canv_ht))
    msg = "Mouse Control:\n" \
        + "Single Click: Toggle Central Shape Style" \
        + "\nDouble Click: Toggle Stop / Start"
    canv.create_text(txt_coords, 
        text=msg, font=("Times", 16), anchor="sw")
    
    cnum = cdict["cnum"]
    cgrow = cdict["cgrow"]
    cwd = cdict["cwd"]
    cht = cdict["cht"]
    canv_wd = cdict["canv_wd"]
    canv_ht = cdict["canv_ht"]
    cx1 = int((canv_wd - cwd)/2)
    cx2 = cx1 + cwd
    cy1 = int((canv_ht - cht)/2)
    cy2 = cy1 + cht

    if cnum == 1:
        canv.create_rectangle(cx1,cy1,cx2,cy2,
            fill="light grey", width=5)
    elif cnum == 2:
        canv.create_rectangle(cx1,cy1,cx2,cy2,
            fill="white", width=5)
    else:
        canv.create_rectangle(cx1,cy1,cx2,cy2,
            fill="light blue", width=5)

    ang = cdict["arc_ang"]
    st = cdict["arc_start"]
    canv.create_arc(cx1,cy1,cx2,cy2,
        start=st, extent=ang, fill="red")
    canv.create_arc(cx1,cy1,cx2,cy2,
        start=st+ang, extent=ang, fill="blue")
    canv.create_arc(cx1,cy1,cx2,cy2,
        start=st+2*ang, extent=ang, fill="purple")
    canv.create_arc(cx1,cy1,cx2,cy2,
        start=st+3*ang, extent=ang, fill="green")
    canv.create_arc(cx1,cy1,cx2,cy2,
        start=st+4*ang, extent=ang, fill="black")
    cdict["arc_start"] = cdict["arc_start"] + cdict["arc_step"]

    if cwd > (canv_wd - 10) or cht > (canv_ht - 10):
        cdict["cgrow"] = False
    
    if cwd < 20 or cht < 20:
        cdict["cgrow"] = True

    if cgrow:
        cdict["cwd"] = cdict["cwd"] + 2
        cdict["cht"] = cdict["cht"] + 2
    else:
        cdict["cwd"] = cdict["cwd"] - 2
        cdict["cht"] = cdict["cht"] - 2

    for mdict in mlist[1:]:
        mx1 = mdict["shape_left"]
        my1 = mdict["shape_top"]
        mx2 = mx1 + mdict["shape_wd"]
        my2 = my1 + mdict["shape_ht"]
        clr = mdict["shape_clr"]
        shape_code = mdict["shape_code"]
        
        if shape_code=="r":
            canv.create_rectangle(mx1,my1,mx2,my2, fill=clr)
        else:
            canv.create_oval(mx1,my1,mx2,my2, fill=clr)

def canv_click(event, mode):
    global mlist

    cdict = mlist[0]

    if mode == "sclick":
        if cdict["cnum"] == 1:
            cdict["cnum"] = 2
            cdict["cwd"] = 200
            cdict["cht"] = 2
        elif cdict["cnum"] == 2:
            cdict["cnum"] = 3
            cdict["cwd"] = 5
            cdict["cht"] = 180
        else:
            cdict["cnum"] = 1
            cdict["cwd"] = 20
            cdict["cht"] = 20            

        cdict["cgrow"] = True
    else:
        move = cdict["move"]
        if move:
            cdict["move"] = False
        else:
            cdict["move"] = True
            animate_a()
#======================
run()
