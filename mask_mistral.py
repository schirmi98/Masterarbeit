# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 13:38:57 2020

@author: imkes
"""

import numpy as np
import pandas as pd
import os, re
import sys

def maske(hour_begin, minutes_begin,hour_end,minutes_end):
    for i in range(0, len(hour_begin)):
        begin = hour_begin[i] * 60 * 60 * 20 + minutes_begin[i]* 60 *20
        end = hour_end[i]*60*60*20+minutes_end[i]*60*20
        mask[begin:end]=np.nan
    return mask

hour_begin_bug_clean=[[20],[],[],[12],[],[],[]]#,[],[],[],[],[],[],[],[],[],[],[],[21],[17],[],[],[],[],[17],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
hour_end_bug_clean=[[20],[],[],[13],[],[],[]]#,[],[],[],[],[],[],[],[],[],[],[],[21],[17],[],[],[],[],[17],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
minutes_begin_bug_clean=[[35],[],[],[50],[],[],[]]#,[],[],[],[],[],[],[],[],[],[],[],[14],[33],[],[],[],[],[44],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
minutes_end_bug_clean=[[55],[],[],[10],[],[],[]]#,[],[],[],[],[],[],[],[],[],[],[],[18],[39],[],[],[],[],[47],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
hour_begin_top_clean=[[],[],[],[],[],[],[]]#,[],[],[],[],[],[16],[],[],[12],[],[],[],[16],[],[],[],[],[17],[],[],[],[12],[],[],[],[],[19],[],[],[],[],[],[],[11],[],[]]
hour_end_top_clean=[[],[],[],[],[],[],[]]#,[],[],[],[],[],[16],[],[],[12],[],[],[],[16],[],[],[],[],[17],[],[],[],[12],[],[],[],[],[20],[],[],[],[],[],[],[11],[],[]]
minutes_begin_top_clean=[[],[],[],[],[],[],[]]#,[],[],[],[],[],[30],[],[],[27],[],[],[],[15],[],[],[],[],[20],[],[],[],[36],[],[],[],[],[58],[],[],[],[],[],[],[06],[],[]]
minutes_end_top_clean=[[],[],[],[],[],[],[]]#,[],[],[],[],[],[31],[],[],[28],[],[],[],[16],[],[],[],[],[30],[],[],[],[37],[],[],[],[],[00],[],[],[],[],[],[],[07],[],[]]
#hour_begin_bug_winddir=[[],[],[],[],[],[],[]]#,[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
#hour_end_bug_winddir=[[],[],[],[],[],[],[]]#,[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
#minutes_begin_bug_winddir=[[],[],[],[],[],[],[]]#,[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
#minutes_end_bug_winddir=[[],[],[],[],[],[],[]]#,[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
#hour_begin_top_winddir=[[],[],[],[],[],[],[]]#,[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
#hour_end_top_winddir=[[],[],[],[],[],[],[]]#,[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
#minutes_begin_top_winddir=[[],[],[],[],[],[],[]]#,[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
#minutes_end_top_winddir=[[],[],[],[],[],[],[]]#,[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
hour_begin_chimney=[[],[],[],[2,5],[12],[8],[]]#,[20],[],[],[],[],[],[21,21,21,21,22,23],[00,12],[1],[7,7,8],[10],[],[14],[],[2],[10,11,13,14,18],[],[],[12,13],[19,21,22,22,23],[0,0],[16],[2,2,3,4,5,7],[16],[14],[21,23],[0,5,6,8,19],[],[],[],[],[],[],[],[11,12]]
hour_end_chimney=[[],[],[],[2,5],[12],[9],[]]#,[20],[],[],[],[],[],[21,21,21,22,22,24],[00,12],[1],[7,7,8],[10],[],[48],[],[3],[10,11,13,14,18],[],[],[12,13],[19,21,22,23,23],[0,0],[17],[2,3,4,4,6,7],[16],[14],[21,23],[4,6,7,8,20],[],[],[],[],[],[],[],[11,12]]
minutes_begin_chimney=[[],[],[],[39,38],[20],[46],[]]#,[42],[],[],[],[],[2,25,37,48,52,2],[00,9],[1],[12,41,8],[37],[],[15],[],[58],[31,10,23,12,24],[],[],[51,0],[27,4,9,21,45],[1,16],[23],[36,54,57,18,25,9],[29],[50],[31,3],[18,14,27,12,33],[],[],[],[],[],[],[],[],[55,37]]
minutes_end_chimney=[[],[],[],[40,39],[29],[21],[]]#,[46],[],[],[],[],[4,33,41,1,55,00],[43,12],[9],[15,43,16],[51],[],[57],[],[1],[58,24,57,50,25],[],[],[54,2],[29,17,10,43,57],[6,18],[47],[43,53,14,22,54,20],[32],[51],[33,21],[28,9,59,23,26],[],[],[],[],[],[],[],[],[57,43]]
hour_begin_rain=[[],[],[],[],[],[],[]]#,[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
hour_end_rain=[[],[],[],[],[],[],[]]#,[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
minutes_begin_rain=[[],[],[],[],[],[],[]]#,[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
minutes_end_rain=[[],[],[],[],[],[],[]]#,[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
#hour_begin_bug_interpolation=[[],[],[],[],[],[],[]]#,[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
#hour_end_bug_interpolation=[[],[],[],[],[],[],[]]#,[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
#minutes_begin_bug_interpolation=[[],[],[],[],[],[],[]]#,[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
#minutes_end_bug_interpolation=[[],[],[],[],[],[],[]]#,[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
#hour_begin_top_interpolation=[[],[],[],[],[],[],[]]#,[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
#hour_end_top_interpolation=[[],[],[],[],[],[],[]]#,[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
#minutes_begin_top_interpolation=[[],[],[],[],[],[],[]]#,[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
#minutes_end_top_interpolation=[[],[],[],[],[],[],[]]#,[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
#hour_begin_stop=[[],[],[],[],[],[],[]]#,[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
#hour_end_stop=[[],[],[],[],[],[],[]]#,[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
#minutes_begin_stop=[[],[],[],[],[],[],[]]#,[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
#minutes_end_stop=[[],[],[],[],[],[],[]]#,[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

day_min, day_max = int(sys.argv[1]), int(sys.argv[2])
print(day_min,day_max)
month= int(sys.argv[3])
day_arr=np.arange(day_min,day_max+1,1)
day=list((day_arr))    
month=['%02d' %(month)]#['01']#['01','02','03']

varpath='/mnt/lustre02/work/um0203/u301025/Variablen/'

x=int(sys.argv[4])#ist null wenns bei 18.01 beginnt., sonst jeden tag später entspricht plus 1
cd='/mnt/lustre02/work/um0203/u301025/Eureka/Daten/Dship/meteorolog_daten/'

for m in month:
    for d in day:
        j=day.index(d)*(month.index(m)+1)
        mask=np.ones(24*60*60*20)
        mask_bug_clean = maske(hour_begin_bug_clean[j], minutes_begin_bug_clean[j],hour_end_bug_clean[j], minutes_end_bug_clean[j])
        mask_top_clean = maske(hour_begin_top_clean[j], minutes_begin_top_clean[j],hour_end_top_clean[j], minutes_end_top_clean[j])
#        mask_bug_winddir = maske(hour_begin_bug_winddir[j], minutes_begin_bug_winddir[j],hour_end_bug_winddir[j], minutes_end_bug_winddir[j])
#        mask_top_winddir = maske(hour_begin_top_winddir[j], minutes_begin_top_winddir[j],hour_end_top_winddir[j], minutes_end_top_winddir[j])
        mask_chimney = maske(hour_begin_chimney[j], minutes_begin_chimney[j],hour_end_chimney[j], minutes_end_chimney[j])
        mask_rain = maske(hour_begin_rain[j], minutes_begin_rain[j],hour_end_rain[j], minutes_end_rain[j])
#        mask_bug_interpolation = maske(hour_begin_bug_interpolation[j], minutes_begin_bug_interpolation[j],hour_end_bug_interpolation[j], minutes_end_bug_interpolation[j])
#        mask_top_interpolation = maske(hour_begin_top_interpolation[j], minutes_begin_top_interpolation[j],hour_end_top_interpolation[j], minutes_end_top_interpolation[j])
#        mask_stop = maske(hour_begin_stop[j], minutes_begin_stop[j],hour_end_stop[j], minutes_end_stop[j])
        flag=pd.DataFrame(data={'mask_bug_clean': mask_bug_clean,'mask_top_clean': mask_top_clean,'mask_chimney': mask_chimney, 'mask_rain': mask_rain} )
        # flag.to_csv(varpath+'mask_{day}{month}.csv'.format(day=d,month=m))
        
# flag=pd.read_csv('mask_{day}{month}.csv'.format(day=str(d),month=m))
#for m in month:
#    for d in day:        
        i = 0
        dfList = []
        for root, dirs, files in os.walk(cd,topdown=True):
            for fname in files:
                if re.match("dship_"+str(d)+'_'+m, fname):
                    frame = pd.read_csv(os.path.join(root, fname), delimiter=";", decimal='.', skiprows=[1,2])
                    frame['key'] = "file{}".format(i)
                    dfList.append(frame)    
                    i += 1
                    print(root)
                    dship= pd.concat(dfList,ignore_index=True)   
                
                    averagespeed1=dship['SYS.CALC.SPEED_kmh'].rolling(60).mean()
                    averagespeed2 = averagespeed1.iloc[59::60]
#                    Maske alles unter einem Knoten bedeutet stehen, alles andere fährt 
                    mask_stop=averagespeed2 < 1,852
                    mask_stop=np.repeat(mask_stop[0], 60*20)
                    mask_stop.reset_index(drop=True, inplace=True)
                    mask_stop.to_frame()
                    mask_stop=1.*mask_stop
                    mask_stop[mask_stop==0.]=np.nan
#                    mask_stop3=mask_stop2.astype('float64')
#                    mask_stop3[mask_stop3==0.]=np.nan
                    flag['mask_stop']=mask_stop
                    
                    usatdata_top=pd.read_csv(varpath+'topusatdata_'+str(d)+m+'.csv', delimiter=",", decimal='.',usecols =['D'])
                    usatdata_bug=pd.read_csv(varpath+'bugusatdata_'+str(d)+m+'.csv', delimiter=",", decimal='.',usecols =['D'])
                    mask_bug_winddir=(usatdata_bug['D'] > 130.) & (usatdata_bug['D'] <250.)
#                    mask_stop2=np.repeat(mask_stop[0], 60*20)
#                    mask_stop2.reset_index(drop=True, inplace=True)
                    mask_bug_winddir.to_frame()
                    mask_bug_winddir=1.*mask_bug_winddir
                    mask_bug_winddir[mask_bug_winddir==0.]=np.nan
                    
                    mask_top_winddir=(usatdata_top['D'] > 180.) & (usatdata_top['D'] <190.) or (usatdata_top['D'] > 110.) & (usatdata_top['D'] <150.) or (usatdata_top['D'] > 245.) & (usatdata_top['D'] <255.)
                    mask_top_winddir.to_frame()
                    mask_top_winddir=1.*mask_top_winddir
                    mask_top_winddir[mask_top_winddir==0.]=np.nan

                    flag['mask_top_winddir']=mask_top_winddir
                    flag['mask_bug_winddir']=mask_bug_winddir
#                    usatdata[~mask_stop] = np.nan
                    
                  
#                    [[2],[2],[2-2.5],[1],[2-2.5],[2.5-3],[3.5-4],[3.5-2.5],[2.5-2],[1.5],[1.5],[1-1.5],[1-1.5],[1.5-2],[1.5-2],[1.5],[1.5-2],[1.5-2],[1.5-2],[1.5],[1.5-2],[1.5-2],[2],[2.5],[3],[2.5-3],[2.5],[2.5-3],[2.5-3],[2.5-3],[2.5-3],[2.5-3],[2-2.5],[1.5-2],[1.5-2],[2.5],[2.5-3(im Landschutz nur 1-1.5)],[3.5],[2.5],[2.5],[1.5-2],[2.5],[nur vorhersage:2-2.5],[nur vorhersage:2],[],[],[]]
                    mask_swell=[[8],[8],[9],[4],[9],[11],[15],[12],[9],[6],[6],[5],[5],[7],[7],[6],[7],[7],[7],[6],[7],[7],[8],[10],[12],[11],[10],[11],[11],[11],[11],[11],[9],[7],[7],[10],[11],[14],[10],[10],[7],[10],[9],[8],[np.nan],[np.nan],[np.nan]]
                    swtest=np.ones(len(flag))*mask_swell[x]
                    flag['mask_swell']=swtest
                    x=+1
                    
#                     mask_best=[[]]
                    
                    despiking_bug=pd.read_csv(varpath+'despiking_{day}{month}_bug.csv'.format(day=d,month=m))
                    despiking_bug=despiking_bug.drop(['Unnamed: 0','X', 'Y', 'Z', 'T', 'CC','CH','V','D','AX','AY','AZ'],axis=1)
                    despiking_top=pd.read_csv(varpath+'despiking_{day}{month}_top.csv'.format(day=str(d),month=m))
                    despiking_top=despiking_top.drop(['Unnamed: 0','X', 'Y', 'Z', 'T', 'CC','CH','V','D','AX','AY','AZ'],axis=1)
                    despiking_top=despiking_top.rename(columns={'X_mask':'X_mask_top', 'Y_mask': 'Y_mask_top', 'Z_mask':'Z_mask_top', 'T_mask':'T_mask_top', 'CC_mask':'CC_mask_top','CH_mask':'CH_mask_top','V_mask':'V_mask_top','D_mask':'D_mask_top','AX_mask':'AX_mask_top','AY_mask':'AY_mask_top','AZ_mask':'AZ_mask_top'})
                    despiking_bug.rename(columns={'X_mask':'X_mask_bug', 'Y_mask': 'Y_mask_bug', 'Z_mask':'Z_mask_bug', 'T_mask':'T_mask_bug', 'CC_mask':'CC_mask_bug','CH_mask':'CH_mask_bug','V_mask':'V_mask_bug','D_mask':'D_mask_bug','AX_mask':'AX_mask_bug','AY_mask':'AY_mask_bug','AZ_mask':'AZ_mask_bug'})
                    flag=flag.append(despiking_top,sort=True)
                    flag=flag.append(despiking_bug)


                    flag.to_csv(varpath+'mask_{day}{month}.csv'.format(day=str(d),month=m))