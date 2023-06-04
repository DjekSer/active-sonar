import tkinter as tk
import math as mt
import turtle as t
import random as rm
from tkinter import ttk

## Основные параметры моделирования
vc = 1500
pi = 3.14159265358979
ti = 6
ts = 0.01
fd = 24000
fs = 5000
d = 1

## Создание окон интерфейса
win = tk.Tk()
win.title("Piw-Paw")
win.geometry('950x600')
                    
canvas1 = tk.Canvas(bg="white", width=800, height=400)
canvas1.place(y=0, x=0)
canvas2 = tk.Canvas(bg="gray", width=945, height=190)
canvas2.place(y=405, x=0)
#t = RawTurtle(canvas2)

screen = t.Screen()
screen.setup (1800, 700)
screen.bgcolor('white')
t.speed(10000)
t.tracer(0)
t.width(0.01)
t.penup()
t.goto(-400,0)
t.pendown()


## Обнуление вводимых данных
otau = [0, 0]
dist = 0
bear = 0
cour = 0

## Вызов команд по нажатию кнопки
def click_button():
    sig = coms.get()
    tar = comt.get()
    for i in range(len(btn)):
        global dist, bear, cour
        if i==0:
            dist = data[i].get()
        elif i==1:
            bear = data[i].get()
        elif i==2:
            cour = data[i].get()
    #signal(ti,fd,ts,fs,pi)
    zaderjka(dist, bear, cour, d, vc, fd, pi)
    risovalka(dist, bear, cour, pi)
    if tar == "Lodo4ka":
        target_L(otau, fd, ti, ts, dist, cour)
    elif tar == "Imitator":
        target_I(otau, fd, ti, ts, dist, cour)
    elif tar == "Cloud":
        target_C(otau, fd, ti, ts)

## Вводимые параметры моделирования
btn = ["Distance, m", "Bearing, deg", "Course angle, deg"]
dat = [0, 0, 0]
data = [0, 0, 0]

## Наполнение интерфейса
for a in range(len(btn)):
    tk.Label(text=btn[a], font=("Times New Roman", 12, "bold")) .place (y=10+60*a, x=810)
    data[a] = ttk.Entry()
    data[a].place (y=40+60*a, x=810)
     
tk.Button (text='FIRE', command=click_button, font=("Times New Roman", 12, "bold"),
    width=13).place(y=300, x=810)
     
st = ["Tonal" , "Noise", "AM-signal"]
coms = ttk.Combobox(values=st, width=18)
coms.place (y=200, x=810)
      
tt = ["Lodo4ka", "Imitator", "Cloud"]
comt = ttk.Combobox(values=tt, width=18)
comt.place (y=240, x=810)

canvas1.create_oval(2,2,798,798)
canvas1.create_oval(390,390,410,410,fill="red")

## Отображение расположения цели
def risovalka(dist, bear, cour, pi):
    x1 = mt.sin(pi*int(bear)/180)*int(dist)*400/4500 + 400
    y1 = -mt.cos(pi*int(bear)/180)*int(dist)*400/4500 + 400
    x2 = mt.sin(pi*(int(cour)-195)/180)*20 + x1
    y2 = -mt.cos(pi*(int(cour)-195)/180)*20 + y1
    x3 = mt.sin(pi*(int(cour)-165)/180)*20 + x1
    y3 = -mt.cos(pi*(int(cour)-165)/180)*20 + y1
    canvas1.create_polygon(x1,y1,x2,y2,x3,y3)

## Расчет задержек сигнала на приёмниках
def zaderjka(dist, bear, cour, d, vc, fd, pi):
    tau = [0,0]
    if int(bear) > 0:
        tau[0] = int(dist)*2/vc
        tau[1] = tau[0] + mt.sin(int(bear)*pi/180)*d/vc
    elif int(bear) < 0:
        tau[0] = int(dist)*2/vc
        tau[1] = tau[0] - mt.sin(int(bear)*pi/180)*d/vc
    elif int(bear) == 0:
        tau[0] = int(dist)*2/vc
        tau[1] = tau[0]
    global otau
    otau[0] = tau[0]*fd
    otau[1] = tau[1]*fd

## Формирование излучаемого сигнала с шумом (пока не используется)
def signal(ti,fd,ts,fs,pi):
    time_sig = [0]
    ns = [0]
    sg = [0]
    sg1 = [0]
    sg2 = [0]
    asig = 0
    
    for i in range (1, ti*fd):
        ns.append(rm.random())
    for p in range (1, int(ts*fd)):
        time_sig.append(time_sig[p-1] + 1/fd)
        sg.append(mt.sin(2*pi*fs*time_sig[p]))
    for d in range(int(ts*fd), ti*fd):
        sg.append(0)
    for k in range (0, ti*fd):
        asig = ns[k]/10 + sg[k]
    return(asig)

## Отраженный сигнал от ПЛ
def target_L(otau, fd, ti, ts, dist, cour):
    rast = abs(mt.sin(pi*(int(cour)-int(bear))/180)*200/1500)
    dec = int(dist)/4500 + 1
    
    sig1 = [0]
    for d in range(1, round(otau[0])):
        sig1.append(0)
    for i in range (round(otau[0]), round(otau[0])+int(ts*fd+rast*fd)):
        sig1.append(mt.sin(2*pi*fs*i/fd)/dec)
    for b in range(round(otau[0])+int(ts*fd+rast*fd), int(ti*fd)):
        sig1.append(0)
    for n in range (0, ti*fd):
        t.color('red')
        t.goto(n/fd*300-900, sig1[n]*250)
        
    sig2 = [0]    
    for d in range(1, round(otau[1])):
        sig2.append(0)
    for i in range (round(otau[1]), round(otau[1])+int(ts*fd+rast*fd)):
        sig2.append(mt.sin(2*pi*fs*i/fd)/dec)
    for b in range(round(otau[1])+int(ts*fd+rast*fd), int(ti*fd)):
        sig2.append(0)
        
    for n in range (0, ti*fd):
        t.color('green')
        t.goto(n/fd*300-900, sig2[n]*250)

## Отраженный сигнал от пары имитаторов
def target_I(otau, fd, ti, ts, dist, cour):
    rast = abs(mt.sin(pi*(int(cour)-int(bear))/180)*200/1500)
    otau_rast = rast*fd
    oafter = round(otau_rast) + int(ts*fd)
    
    sig1 = [0]
    for d in range(1, round(otau[0])):
        sig1.append(0)
    if round(otau_rast) <= int(ts*fd):
        for i in range (round(otau[0]), round(otau[0])+int(oafter)):
            sig1.append(mt.sin(2*pi*fs*i/fd))
        for b in range(round(otau[0])+int(oafter), int(ti*fd)):
            sig1.append(0)
    elif round(otau_rast) > int(ts*fd):
        for i in range (round(otau[0]), round(otau[0])+int(ts*fd)):
            sig1.append(mt.sin(2*pi*fs*i/fd))
        for p in range(round(otau[0])+int(ts*fd), round(otau[0])+round(otau_rast)):
            sig1.append(0)
        for s in range (round(otau[0])+round(otau_rast), round(otau[0])+int(oafter)):
            sig1.append(mt.sin(2*pi*fs*s/fd))          
        for b in range(round(otau[0])+int(oafter), int(ti*fd)):
            sig1.append(0)        
    for n in range (0, ti*fd):
        t.color('red')
        t.goto(n/fd*300-900, sig1[n]*250)
        
    sig2 = [0]    
    for d in range(1, round(otau[1])):
        sig2.append(0)
    if round(otau_rast) <= int(ts*fd):
        for i in range (round(otau[1]), round(otau[1])+int(oafter)):
            sig2.append(mt.sin(2*pi*fs*i/fd))
        for b in range(round(otau[1])+int(oafter), int(ti*fd)):
            sig2.append(0)
    elif round(otau_rast) > int(ts*fd):
        for i in range (round(otau[1]), round(otau[0])+int(ts*fd)):
            sig2.append(mt.sin(2*pi*fs*i/fd))
        for p in range(round(otau[1])+int(ts*fd), round(otau[1])+round(otau_rast)):
            sig2.append(0)
        for s in range (round(otau[1])+round(otau_rast), round(otau[1])+int(oafter)):
            sig2.append(mt.sin(2*pi*fs*s/fd))          
        for b in range(round(otau[1])+int(oafter), int(ti*fd)):
            sig2.append(0)
    for n in range (0, ti*fd):
        t.color('green')
        t.goto(n/fd*300-900, sig2[n]*250)

## Отраженный сигнал от облака осколков/мелких_объектов/пассивных_имитаторов
def target_C(otau, fd, ti, ts):
    sig1 = [0]
    for d in range(1, round(otau[0])):
        sig1.append(0)
    for i in range (round(otau[0]), round(otau[0])+int(ts*fd+0.1*fd)):
        sig1.append(mt.sin(2*pi*fs*i/fd)*0.6)
    for b in range(round(otau[0])+int(ts*fd+0.1*fd), int(ti*fd)):
        sig1.append(0)
    for n in range (0, ti*fd):
        t.color('red')
        t.goto(n/fd*300-900, sig1[n]*250)
        
    sig2 = [0]    
    for d in range(1, round(otau[1])):
        sig2.append(0)
    for i in range (round(otau[1]), round(otau[1])+int(ts*fd+0.1*fd)):
        sig2.append(mt.sin(2*pi*fs*i/fd)*0.6)
    for b in range(round(otau[1])+int(ts*fd+0.1*fd), int(ti*fd)):
        sig2.append(0)
    for n in range (0, ti*fd):
        t.color('green')
        t.goto(n/fd*300-900, sig2[n]*250)  
           
win.mainloop()
