# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 11:26:52 2020

@author: imkes
"""


import numpy as np
import pandas as pd
#import os, re
import rel_real_wind as rw
import math
from pandas.tseries.frequencies import to_offset
import matplotlib.pyplot as plt
import sys

day_min, day_max = int(sys.argv[1]), int(sys.argv[2])
print(day_min,day_max)
month= int(sys.argv[3])
# print(month)
day_arr=np.arange(day_min,day_max+1,1)
day=list((day_arr))    
# day=['18','19','20','21','22','23','24','25','26','27','28','29','30','31']#['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17',
month=['%02d' %(month)]#['01']#['01','02','03']
station=str(sys.argv[4])#['bug']
station1=str(sys.argv[5])#'BUG'


varpath='/mnt/lustre02/work/um0203/u301025/Variablen/'
cd = '/mnt/lustre02/work/um0203/u301025/Masterarbeit/Eureka/Daten/'+station+'/Level0b_RawData20HzDaily/'

for m in month:
    for d in day: 
        #ab dem 27.01. gibt es bei seapathdata 10 hz daten!
#        dann: seapathfile=10hz
#        trotzdem:
#        seapathdata=seapathdata.resample('0.05S').asfreq()...
        seapathfile='/mnt/lustre02/work/um0203/u301025/Masterarbeit/Eureka/Daten/Dship/seapath/2020'+m+str(d)+'_DSHIP_all_1Hz.dat'
        seapathdata=pd.read_csv(seapathfile, delimiter='\t', decimal='.',skiprows=[1,2] ,engine='python')
        cogfile='/mnt/lustre02/work/um0203/u301025/Masterarbeit/Eureka/Daten/Dship/seapath/2020'+m+str(d)+'cog_1Hz.dat'
        cog=pd.read_csv(cogfile, delimiter='\t', decimal='.',skiprows=[1,2] ,engine='python')
        cog['X']=(float(seapathdata['SYS.CALC.SPEED_kmh'])/3.6)*np.sin((float(cog['SYS.STR.Course']))/180. * math.pi)
        cog['Y']=(float(seapathdata['SYS.CALC.SPEED_kmh'])/3.6)*np.cos((float(cog['SYS.STR.Course']))/180. * math.pi)
        # cog['date']=cog['date time'][:].astype('datetime64[ns]')
        cog['date']=pd.to_datetime(cog['date time'])
        cog.set_index(['date'],drop=True,append=False,inplace=True)
        cog=cog.resample('50L').asfreq()
        loffset = '1S'
        cog1=cog
        cog1.index = cog1.index + to_offset(loffset)
        cog=cog.append(cog1[1727961:-1])
        cog=cog.reset_index()
        cog.loc[1727981:,'X']=cog.loc[1727980,'X']
        cog.loc[1727981:,'Y']=cog.loc[1727980,'Y']
        cog['X']=cog['X'].interpolate(method='slinear')
        cog['Y']=cog['Y'].interpolate(method='slinear')
        cog['SYS.STR.Course_test']=(180./np.pi)*np.arctan2(cog['X'], cog['Y'])
        # cog_test=np.zeros((len(cog['SYS.STR.Course_test'])))
        # for i in range(0,len(cog['SYS.STR.Course_test'])):
        #     #print(i)
        #     if cog.loc[i]['SYS.STR.Course_test'] < 0.:
        #        cog_test[i]=cog.loc[i]['SYS.STR.Course_test']+360.
        #     else:
        #        cog_test[i]=cog.loc[i]['SYS.STR.Course_test']  
        # cog_test=pd.DataFrame(cog_test)   
        cog.loc[np.where(cog['SYS.STR.Course_test'] < 0.)]['SYS.STR.Course_test']=cog.loc[np.where(cog['SYS.STR.Course_test'] < 0.)]['SYS.STR.Course_test']+360.
        #auf 10 hz bringen
        seapathdata['date']=seapathdata['date time'][:].astype('datetime64[ns]')
        seapathdata.set_index(['date'],drop=True,append=False,inplace=True)
        seapathdata=seapathdata.resample('50L').asfreq()
        seapathdata1=seapathdata.resample('50L').asfreq()
        seapathdata1.index = seapathdata1.index + to_offset(loffset)
        seapathdata=seapathdata.append(seapathdata1[1727961:])
        seapathdata=seapathdata.reset_index()
        seapathdata=seapathdata.interpolate(method='slinear')
        seapathdata=seapathdata.drop(seapathdata.index[len(seapathdata)-1]) 
#        for i in range(2,len(seapathdata.loc[0][:])):
#            seapathdata.loc[1727981:][i]=seapathdata.loc[1727980][i]
#        plt.figure()
#        plt.plot(cog['SYS.STR.Course'],'*')
        
#        i = 0
#        dfList = []
#        for root, dirs, files in os.walk(cd,topdown=True):
#            for fname in files:
#                if re.match("2020"+m+d+"-U"+station1, fname):
#                    frame = pd.read_csv(os.path.join(root, fname), delimiter=";", decimal='.')
#                    frame['key'] = "file{}".format(i)
#                    dfList.append(frame)    
#                    i += 1
#                    print(root)
#                    usatdata= pd.concat(dfList,ignore_index=True)
                    #despiking und maske: anstelle von gesamten daten einlesen nur flag einlesen und dort die columns mit daten rausziehen        
        usatdata=pd.read_csv(varpath+'despiking_{day}{month}_{station}.csv'.format(day=str(d),month=m,station=station))
        # usatdata=flag
        usatdata=usatdata.drop(['Unnamed: 0','X_mask', 'Y_mask', 'Z_mask', 'T_mask', 'CC_mask','CH_mask','V_mask','D_mask','AX_mask','AY_mask','AZ_mask'],axis=1)
        usatdata['Xrel']=usatdata['X']
        usatdata['Yrel']=usatdata['Y']
        usatdata['Zrel']=usatdata['Z']
        #absoluter Wind
        #ber_wind_vgl=rw.wind(seapathdata['SYS.CALC.SPEED_kmh']/3.6,
        #                 seapathdata['WEATHER.PBWWI.RelWindSpeed'],
        #                 seapathdata['WEATHER.PBWWI.RealWindDir'],
        #                 seapathdata['SEAPATH.PSXN.Heading'], cog_test[0])
        #                ##
        unterschied=usatdata.D-seapathdata['WEATHER.PBWWI.RealWindDir']
        test_1=unterschied.where(usatdata.D > 170.)
        test_1=test_1.where(usatdata.D  <190.)
        mittel_obere=np.mean(test_1.where(test_1 >100.))
        versuch=usatdata.D-mittel_obere
        for i in range(0,len(versuch)):
            if versuch[i] <0.:
                versuch[i]=versuch[i]+360.
        usatdata['D_metsystem']=versuch
                
        ber_wind=rw.wind(seapathdata['SYS.CALC.SPEED_kmh']/3.6,
                         usatdata['V'],
                         usatdata['D_metsystem'],
                         seapathdata['SEAPATH.PSXN.Heading'], cog['SYS.STR.Course_test'])
        
        #wie ist der unterschied der Messungen der Meteor und unserer Messungen?

        #plt.figure()
        #plt.plot(ber_wind_vgl[0]-ber_wind[0],'*')
        #plt.savefig(abb_path+station+'speedvgl-speed{day1}{month1}'.format(day1=d,month1=m))
        #plt.figure()
        #plt.plot(ber_wind_vgl[1]-ber_wind[1],'*')
        #plt.savefig(abb_path+station+'dirvgl-dir{day1}{month1}'.format(day1=d,month1=m))
        #plt.figure()
        #plt.plot(seapathdata['WEATHER.PBWWI.RelWindSpeed']-usatdata['V'],'*')
        #plt.savefig(abb_path+station+'difspeed{day1}{month1}'.format(day1=d,month1=m))
        #plt.figure()
        #plt.plot(seapathdata['WEATHER.PBWWI.RealWindDir']-usatdata['D_metsystem'],'*')
        #plt.savefig(abb_path+station+'difdir{day1}{month1}'.format(day1=d,month1=m))
        #dif_speed=seapathdata['WEATHER.PBWWI.RelWindSpeed']-usatdata['V']
        #dif_dir=seapathdata['WEATHER.PBWWI.RealWindDir']-usatdata['D_metsystem']
        #dif_berwindspeed=ber_wind_vgl[0]-ber_wind[0]
        #dif_berwinddir=ber_wind_vgl[1]-ber_wind[1]
        
        usatdata['X']=ber_wind[2]
        usatdata['Y']=ber_wind[3]
        usatdata['real_winddir']=ber_wind[1]
        usatdata['real_windvel']=ber_wind[0]
        usatdata['EU']=-np.sin(usatdata['real_winddir'])
        usatdata['EV']=-np.cos(usatdata['real_winddir'])
        usatdata['XZ']=usatdata['X']*usatdata['Z']
        usatdata['XY']=usatdata['X']*usatdata['Y']
        usatdata['YZ']=usatdata['Y']*usatdata['Z']
        usatdata['rho']=1.29227*273.16/(usatdata['T']+273.15)
        usatdata['rhoco2']=usatdata.CC*44.01*1e-06 #in kg m-3
        usatdata['rhoh2o']=usatdata.CH*18.015*1e-06
        Rw=461.45 #j/kg K
        Rl=287.05#j/kg K
        usatdata['q']=usatdata['rhoh2o']/(usatdata['rhoh2o']+((101.3*1e03-(usatdata['rhoh2o']*Rw*(usatdata['T']+273.15)))/(Rl*(usatdata['T']+273.15))))
        usatdata['ZH2O']=usatdata['Z']*usatdata['rhoh2o']
        usatdata['ZCO2']=usatdata['Z']*usatdata['rhoco2']
        usatdata['ZT']=usatdata['Z']*(usatdata['T']+273.15)
        usatdata.to_csv(varpath+station+'usatdata_{day}{month}.csv'.format(day=str(d),month=m))
        
        #mean über 30 min
        meanval=usatdata.groupby(np.arange(len(usatdata.index))//(20*1800)).mean()
        meanval.D=(np.arctan2(-meanval.EU,-meanval.EV)+np.pi)*180./np.pi
        meanvalnew=pd.DataFrame(np.repeat(meanval.values,(20*1800),axis=0))
        meanvalnew.columns = meanval.columns
        meanval.to_csv(varpath+station+'meanval_{day}{month}.csv'.format(day=str(d),month=m))
        
        abw=usatdata-meanvalnew
        abw.to_csv(varpath+station+'abw_{day}{month}.csv'.format(day=str(d),month=m))