# -*- coding: utf-8 -*-
"""
Spyder Editor

Dies ist eine temporäre Skriptdatei.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import calendar
import datetime
#from matplotlib.dates import HourLocator
from time import gmtime,strftime
import sys

abb_path='/mnt/lustre02/work/um0203/u301025/Abbildungen/Fluxes/'
varpath='/mnt/lustre02/work/um0203/u301025/Variablen/'
# cd = '/mnt/lustre02/work/um0203/u301025/Masterarbeit/Eureka/Daten/'+station+'/Level0b_RawData20HzDaily/'
day_min, day_max = int(sys.argv[1]), int(sys.argv[2])
print(day_min,day_max)
month= int(sys.argv[3])
# print(month)
day_arr=np.arange(day_min,day_max+1,1)
day=list((day_arr))    
# day=['18','19','20','21','22','23','24','25','26','27','28','29','30','31']#['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17',
month=['%02d' %(month)]#['01']#['01','02','03']
station=str(sys.argv[4])#['bug']
# station1=str(sys.argv[5])#'BUG'
anz=len(day)*len(month)

fco2=np.zeros((48,len(day),len(month)))
fh2o=np.zeros((48,len(day),len(month)))
fmom=np.zeros((48,len(day),len(month)))
fmom2=np.zeros((48,len(day),len(month)))
fsen=np.zeros((48,len(day),len(month)))
flat=np.zeros((48,len(day),len(month)))

Fco2=np.zeros(48*len(day)*len(month))
Fh2o=np.zeros((48*len(day)*len(month)))
Fmom=np.zeros((48*len(day)*len(month)))
Fmom2=np.zeros((48*len(day)*len(month)))
Fsen=np.zeros((48*len(day)*len(month)))
Flat=np.zeros((48*len(day)*len(month)))
a=0
cp=1004.8 #j/kg K
Rw=461.45 #j/kg K
Rl=287.05#j/kg K

for m in month:
    for d in day:
#            fname1='../../Eureka/Daten/'+station+'/Level0b_RawData20HzDaily/E4C_METEOR_UBUG_RAW_DAYS_2020'+m+d+'/2020'+m+d+'-UBUG'
#'../data/Bug/2020'+m+d+'-'+z+'0000-UTC-UBUG-COM1.raw' #18.01/20200118-'+z+'0000-UTC-UBUG-COM1.raw'
#            fname2='../data/Bug/2020'+m+d+'-'+z+'0000-UTC-LBUG-COM3.raw''
            j=day.index(str(d))
            # k=month.index(m)
#            interval=[0,len(usatdata['E3'])/2,len(usatdata['E3'])]
            
#        usatdata entspricht meanval(30min)
            usatdata =pd.read_csv(varpath+station+'meanval_'+str(d)+m+'.csv', delimiter=",", decimal='.')
#            licordata =pd.read_csv(fname2, delimiter=";", skiprows=1, skipfooter=4, decimal=',', engine='python')
  
#            usatdata.iloc[np.flatnonzero(usatdata['D']>210.),:]=np.nan
#            usatdata.iloc[np.flatnonzero(usatdata['D']<150.),:]=np.nan
#            licordata.iloc[np.flatnonzero(usatdata['D']>210.),:]=np.nan
#            licordata.iloc[np.flatnonzero(usatdata['D']<150.),:]=np.nan
            Lv=2501000-2370*usatdata['T'] #J/kg
#            sinphi=usatdata['Z'][:]/(np.sqrt((usatdata['X'][:])**2+(usatdata['Y'][:])**2+usatdata['Z'][:]**2))
#            cosphi=np.sqrt(((usatdata['X'][:]))**2+((usatdata['Y'][:]))**2)/(np.sqrt(((usatdata['X'][:]))**2+((usatdata['Y'][:]))**2+((usatdata['Z'][:]))**2))
#            sigmaz=np.sqrt((usatdata['Z'][:]**2)-(usatdata['Z'][:])**2)
#            sigmax=np.sqrt((usatdata['X'][:]**2)-(usatdata['X'][:])**2)
#            sigmay=np.sqrt((usatdata['Y'][:]**2)-(usatdata['Y'][:])**2)
#            teta=np.arctan2((usatdata['X'][:]),(usatdata['Y'][:]))
#            sigmaxy=(usatdata['XY'][:])-(usatdata['X'][:])*(usatdata['Y'][:])
#            sigmaxz=(usatdata['XZ'][:])-(usatdata['X'][:])*(usatdata['Z'][:])
#            sigmayz=(usatdata['YZ'][:])-(usatdata['Y'][:])*(usatdata['Z'][:])
#            sigmal=np.sqrt(sigmay**2*np.cos(teta)**2+2*sigmaxy*np.sin(teta)*np.cos(teta)+sigmax**2*np.sin(teta)**2)
#            sigmalz=sigmaxz*np.sin(teta)+sigmayz*np.cos(teta)
#            uschub=sigmalz*(sinphi**2-cosphi**2)+(sigmal**2-sigmaz**2)*sinphi*cosphi
#            uschub2=np.sqrt(np.sqrt((usatdata['XZ'][:]-usatdata['X']*usatdata['Z'])**2+(usatdata['YZ'][:]-usatdata['Y']*usatdata['Z'])**2))

            #Flüsse
            fco2[:,j]=((usatdata['ZCO2'][:])-((usatdata['Z'][:])*(usatdata['rhoco2'][:])))*1e06 #mg/m2s
            fh2o[:,j]=((usatdata['ZH2O'][:])-((usatdata['Z'][:])*(usatdata['rhoh2o'][:])))*1e06 #mg/m2s
            fsen[:,j]=(usatdata['rho'][:])*cp*(usatdata['ZT'][:]-(usatdata['Z'][:]*(usatdata['T'][:]+273.15))) #w/m2
            #kommender ausdruck ergibt das gleiche wie fmom
             #fmom1[:,j,k]=-(usatdata['rho'][:])*uschub2[:]**2
             
##           fmom2[:,j,k]=-(usatdata['rho'][:])*(usatdata['XZ'])-((usatdata['X'])*(usatdata['Z']))

            fmom[:,j]=(usatdata['rho'][:])*np.sqrt((usatdata['XZ'][:]-usatdata['X']*usatdata['Z'])**2+(usatdata['YZ'][:]-usatdata['Y']*usatdata['Z'])**2)
            flat[:,j]=Lv*fh2o[:,j]/1e06
           
            Fco2[a:(a+48)]=fco2[:,j]
            Fh2o[a:(a+48)]=fh2o[:,j]
            Fsen[a:(a+48)]=fsen[:,j]
            Fmom[a:(a+48)]=fmom[:,j]
#            Fmom2[a:(a+48)]=fmom2[:,j,k]
            Flat[a:(a+48)]=flat[:,j]
        
            a=a+48
achse=[]
date = datetime.datetime(2020, int(month[0]), int(day[0]))
bla=calendar.timegm(date.timetuple())
#für 00, 06,12,18uhr abstände, also wenn nur 1-2 tage geplottet werden
#for e in range(0,48*len(day)*len(month)*3600,6*3600):
#    achse.append(strftime("%H:%M", gmtime(e)))
  #nur datum, also wenn nur mehr tage geplottet werden  
for e in range(0,48*len(day)*len(month)*3600,24*3600):
    achse.append(strftime("%d.%m", gmtime(e+bla)))  

fig=plt.figure(4)      
ax1 = fig.add_subplot(1,1,1) 
ax1.plot(Fco2[:])
ax1.set_title('CO2 flux from {day1}.{month1} to {day2}.{month2}'.format(day1=day[0],month1=month[0],day2=str(d),month2=m),fontsize=12)
ax1.set_ylabel('CO2 flux/mg s-1 m-2',fontsize=12)
ax1.set_xlabel('time',fontsize=12)
ax1.set_xticks(np.arange(0,48*len(day)*len(month),48))#12statt 48
ax1.set_xticklabels(achse[:])
#ax1.set_ylim(-1,1)
#ax1.set_xticklabels(day[:])
plt.savefig(abb_path+station+'co2_30min_{day1}{month1}-{day2}{month2}'.format(day1=day[0],month1=month[0],day2=str(d),month2=m))
plt.figure(5)
plt.plot(Fh2o[:])
plt.title('H2O flux from {day1}.{month1} to {day2}.{month2}'.format(day1=day[0],month1=month[0],day2=d,month2=m),fontsize=12)
plt.ylabel('H2O flux/mg s-1 m-2',fontsize=12)
plt.xlabel('time',fontsize=12)
plt.xticks(np.arange(0,48*len(day)*len(month),48),achse[:])
#plt.xticks(np.arange(0,48*len(day)*len(month),48),day[:])
plt.savefig(abb_path+station+'h2o_30min_{day1}{month1}-{day2}{month2}'.format(day1=day[0],month1=month[0],day2=str(d),month2=m))
plt.figure(9)
plt.plot(Flat[:])
plt.title('latent heat flux from {day1}.{month1} to {day2}.{month2}'.format(day1=day[0],month1=month[0],day2=str(d),month2=m),fontsize=12)
plt.ylabel('latent heat flux/W m-2',fontsize=12)
plt.xlabel('time',fontsize=12)
plt.xticks(np.arange(0,48*len(day)*len(month),48),achse[:])
#plt.xticks(np.arange(0,48*len(day)*len(month),48),day[:])
plt.savefig(abb_path+station+'lat_30min_{day1}{month1}-{day2}{month2}'.format(day1=day[0],month1=month[0],day2=str(d),month2=m))
plt.figure(6)
plt.plot(Fmom[:])
plt.title('momentum flux from {day1}.{month1} to {day2}.{month2}'.format(day1=day[0],month1=month[0],day2=str(d),month2=m),fontsize=12)
plt.ylabel('momentum flux/N m-2',fontsize=12)
plt.xlabel('time',fontsize=12)
plt.xticks(np.arange(0,48*len(day)*len(month),48),achse[:])
#plt.xticks(np.arange(0,48*len(day)*len(month),48),day[:])
plt.savefig(abb_path+station+'momentum_30min_{day1}{month1}-{day2}{month2}'.format(day1=day[0],month1=month[0],day2=str(d),month2=m))
#plt.figure(7)
#plt.plot(Fmom2[:])
#plt.title('momentum flux 2 from {day1}.{month1} to {day2}.{month2}'.format(day1=day[0],month1=month[0],day2=d,month2=m),fontsize=12)
#plt.ylabel('momentum flux/N m-2',fontsize=12)
#plt.xlabel('hours',fontsize=12)
plt.figure(8)
plt.plot(Fsen[:])
plt.title('sensible heat flux from {day1}.{month1} to {day2}.{month2}'.format(day1=day[0],month1=month[0],day2=str(d),month2=m),fontsize=12)
plt.ylabel('sensible heat flux/W m-2',fontsize=12)
plt.xlabel('time',fontsize=12)
plt.xticks(np.arange(0,48*len(day)*len(month),48),achse[:])
#plt.xticks(np.arange(0,48*len(day)*len(month),48),day[:])
plt.savefig(abb_path+station+'sens_30min_{day1}{month1}-{day2}{month2}'.format(day1=day[0],month1=month[0],day2=str(d),month2=m))

np.save(varpath+station+'fh2o_{day1}{month1}-{day2}{month2}'.format(day1=day[0],month1=month[0],day2=str(d),month2=m), fh2o[:,:,:])
np.save(varpath+station+'fco2_{day1}{month1}-{day2}{month2}'.format(day1=day[0],month1=month[0],day2=str(d),month2=m), fco2[:,:,:])
np.save(varpath+station+'fmom_{day1}{month1}-{day2}{month2}'.format(day1=day[0],month1=month[0],day2=str(d),month2=m), fmom[:,:,:])
np.save(varpath+station+'fsen_{day1}{month1}-{day2}{month2}'.format(day1=day[0],month1=month[0],day2=str(d),month2=m), fsen[:,:,:])
np.save(varpath+station+'flat_{day1}{month1}-{day2}{month2}'.format(day1=day[0],month1=month[0],day2=str(d),month2=m), flat[:,:,:])

#test=np.load(station+'fh2o_{day1}{month1}-{day2}{month2}.npy'.format(day1=day[0],month1=month[0],day2=d,month2=m))