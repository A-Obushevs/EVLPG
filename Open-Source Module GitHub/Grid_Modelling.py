# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 15:06:56 2020

@author: lucag
"""
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 13:12:19 2020

@author: lucag
"""
#***********************************************************
# Import external library and define OpenDSS commands
#***********************************************************
import pandas as pd
from GUI import *
#from GUI_ import*
import os
#***********************************************************
# IMPORT GRID
#***********************************************************

percentage=percent
repetitions=repetition
EV_distribution=EVDistribution
pathEV=pathEV
pathRes=pathRes
MethodOfCalculation=MethodOfCalculation
NO_EV_Grid=NO_EV_Grid
NbrOfDistr=int(NbrOfDistr)
PercentPower=int(PercentPower)/100

if simulation == 1:
    
#*************************************************************************************************************************
# STEP 1: IMPORT EXCEL FILE OF ELEMENTS AND SLPs
#*************************************************************************************************************************
       
    dfSLP= pd.read_excel(pathSLP)   
    dfLines=pd.read_excel(pathGrid,"Lines")    
    dfLoads = pd.read_excel(pathGrid,"Loads")    
    dfTrafo=pd.read_excel(pathGrid,"Transformers")  
    dfGrid=pd.read_excel(pathGrid,"Ext Grid")
    
    # Define the number of loads in the grid model
    nbr_loads=len(dfLoads)
    nbr_lines=len(dfLines)
    nbr_trafos=len(dfTrafo)
    line_load=nbr_loads+nbr_lines
    line_2loads=line_load+nbr_loads
    Tot_elements=line_2loads+nbr_trafos
    
    for i in range(len(pathDSS)):
        char=pathDSS[len(pathDSS)-1-i]
    
        if char == '/':
            index=i
            pathElement = pathDSS[0:len(pathDSS)-index]
            break
    directory = pathElement
    files_in_directory = os.listdir(directory)
    filtered_files = [file for file in files_in_directory if file.endswith(".txt")]
    for file in filtered_files:
        path_to_file = os.path.join(directory, file)
        os.remove(path_to_file)
        
#********************************************************************************************************************
# STEP 2: DEFINE EMPTY ARRAY USED TO WRITE .txt FILES THAT CONTAINS GRID ELEMENTS
#********************************************************************************************************************
    #Create an empty vector from 0 to the number of loads.
    #This vector is used to store the parameters of each load
    loads=[0 for i in range(nbr_loads)]
    monitors=[0 for i in range(Tot_elements)] # Additional nbr_loads because for each load there are 2 monitors. 1 for voltage and the second for power
    
    lines=[0 for i in range(nbr_lines)]
    transformers=[[0  for i in range(3)] for i in range(len(dfTrafo))]
    Ext_Grid=[0 for i in range(len(dfGrid))]
    
#*************************************************************************************************************************
# STEP 3: DEFINE GRID ELEMENTS BASED ON INPUT DATA AND EXPORT IT IN TXT FILE FOR OPENDSS
#*************************************************************************************************************************

    #***********************************************************
    # DEFINE EXTERNAL GRID
    #***********************************************************
    for index_grid in range(len(Ext_Grid)):
        Ext_Grid= 'New circuit.'+dfGrid['Name'][index_grid]+' basekv='+str(dfGrid['Voltage [kV]'][index_grid])+' bus1='+dfGrid['bus'][index_grid]#+' pu='+str(dfGrid['Voltage [p.u]'][index_grid])+' bus1='+dfGrid['bus'][index_grid]+' MVAsc3='+str(dfGrid['MVAsc 3ph'][index_grid])+' MVAsc1='+str(dfGrid['MVAsc 1ph'][index_grid])
    
    # Write the .dss file used then in OpenDSS to define external grids
    ExtGrid_file = open(pathElement+"ExtGrid.txt","w")
    for i in range(len(Ext_Grid)):
        ExtGrid_file.write(Ext_Grid[i])
    ExtGrid_file.close()

    #***********************************************************
    # DEFINE TRANSFORMERS
    #***********************************************************
    
    for index_trafo in range(len(dfTrafo)):
        transformers[index_trafo][0]='New Transformer.'+str(dfTrafo['Name'][index_trafo])+' phases='+str(dfTrafo['phases'][index_trafo])+' Basefreq='+str(dfTrafo['Frequency'][index_trafo])+' XHL='+str(dfTrafo['XHL'][index_trafo])+' %loadloss='+str(dfTrafo['loadloss %'][index_trafo])+' %noloadloss='+str(dfTrafo['noloadloss %'][index_trafo])
        transformers[index_trafo][1]='~ wdg=1 bus='+str(dfTrafo['HV bus'][index_trafo])+' conn='+str(dfTrafo['HV conn'][index_trafo])+' kV='+str(dfTrafo['HV kV'][index_trafo])+' kVA='+str(dfTrafo['Snom kVA'][index_trafo])
        transformers[index_trafo][2]='~ wdg=2 bus='+str(dfTrafo['LV bus'][index_trafo])+' conn='+str(dfTrafo['LV conn'][index_trafo])+' kV='+str(dfTrafo['LV kV'][index_trafo])+' kVA='+str(dfTrafo['Snom kVA'][index_trafo])
    
    # Write the .dss file used then in OpenDSS to define transformer
    transformer_file = open(pathElement+"transformers.txt","w")
    for i in range(len(transformers)):
        transformer_file.write(transformers[i][0]+"\n"+transformers[i][1]+"\n"+transformers[i][2]+"\n")
    transformer_file.close()
    #***********************************************************
    # DEFINE LOAD SHAPES
    #***********************************************************
    SLPname=list()
    x=0
    for i in range(len(dfSLP.columns)):
        if 'P' in dfSLP.columns[i]:
            SLPname.insert(x,dfSLP.columns[i].replace('P',''))
            x=x+1
                
    npts=str(timeperiod)
    minterval=str(timestep)
    loadshape=[[0  for i in range(3)] for i in range(len(SLPname))]
    for index_loadshape in range(len(SLPname)):
        loadshape[index_loadshape][0] = "New Loadshape."+SLPname[index_loadshape]+" npts="+npts+" minterval="+minterval
        loadshape[index_loadshape][1]="~ mult="+str(tuple(dfSLP['P'+SLPname[index_loadshape]]))
        loadshape[index_loadshape][2]="~ Qmult="+str(tuple(dfSLP['Q'+SLPname[index_loadshape]]))
    
    # Write the .dss file used then in OpenDSS to define lines
    loadshape_file = open(pathElement+"Loadshape.txt","w")
    for i in range(len(loadshape)):
        loadshape_file.write(loadshape[i][0]+"\n"+loadshape[i][1]+"\n"+loadshape[i][2]+"\n")
    loadshape_file.close()
        
    #***********************************************************
    # DEFINE LOADS
    #***********************************************************
    
    # Assign to the vector loads the information of each load
    for index_load in range(nbr_loads):
        loads[index_load] = "New Load."+dfLoads["Name"][index_load]+" phases="+str(dfLoads["phases"][index_load])+" bus1="+str(dfLoads["Bus"][index_load])+" conn=wye kv=0.4 kw="+str(dfLoads["Pmax_PCC"][index_load])+" kvar="+str(dfLoads["Pmax_kVar"][index_load])+" daily="+str(dfLoads["class"][index_load])+' Vmaxpu=1.2 Vminpu=0.8'
    
    # Write the .dss file used then in OpenDSS to define loads
    loads_file = open(pathElement+"Loads.txt","w")
    for i in range(nbr_loads):
        loads_file.write(loads[i]+"\n")
    loads_file.close()
    
     #***********************************************************
    # DEFINE ENERGY METERS
    #***********************************************************
    index_EM=0
    EnergyMeter=list()
    for i in range(len(dfLines)):
        if dfLines['From'][i]==dfTrafo['LV bus'][0]:
            EnergyMeter.insert(index_EM, "New energymeter.EM"+str(index_EM)+" line."+dfLines['Name'][i]+"  1")
            index_EM=index_EM+1
    #EnergyMeter=pd.DataFrame(data=EnergyMeter)
    # Write the .dss file used then in OpenDSS to define loads
    EM_file = open(pathElement+"EM.txt","w")
    for i in range(len(EnergyMeter)):
        EM_file.write(EnergyMeter[i]+"\n")
    EM_file.close()   
    #***********************************************************
    # DEFINE LINES 
    #***********************************************************
    
    for index_line in range(nbr_lines):
        a="New Line."+str(dfLines["Name"][index_line])+" bus1="+str(dfLines["From"][index_line])+" bus2="+str(dfLines["To"][index_line])+" Length="+str(dfLines["Length"][index_line])
        b=" phases="+str(int(dfLines["nphases"][index_line]))+" units="+str(dfLines["Units"][index_line])+" BaseFreq=50 normamps="+str(dfLines["Fuse limit"][index_line])+" enabled="+str(dfLines["Service"][index_line])
        positive_seq=" R1="+str(dfLines["R(1)"][index_line])+" X1="+str(dfLines["X(1)"][index_line])+" C1="+str(dfLines["C(1)"][index_line])
        #zero_seq= " R0="+str(dfLines["R(0)"][index_line])+" X0="+str(dfLines["X(0)"][index_line])+" C0="+str(dfLines["C(0)"][index_line])
        lines[index_line] = a+b+positive_seq#+zero_seq
        
        if dfLines["Units"][index_line]=='km':
            ScailingFactorDistance=1000
        else:
            ScailingFactorDistance=1
    # Write the .dss file used then in OpenDSS to define lines
    lines_file = open(pathElement+"Lines.txt","w")
    for i in range(nbr_lines):
        lines_file.write(str(lines[i])+" \n")
    lines_file.close()
    
    #***********************************************************
    # DEFINE MONITORS FOR LOADS LINES AND TRANSFORMER
    #***********************************************************
    
    for index_monitor in range(nbr_lines):
            monitors[index_monitor] = "New monitor.Line_"+dfLines["Name"][index_monitor]+" element=Line."+dfLines["Name"][index_monitor]+" terminal=1 mode=0 ppolar=no"
    
    
    for index_monitor in range(nbr_lines,line_load):
        monitors[index_monitor] = "New monitor.VLoad_"+dfLoads["Name"][index_monitor-nbr_lines]+" element=Load."+dfLoads['Name'][index_monitor-nbr_lines]+" terminal=1 mode=0 ppolar=no"
    
    for index_monitor in range(line_load,line_2loads):
        monitors[index_monitor] = "New monitor.PLoad_"+dfLoads["Name"][index_monitor-line_load]+" element=Load."+dfLoads['Name'][index_monitor-line_load]+" terminal=1 mode=1 ppolar=no"


    for index_monitor in range(line_2loads, Tot_elements):
        monitors[index_monitor] = "New monitor.Trafo"+str(dfTrafo["Name"][index_monitor-line_2loads])+" element=transformer."+str(dfTrafo['Name'][index_monitor-line_2loads])+" terminal=1 mode=0 ppolar=no"
    
    
    # Write the .dss file used then in OpenDSS to define lines
    monitors_file = open(pathElement+"Monitor.txt","w")
    for i in range(len(monitors)):
        monitors_file.write(str(monitors[i])+"\n")
    monitors_file.close()
    
