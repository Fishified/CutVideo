# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 16:05:05 2016

@author: Jason

Creates bash script run from a linux bash shell. The bash script extracts video from raw Raspberry pi videos.
"""

import numpy as np
import subprocess
import os
#import cv2
import os.path
import pandas as pd
from multiprocessing import Process


Lsvpd = pd.read_excel('./video_extraction_Times.xlsx',0)
dfCameraStartTimes = pd.read_excel('./Camera_start_times.xlsx',0)
ipadresses = pd.read_excel('./ipadresses.xlsx',0)
Lsv=Lsvpd.as_matrix()
CameraStartTimes=dfCameraStartTimes.as_matrix()
trials=[1,2]
commandlist=[]
timeBuffer=3

if os.path.isdir('./Cutvideo') is False:
    os.mkdir('./Cutvideo')

for count in range(len(CameraStartTimes)):
    if os.path.isdir('./Cutvideo/Trial_%s' %int(CameraStartTimes[count,0])) is False:
            os.mkdir('./Cutvideo/Trial_%s' %int(CameraStartTimes[count,0]))

srcfldList=['151002A','151002B','151003A','151003B','151004A','151004B',
            '151014A','151014B','151015A','151015B','151016A','151016B','151017A']

for i in range(len(Lsv)): #for each row (attempt) in list

    for count in range(len(CameraStartTimes)):

        if Lsv[i,3]==CameraStartTimes[count,0]:
             maxAntenna=Lsv[i,5]
             
             srcfld=srcfldList[count]
             start=Lsv[i,9]-timeBuffer #number of frames from start of video to start of attempt
             stop=Lsv[i,10]+timeBuffer #number of frames from start of video to end of attempt
             
             #create tag subfolder within trial
             cwd='./Cutvideo/Trial_%s/%d' %(int(CameraStartTimes[count,0]),Lsv[i,0]) 
             if os.path.isdir(cwd) is False:
                 os.mkdir(cwd)

             attmpnumber=len(os.listdir(cwd))+1 #finds attempt number by counting number of files in directory after previous pass
             svfld='./Cutvideo/Trial_%s/%d/%d_%d_%d' % (int(CameraStartTimes[count,0]),Lsv[i,0],int(CameraStartTimes[count,0]),Lsv[i,0],attmpnumber)
             if os.path.isdir(svfld) is False:
                 os.mkdir(svfld)
            
             f = open('%s/info.txt' %svfld, 'a')
             f.write('Trail index,%d\n' %attmpnumber)
             f.write('Tag,%d\n' %Lsv[i,0])
             f.write('Start,%.15f\n' %Lsv[i,1])
             f.write('Stop,%.15f\n' %Lsv[i,2])
             f.close()
             
             if maxAntenna == 1:
                  cameras=[10]
             if maxAntenna == 2 or maxAntenna==3 or maxAntenna==4:
                 cameras=[10,12]
             if maxAntenna == 5 or maxAntenna==6 or maxAntenna==7:
                 cameras=[10,12,14,16]
             if maxAntenna == 8 or maxAntenna==9 or maxAntenna==10:
                 cameras=[10,12,14,16,18]

             for b in range(len(cameras)):
                 f = open('GNUtest.txt','a') #opens file
                 #command='ffmpeg -f h264 -r:v 27 -i ./%s/*%s.h264 -ss %s -c copy -to %d %s/%s.h264 > /dev/null 2>/dev/null &\n' %(srcfld,cameras[b],start,stop,svfld,cameras[b])#run bash ffmpeg command to splice videos

                 f.write('ffmpeg -r 27 -i ./%s/*%s.h264 -ss %d -to %d -r 27 %s/%s.h264 > /dev/null 2>/dev/null &\n' %(srcfld,cameras[b],start,stop,svfld,cameras[b]))#run bash ffmpeg command to splice videos
                 f.close()
