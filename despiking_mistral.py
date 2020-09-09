# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 10:39:05 2020

@author: imkes
"""
import numpy as np
# import matplotlib.pyplot as plt
import pandas as pd
# import math
import os, re
import sys

        #variante 1
def despike(var, var_name,tresholdfactor, mini, maxi):
#        var=pd.DataFrame(data['X'])
#        var_name='X'
#        tresholdfactor=3.5
#        mini=0.5
#        maxi=50.
        var_ma= var.rolling(6000, win_type=None).mean() #6000
        wichtig=var_ma[(6000-1)::6000]
        mittel=pd.DataFrame(np.repeat(wichtig.values,6000))
        mittel=mittel.rename(columns={0:var_name})
        noise= pd.DataFrame(var[var_name]-mittel[var_name])
        treshold= tresholdfactor*np.std(noise) #6
        mask_despiking=np.abs(noise) > treshold
        mask_despiking=mask_despiking.rename(columns={0:var_name})
        despiked_data=var[~mask_despiking]
        despiked_data=despiked_data.fillna(mittel)
#        despiked_data[var_name].iloc[np.flatnonzero(despiked_data[var_name]<mini)] =mittel[var_name].iloc[np.flatnonzero(despiked_data[var_name]<mini)]
#        despiked_data[var_name].iloc[np.flatnonzero(despiked_data[var_name]>maxi)]=mittel[var_name].iloc[np.flatnonzero(despiked_data[var_name]>maxi)]
#        mask_despiking[var_name].iloc[np.flatnonzero(despiked_data[var_name]<mini)] =True
#        mask_despiking[var_name].iloc[np.flatnonzero(despiked_data[var_name]>maxi)]=True
        return despiked_data,mask_despiking #mittel,noise,
  

day_min, day_max = int(sys.argv[1]), int(sys.argv[2])
print(day_min,day_max)
month= int(sys.argv[3])
print(month)
day_arr=np.arange(day_min,day_max+1,1)
day=list((day_arr))    
# day=['18','19','20','21','22','23','24','25','26','27','28','29','30','31']#['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17',
month=['%02d' %(month)]#['01']#['01','02','03']
station=str(sys.argv[4])#['bug']
station1=str(sys.argv[5])#'BUG'
s=station

varpath='/mnt/lustre02/work/um0203/u301025/Variablen'
cd = '/mnt/lustre02/work/um0203/u301025/Masterarbeit/Eureka/Daten/'+s+'/Level0b_RawData20HzDaily/'
print(day_arr,day,month,station1,s,cd)
for m in month:
    print(m)
    for d in day:
        print(d)
        i = 0
        dfList = []
        for root, dirs, files in os.walk(cd,topdown=True):
            for fname in files:
                if re.match("2020"+m+str(d)+"-U"+station1+'.txt', fname):
                    frame = pd.read_csv(os.path.join(root, fname), delimiter=";", decimal='.')
                    frame['key'] = "file{}".format(i)
                    dfList.append(frame)    
                    i += 1
                    print(root)
                    data= pd.concat(dfList,ignore_index=True)
        
        despike_X=despike(pd.DataFrame(data['X']),'X',12.,-20.,20.)#3.5
        despike_Y=despike(pd.DataFrame(data['Y']),'Y',12.,-20.,20.)#3.5
        despike_Z=despike(pd.DataFrame(data['Z']),'Z',8.,-10.,10.)#5
        despike_T=despike(pd.DataFrame(data['T']),'T',8.,10.,40.)#3.5
        despike_CC=despike(pd.DataFrame(data['CC']),'CC',1000.,8.,32.)#8
        despike_CH=despike(pd.DataFrame(data['CH']),'CH',1000.,0.,1200.)#8
        despike_AX=despike(pd.DataFrame(data['AX']),'AX',5.,-9.8136,9.8136)#5
        despike_AY=despike(pd.DataFrame(data['AY']),'AY',5.,-9.8136,9.8136)#5
        despike_AZ=despike(pd.DataFrame(data['AZ']),'AZ',5.,0,19.6272)#5
        
        despike_X=list(despike_X)
        despike_Y=list(despike_Y)
        despike_Z=list(despike_Z)
        despike_T=list(despike_T)
        despike_CC=list(despike_CC)
        despike_CH=list(despike_CH)
        despike_AX=list(despike_AX)
        despike_AY=list(despike_AY)
        despike_AZ=list(despike_AZ)
        
        despike_X[1]=despike_X[1]*1
        despike_Y[1]=despike_Y[1]*1
        despike_Z[1]=despike_Z[1]*1
        despike_T[1]=despike_T[1]*1
        despike_CC[1]=despike_CC[1]*1
        despike_CH[1]=despike_CH[1]*1
        despike_AX[1]=despike_AX[1]*1
        despike_AY[1]=despike_AY[1]*1
        despike_AZ[1]=despike_AZ[1]*1
        
        
        despike_X[1][despike_X[1]==0.]=np.nan
        despike_Y[1][despike_Y[1]==0.]=np.nan
        despike_Z[1][despike_Z[1]==0.]=np.nan
        despike_T[1][despike_T[1]==0.]=np.nan
        despike_CC[1][despike_CC[1]==0.]=np.nan
        despike_CH[1][despike_CH[1]==0.]=np.nan
        despike_AX[1][despike_AX[1]==0.]=np.nan
        despike_AY[1][despike_AY[1]==0.]=np.nan
        despike_AZ[1][despike_AZ[1]==0.]=np.nan
        
        despike_Vberechnet1=np.sqrt(despike_X[0]['X']**2+despike_Y[0]['Y']**2)
        despike_Vberechnet2=despike_X[1]['X']*despike_Y[1]['Y']
        despike_Vberechnet=[pd.DataFrame(despike_Vberechnet1),pd.DataFrame(despike_Vberechnet2)]            
        #            X=np.array([1,0,1,-1,0,-1])
        #            Y=np.array([1,1,0,0,-1,-1])
        #            alpha_1=180/np.pi*np.arctan2(-X,-Y)%360
        #            alpha_2=180/np.pi*np.arctan2(-Y,X)
        #            alpha_3=270-((180/np.pi)*np.arctan2(np.cos((Y-180)/180. * math.pi),np.sin((X-180)/180. * math.pi)))
        #            alpha_4=180/np.pi*np.arctan2(-Y,-X)%360
        despike_D1=180/np.pi*np.arctan2(-despike_Y[0]['Y'],-despike_X[0]['X'])%360
        despike_D1=despike_D1 + np.ceil( -despike_D1 / 360 ) * 360
        despike_D2=despike_X[1]['X']*despike_Y[1]['Y']
        despike_D=[pd.DataFrame(despike_D1),pd.DataFrame(despike_D2)]
        
        a1=despike_X[0]['X']
        b1=despike_X[1]['X']
        c1=despike_Y[0]['Y']
        d1=despike_Y[1]['Y']
        e1=despike_Z[0]['Z']
        f1=despike_Z[1]['Z']
        g1=despike_T[0]['T']
        h1=despike_T[1]['T']  
        i1=despike_CC[0]['CC'] 
        j1=despike_CC[1]['CC'] 
        k1=despike_CH[0]['CH'] 
        l1=despike_CH[1]['CH'] 
        m1=despike_Vberechnet[0][0]
        n1=despike_Vberechnet[1][0]
        o1=despike_D[0]['Y'] 
        p1=despike_D[1][0]
        q1=despike_AX[0]['AX'] 
        r1=despike_AX[1]['AX']
        s1=despike_AY[0]['AY'] 
        t1=despike_AY[1]['AY']
        u1=despike_AZ[0]['AZ'] 
        v1=despike_AZ[1]['AZ']
          
        flag=pd.DataFrame(data={'X':  a1,'X_mask': b1,'Y':c1 ,'Y_mask': d1,'Z': e1,'Z_mask': f1,'T': g1,'T_mask': h1,'CC': i1,'CC_mask': j1,'CH': k1,'CH_mask': l1, 'V':  m1,'V_mask': n1,'D':  o1,'D_mask': p1,'AX':q1 ,'AX_mask': r1,'AY':s1 ,'AY_mask': t1,'AZ':u1 ,'AZ_mask': v1,} ) #np.array(despike_X[0].index
        flag.to_csv(varpath+'despiking_{day}{month}_{station}.csv'.format(day=str(d),month=m,station=s))        
        # #%%        #plots zur veranschaulichung
        # #            flag=pd.read_csv('despiking_{day}{month}_{station}.csv'.format(day=d,month=m,station=station))
        #             plt.figure(1)
        #             plt.plot(data['X'])
        #             plt.figure(2)
        #             plt.plot(despike_X[0])
        #             plt.figure(3)
        #             plt.plot(despike_X[1])
        #             plt.figure(4)
        #             plt.plot(data['X']-despike_X[0]['X'])
        
        #             #std=6
        #             test_m= np.where(despike_X[1]==1.)
        #             test_m=test_m[0]
        #             abfrage=test_m[(test_m > 1696000.)]
        #             test_n=test_m[abfrage[0][:]]
        #             plt.plot(data.loc[1696000:1699700]['X'],'*')#.loc[1696000:1699700]
        #             for i in range(0,len(test_n)):
        #                 plt.plot(test_n[i],data.loc[test_n[i]]['X'],'*')
            
        #             test_m= np.where(despike_X[1]==1.)
        #             test_m=test_m[0]
        #             abfrage=test_m[(test_m > 1698000.) & (test_m < 1699000.)]
        # #            test_n=test_m[abfrage[0][:]]
        #             plt.plot(data.loc[1698000:1699000]['X'],'*')#.loc[1696000:1699700]
        #             for i in range(0,len(abfrage)):
        #                 plt.plot(abfrage[i],data.loc[abfrage[i]]['X'],'*',color='red')    
            
        #             test_m= np.where(despike_X[1]==1.)
        #             plt.plot(data['X'],'*')#.loc[1696000:1699700]
        #             for i in range(0,len(test_m)):
        #                 plt.plot(test_m[i],data.loc[test_m[i]]['X'],'*')
        
        
        #             plt.figure(5)
        #             plt.plot(data['Y'])
        #             plt.figure(6)
        #             plt.plot(despike_Y[0])
        #             plt.figure(7)
        #             plt.plot(despike_Y[1])
        #             plt.figure(8)
        #             plt.plot(data['Y']-despike_Y[0]['Y'])
        
        #             test_m= np.where(despike_Y[1]==1.)
        #             plt.plot(data['Y'],'*')#.loc[1696000:1699700]
        #             for i in range(0,len(test_m)):
        #                 plt.plot(test_m[i],data.loc[test_m[i]]['Y'],'*',color='red')
            
        #             test_m= np.where(despike_Y[1]==1.)
        #             test_m=test_m[0]
        #             abfrage=test_m[(test_m > 221990.) & (test_m < 222500.)]
        # #            test_n=test_m[abfrage[0][:]]
        #             plt.plot(data.loc[221990:222500]['Y'],'*')#.loc[1696000:1699700]
        #             for i in range(0,len(abfrage)):
        #                 plt.plot(abfrage[i],data.loc[abfrage[i]]['Y'],'*',color='red')  
        
        #             plt.figure(9)
        #             plt.plot(data['Z'])
        #             plt.figure(10)
        #             plt.plot(despike_Z[0])
        #             plt.figure(11)
        #             plt.plot(despike_Z[1])
        #             plt.figure(12)
        #             plt.plot(data['Z']-despike_Z[0]['Z'])
        
        #             test_m= np.where(despike_Z[1]==1.)
        #             plt.plot(data['Z'],'*')#.loc[1696000:1699700]
        #             for i in range(0,len(test_m)):
        #                 plt.plot(test_m[i],data.loc[test_m[i]]['Z'],'*',color='red')
            
        #             test_m= np.where(despike_Z[1]==1.)
        #             test_m=test_m[0]
        #             abfrage=test_m[(test_m > 735000.) & (test_m < 740000.)]
        # #            test_n=test_m[abfrage[0][:]]
        #             plt.plot(data.loc[735000:740000]['Z'],'*')#.loc[1696000:1699700]
        #             for i in range(0,len(abfrage)):
        #                 plt.plot(abfrage[i],data.loc[abfrage[i]]['Z'],'*',color='red')
            
        
        #             plt.figure(13)
        #             plt.plot(data['T'])
        #             plt.figure(14)
        #             plt.plot(despike_T[0])
        #             plt.figure(15)
        #             plt.plot(despike_T[1])
        #             plt.figure(16)
        #             plt.plot(data['T']-despike_T[0]['T'])
        
        #             test_m= np.where(despike_T[1]==1.)
        #             plt.plot(data['T'],'*')#.loc[1696000:1699700]
        #             for i in range(0,len(test_m)):
        #                 plt.plot(test_m[i],data.loc[test_m[i]]['T'],'*',color='red')
            
        #             test_m= np.where(despike_T[1]==1.)
        #             test_m=test_m[0]
        #             abfrage=test_m[(test_m > 732000.) & (test_m < 735000.)]
        # #            test_n=test_m[abfrage[0][:]]
        #             plt.plot(data.loc[732000:735000]['T'],'*')#.loc[1696000:1699700]
        #             for i in range(0,len(abfrage)):
        #                 plt.plot(abfrage[i],data.loc[abfrage[i]]['T'],'*',color='red')
        
        #             plt.figure(17)
        #             plt.plot(data['CC'])
        #             plt.figure(18)
        #             plt.plot(despike_CC[0])
        #             plt.figure(19)
        #             plt.plot(despike_CC[1])
        #             plt.figure(20)
        #             plt.plot(data['CC']-despike_CC[0]['CC'])
        
        #             test_m= np.where(despike_CC[1]==1.)
        #             test_m=test_m[0]
        #             plt.plot(data['CC'],'*')#.loc[1696000:1699700]
        #             for i in range(0,len(test_m)):
        #                 plt.plot(test_m[i],data.loc[test_m[i]]['CC'],'*',color='red')
            
        #             abfrage=test_m[(test_m > 749000.) & (test_m < 750000.)]
        # #            test_n=test_m[abfrage[0][:]]
        #             plt.plot(data.loc[749000:750000]['CC'],'*')#.loc[1696000:1699700]
        #             for i in range(0,len(abfrage)):
        #                 plt.plot(abfrage[i],data.loc[abfrage[i]]['CC'],'*',color='red')
        
        #             plt.figure(21)
        #             plt.plot(data['CH'])
        #             plt.figure(22)
        #             plt.plot(despike_CH[0])
        #             plt.figure(23)
        #             plt.plot(despike_CH[1])
        #             plt.figure(24)
        #             plt.plot(data['CH']-despike_CH[0]['CH'])
        
        #             test_m= np.where(despike_CH[1]==1.)
        #             test_m=test_m[0]
        #             plt.plot(data['CH'],'*')#.loc[1696000:1699700]
        #             for i in range(0,len(test_m)):
        #                 plt.plot(test_m[i],data.loc[test_m[i]]['CH'],'*',color='red')
        
        #             plt.figure(25)
        #             plt.plot(data['V'])
        #             plt.figure(26)
        #             plt.plot(despike_V[0])
        #             plt.figure(27)
        #             plt.plot(despike_V[1])
        #             plt.figure(28)
        #             plt.plot(data['V']-despike_V[0]['V'])
        #             plt.figure(45)
        #             plt.plot(despike_Vberechnet)
        #             plt.figure(46)
        #             plt.plot(pd.DataFrame(despike_Vberechnet)[0]-despike_V[0]['V'])
        
        
        #             plt.figure(29)
        #             plt.plot(data['D'],'*')
        #             plt.figure(30)
        #             plt.plot(despike_D[0],'*')
        #             plt.figure(31)
        #             plt.plot(despike_D[1])
        #             plt.figure(32)
        #             plt.plot(data['D']-despike_D[0]['Y'],'*')
        
        
        #             plt.figure(33)
        #             plt.plot(data['AX'])
        #             plt.figure(34)
        #             plt.plot(despike_AX[0])
        #             plt.figure(35)
        #             plt.plot(despike_AX[1])
        #             plt.figure(36)
        #             plt.plot(data['AX']-despike_AX[0]['AX'])
        
        #             test_m= np.where(despike_AX[1]==1.)
        #             test_m=test_m[0]
        #             plt.plot(data['AX'],'*')#.loc[1696000:1699700]
        #             for i in range(0,len(test_m)):
        #                 plt.plot(test_m[i],data.loc[test_m[i]]['AX'],'*',color='red')
        
        #             plt.figure(37)
        #             plt.plot(data['AY'])
        #             plt.figure(38)
        #             plt.plot(despike_AY[0])
        #             plt.figure(39)
        #             plt.plot(despike_AY[1])
        #             plt.figure(40)
        #             plt.plot(data['AY']-despike_AY[0]['AY'])
        
        #             test_m= np.where(despike_AY[1]==1.)
        #             test_m=test_m[0]
        #             plt.plot(data['AY'],'*')#.loc[1696000:1699700]
        #             for i in range(0,len(test_m)):
        #                 plt.plot(test_m[i],data.loc[test_m[i]]['AY'],'*',color='red')
        
        #             plt.figure(41)
        #             plt.plot(data['AZ'])
        #             plt.figure(42)
        #             plt.plot(despike_AZ[0])
        #             plt.figure(43)
        #             plt.plot(despike_AZ[1])
        #             plt.figure(44)
        #             plt.plot(data['AZ']-despike_AZ[0]['AZ'])
        # #            
        #             test_m= np.where(despike_AZ[1]==1.)
        #             test_m=test_m[0]
        #             plt.plot(data['AZ'],'*')#.loc[1696000:1699700]
        #             for i in range(0,len(test_m)):
        #                 plt.plot(test_m[i],data.loc[test_m[i]]['AZ'],'*',color='red')
        #variante 2
        #u=data['T']
        #u_ma= u.rolling(6000, win_type=None).mean() #6000
        #noise= u-u_ma
        #treshold= 6*np.std(noise) #6
        #mask_despiking=np.abs(noise) > treshold
        ##test=u
        #test=u[~mask_despiking]
        #test=test.fillna(u_ma)
        ##test[~mask_despiking]=np.nan
        #plt.figure(1)
        #plt.plot(u)
        #plt.figure(2)
        #plt.plot(test)
        #plt.figure(3)
        #plt.plot(mask_despiking)
        
        #test
        #u=pd.DataFrame(np.array([1,2,1,2,99,1,2,1,3,2,1]))
        #u_ma= u.rolling(5, win_type=None).mean() #6000
        #wichtig=u_ma[4::5]
        #mittel=pd.DataFrame(np.repeat(wichtig.values,5))
        #noise= u-mittel
        #treshold= 0.5*np.std(noise) #6
        #mask_despiking=np.abs(noise) > treshold
        ##test=u
        #test=u[~mask_despiking]
        #test=test.fillna(mittel)
        ##test[~mask_despiking]=np.nan
        #plt.figure(1)
        #plt.plot(u)
        #plt.figure(2)
        #plt.plot(test)
        #plt.figure(3)
        #plt.plot(mask_despiking)