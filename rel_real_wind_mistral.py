# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 07:31:02 2020
@author: imkes
"""


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math


def wind(S,A,alpha,H,cog):
#S=seapathdata['SYS.CALC.SPEED_kmh']/3.6
#A=seapathdata['WEATHER.PBWWI.RelWindSpeed']
#alpha=seapathdata['WEATHER.PBWWI.RealWindDir']
#H=seapathdata['SEAPATH.PSXN.Heading']
#coghier=cog_test[0]
    awd=270-(H+alpha)
    c=90-cog #in degrees
    u=np.abs(A)*np.cos(awd/180. * math.pi)+np.abs(S)*np.cos(c/180. * math.pi)
    v=np.abs(A)*np.sin(awd/180. * math.pi)+np.abs(S)*np.sin(c/180. * math.pi)
    t=np.sqrt(u**2+v**2)
    twd=270-((180/np.pi)*np.arctan2(v,u))
    u=-t*np.sin(twd/180. * math.pi)
    v=-t*np.cos(twd/180. * math.pi)
    for i in range(0,len(twd)):#wenn funktion von diesem programm aufgerufen dann:len(twd)*60,60
        if twd[i] > 360.:
            twd[i]=twd[i]-360.
    return t,twd,u,v

#%%
#station='top'
#day=['23']#,'19','20','21','22','23','24']#['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
#month=['01']#['01','02','03']
#
#
#for m in month:
#    for d in day:
#        seapathfile='../../Eureka/Daten/Dship/seapath/2020'+m+d+'_DSHIP_all_1Hz.dat'
#        cogfile='../../Eureka/Daten/Dship/seapath/2020'+m+d+'cog_1Hz.dat'
#        seapathdata=pd.read_csv(seapathfile, delimiter='\t', decimal='.',skiprows=[1,2] ,engine='python')
#        cog=pd.read_csv(cogfile, delimiter='\t', decimal='.',skiprows=[1,2] ,engine='python')
#        ber_wind=wind(seapathdata['SYS.CALC.SPEED_kmh'][0::60]/3.6,seapathdata['WEATHER.PBWWI.RelWindSpeed'][0::60],seapathdata['WEATHER.PBWWI.RealWindDir'][0::60],seapathdata['SEAPATH.PSXN.Heading'][0::60], cog['SYS.STR.Course'][0::60])
#   #speed in knoten: sys.str.speed*100,rel windspeed in kn:*1.944
#plt.figure()
#plt.plot(ber_wind[0])
#plt.figure()
#plt.plot(seapathdata['WEATHER.PBWWI.TrueWindSpeed'][0::60])
#plt.figure()
#plt.plot(ber_wind[1],'*')
#plt.figure()
#plt.plot(seapathdata['WEATHER.PBWWI.TrueWindDir'][0::60],'*') 
#plt.figure()
#plt.plot(seapathdata['SYS.STR.Speed'][0::60])
#plt.figure()
#plt.plot(seapathdata['WEATHER.PBWWI.RelWindSpeed'][0::60])
#plt.figure()
#plt.plot(seapathdata['WEATHER.PBWWI.RealWindDir'][0::60],'*')