# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 11:05:59 2020

@author: lucag
"""

from tkinter import *
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory
from PIL import ImageTk,Image


#***********************************************************
# GUI
#***********************************************************
# Definition of the function which allows to get a defined pattern+name of a file

def open_grid():
    enterGridName.delete(0,END)
    filename = askopenfilename()
    enterGridName.insert(0,filename)

def open_SLP():
    enterSLP.delete(0,END)
    filename = askopenfilename()
    enterSLP.insert(0,filename)

def open_DSS():
    enterDSS.delete(0,END)
    filename = askopenfilename()
    enterDSS.insert(0,filename)

def open_EVDistr():
    enterEV.delete(0,END)
    filename = askopenfilename()
    enterEV.insert(0,filename)
def open_Res():
    enterRes.delete(0,END)
    foldername = askdirectory()
    enterRes.insert(0,foldername)
    
#Define function to close the window
def close():
    global simulation
    simulation=0
    window.destroy()
    
def NoEVs():
    global simulation
    global pathGrid
    global pathSLP
    global timeperiod
    global timestep
    global pathDSS
    global export_result
    global repetition
    global percent
    global EVDistribution
    global pathEV
    global MethodOfCalculation
    global NO_EV_Grid
    global pathRes
    global NbrOfDistr
    global PercentPower
    NO_EV_Grid=1
    timestep=int(step.get())
    timeperiod=(60/timestep)*24*int(days.get())
    simulation=1
    pathGrid = GridPath.get()
    pathDSS = DSSPath.get()
    pathSLP= SLPPath.get()
    export_result=i.get()
    repetition=rep.get()
    percent=perc.get()
    EVDistribution=int(Distr.get())
    pathEV=EVPath.get()
    MethodOfCalculation=CalcMethod.get()
    pathRes=ResPath.get()
    NbrOfDistr=NbrDistr.get()
    PercentPower=PercPower.get()
    
    window.destroy()

def simulate():
    global simulation
    global pathGrid
    global pathSLP
    global pathRes
    global timeperiod
    global timestep
    global pathDSS
    global export_result
    global repetition
    global percent
    global EVDistribution
    global pathEV
    global MethodOfCalculation
    global NO_EV_Grid
    global NbrOfDistr
    global PercentPower
    NO_EV_Grid=0
    timestep=int(step.get())
    timeperiod=(60/timestep)*24*int(days.get())
    simulation=1
    pathGrid = GridPath.get()
    pathRes=ResPath.get()
    pathDSS = DSSPath.get()
    pathSLP= SLPPath.get()
    export_result=i.get()
    repetition=rep.get()
    percent=perc.get()
    EVDistribution=int(Distr.get())
    pathEV=EVPath.get()
    MethodOfCalculation=CalcMethod.get()
    NbrOfDistr=NbrDistr.get()
    PercentPower=PercPower.get()
    
    
    window.destroy()

#Creation of the main window
window = tk.Tk()
window.title('Open-source module for the investigation of the impact of EVs in a LV grid')
window.geometry("1080x720")
window.minsize(720,720)
#Icon
window.iconbitmap("./ZHAW_logo.ico")
# Background color
window.config(bg='#2774B2')

canvas = Canvas(window, width = 480, height = 198)
canvas.place(x=0,y=0)

img = ImageTk.PhotoImage(Image.open("ZHAW2.png"))
canvas.create_image(0, 0, anchor=NW, image=img)

# Define buttons
btn_open = tk.Button(window,width=20,bg='white', text="Select Grid", command=open_grid)
btn_open_2 = tk.Button(window,width=20,bg='white', text="Select SLP", command=open_SLP)
btn_open_3 = tk.Button(window,width=20,bg='white', text="Select OpenDSS File", command=open_DSS)
btn_open_4 = tk.Button(window,width=30,bg='white', text="Select External File\n(If External File or Mix are selected)", command=open_EVDistr)
btn_open_5 = tk.Button(window,width=20,bg='white', text="Select Results Folder", command=open_Res)
btn_simulate = tk.Button(window,width=20, text="Simulate",bg='#54CE15', command=simulate)
btn_simulate_noEV = tk.Button(window,width=20, text="Simulate Empty Grid",bg='#E6B512', command=NoEVs)
btn_close=tk.Button(window,width=20, text="Close",bg='#DC2412', command=close)
#Define enterbox variables
GridPath=StringVar(window,'     -- Please select the Grid file (*.xlsx ) --')
SLPPath=StringVar(window,'      -- Please select the SLP file (*.xlsx ) --')
DSSPath=StringVar(window,'      -- Please select the OpenDSS file (*.dss or *.txt ) --')
EVPath=StringVar(window,'       -- Please select the External file for EVs position file (*.xlsx ) --')
ResPath=StringVar(window,'      -- Please select the folder for results --')
days=StringVar(window,1)
step=StringVar(window,10)
rep=StringVar(window,1)
perc=StringVar(window,0)
NbrDistr=StringVar(window,1)
PercPower=StringVar(window,50)

#Define enterbox
enterGridName=Entry(window,width=70,textvariable=GridPath)
enterSLP=Entry(window,width=70,textvariable=SLPPath)
enterDSS=Entry(window,width=70,textvariable=DSSPath)
enterRes=Entry(window,width=70,textvariable=ResPath)
enterEV=Entry(window,width=70,textvariable=EVPath)
enterDays=Entry(window,width=5,textvariable=days)
enterStep=Entry(window,width=5,textvariable=step)
enterrep=Entry(window,width=5,textvariable=rep)
enterperc=Entry(window,width=5,textvariable=perc)
enterdistr=Entry(window,width=5,textvariable=NbrDistr)
enterpower=Entry(window,width=5,textvariable=PercPower)

#Definemultiple choice for results export
i = IntVar() #Basically Links Any Radiobutton With The Variable=i.
r1 = Radiobutton(window, text="Automatic", value=0, variable=i,bg='#2774B2')
r2 = Radiobutton(window, text="Manual", value=1, variable=i,bg='#2774B2')
r3 = Radiobutton(window, text="Mix", value=2, variable=i,bg='#2774B2')

Distr = IntVar() 
CalcMethod=IntVar()
d1 = Radiobutton(window, text="Grid", value=0, variable=Distr,bg='#2774B2')
d2 = Radiobutton(window, text="External file", value=1 , variable=Distr,bg='#2774B2')
d5 = Radiobutton(window, text="Mix", value=2 , variable=Distr,bg='#2774B2')
d3 = Radiobutton(window, text="All combos", value=1 , variable=CalcMethod,bg='#2774B2')
d4 = Radiobutton(window, text="Random", value=0 , variable=CalcMethod,bg='#2774B2')
d6 = Radiobutton(window, text="Algorithm", value=2 , variable=CalcMethod,bg='#2774B2')

# Define text
nbr_sim = tk.Label(window, width=20,text="Time period:", bg='#2774B2')
nbr_timestep = tk.Label(window, width=20,text="Time Step:", bg='#2774B2')
period_units = tk.Label(window, width=5,text="[Days]", bg='#2774B2')
step_units=tk.Label(window, width=10,text="[Minutes]", bg='#2774B2')
export_options=tk.Label(window,text="Analysis of results:", bg='#2774B2')
rep_units = tk.Label(window, width=5,text="[/]", bg='#2774B2')
perc_units = tk.Label(window, width=5,text="[%]", bg='#2774B2')
text_perc = tk.Label(window, width=25,text="Percentage of integration:", bg='#2774B2')
text_rep = tk.Label(window, width=20,text="Nbr of repetitions:", bg='#2774B2')
text_nbrDistr = tk.Label(window, width=20,text="--> Nbr of distributions:", bg='#2774B2')
text_percPower = tk.Label(window, width=20,text="--> Power Limitation [%]:", bg='#2774B2')

distr_options=tk.Label(window,text="Distribution of EVs:", bg='#2774B2')
calc_options=tk.Label(window,text="Calculation method:", bg='#2774B2')

#Place buttons
btn_open.place(x=5,y=225)
btn_open_2.place(x=5,y=270)
btn_open_3.place(x=5,y=320)
nbr_sim.place(x=5, y=410)
nbr_timestep.place(x=5, y=440)
btn_simulate.place(x=5,y=660)
btn_simulate_noEV.place(x=200,y=660)
btn_close.place(x=395,y=660) #470
btn_open_4.place(x=350,y=580)
btn_open_5.place(x=5,y=370)
#Place enterbox
enterGridName.place(x=200,y=225)
enterSLP.place(x=200,y=270)
enterDSS.place(x=200,y=320)
enterDays.place(x=200,y=410)
enterStep.place(x=200,y=440)
enterrep.place(x=200,y=470)
enterperc.place(x=580,y=540)
enterEV.place(x=580,y=590)
enterdistr.place(x=820,y=490)
enterRes.place(x=200,y=370)
enterpower.place(x=820,y=510)
#Place additional information
period_units.place(x=240,y=410)
step_units.place(x=240,y=440)
export_options.place(x=5,y=535)
text_perc.place(x=380,y=540)
text_rep.place(x=5,y=470)
perc_units.place(x=615,y=540)
rep_units.place(x=240,y=470)
distr_options.place(x=410,y=420)
calc_options.place(x=410,y=490)
text_nbrDistr.place(x=650,y=490)
text_percPower.place(x=660,y=510)
#Place Multiple choice
r1.place(x=200,y=510)
r2.place(x=200,y=535)
r3.place(x=200,y=560)

d1.place(x=580,y=400)
d2.place(x=580,y=420)
d5.place(x=580,y=440)
d3.place(x=580,y=470)
d4.place(x=580,y=490)
d6.place(x=580,y=510)

window.mainloop()
