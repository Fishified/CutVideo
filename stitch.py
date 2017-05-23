# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 09:36:36 2016

@author: Jason
"""
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import kinematics as kn


path='F:/Cutvideo/Trial_1/226000506285/1_226000506285_3/'
cameras=[10,12,14,16]#bring last two digits of each cameras ip adress

crop='yes'
cropstart=0
cropend=177
interpolate='yes'

rollingperiods=10
framerate=27

#---------------------------------------------------------
#---------------------------------------------------------
#---------------------------------------------------------

tag=int(path[-15:-3]) #extract tag number from path
attempt=int(path[-2])
trial=int(path[-17])


csvlist=[]
for i in range(len(cameras)):
	csvlist.append(pd.read_csv('%s%d_raw.csv' % (path,cameras[i])))


"""
Slightly out of sync camera?

Try your hardest to have the cameras perfectly synced. This will save many headaches. When the attempts are cut from the raw video
I used an approach assuming each camera starts at the same time. Then the attempt is cut by counting the number of seconds from the
start of the video to the start of the attempt (first registry on the TIRIS system) minus a three second buffer and then cutting out the
video until the end of the attempt plus a three second buffer. Works perfectly if the cameras started at the same time, which is most of the time.
But if one had a small delay, then it can cause some problems. I wrote the code below to add empty rows to the affected camera.
"""

#if one camera is out of sync with the rest, this code can help. Makes empty dataFrame with length equal to estimated duration of lagtime
data = np.zeros([14,6])
timelag=pd.DataFrame(data)
timelag.columns=['index','Tag','Trial','Attempt','xCoord','yCoord']
timelag.reset_index()

#append the timelag to the start of the affected camera data
csvlist[0]=timelag.append(csvlist[0])
csvlist[0]=csvlist[0].reset_index()


for i in range(len(csvlist)):
	csvlist[i].ix[csvlist[i].xCoord==0,('xCoord','yCoord','xpixel','ypixel')]=None

horizontalStack = pd.concat(csvlist, axis=1)#this is only here to allow user to check alignment of xCoord and yCoord

"""
This next bit of code combines the lists horizontally. Rows that do not appear in the first carmera are filled by values
present in the second, third, fourth camera, etc. The sync code (above) helps to reduce errors where the index of the first array
actually correspond to a different time in the other cameras. 
"""
csvcombined=csvlist[0]#initiate list
for i in range(len(cameras)):
	try:
		csvcombined=csvcombined.combine_first(csvlist[i+1])
	except IndexError:
		break


#---------save before kinematics-----------
csvcombined.to_csv("%s%d_%d_%d_stitch_raw.csv" %(path,trial,tag,attempt))

#---------Call kinematics function---------
treatedcsvcombined=kn.kinematics(csvcombined,crop,cropstart,cropend,interpolate,framerate,rollingperiods,path,trial,tag,attempt)

#---------Save after kinematics------------
treatedcsvcombined.to_csv("%s%d_%d_%d_stitch_kin.csv" %(path,trial,tag,attempt))





