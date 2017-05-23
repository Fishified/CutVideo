

"""
This little code converts every video file within the directory with the specified extension to .mp4.
I (Jason) wrote this so I could convert the Raspberry Pi .h264 to mp4 for treatment in cv2.
"""
import pandas as pd

import os
names=[]
for root, dirs, files in os.walk("F:/Cutvideo/Trial_1"):
    for file in files:
        if file.endswith(".mp4"):
             names.append(os.path.join(root,file))
             print(os.path.join(root,file))
#             print "Converting"+os.path.splitext(os.path.join(root,file))[0]
             prefix=os.path.splitext(os.path.join(root,file))[0]
             #command=
             #os.system('ffmpeg -i %s -vcodec copy %s.mp4 > /dev/null 2>/dev/null &\n' % (os.path.join(root, file),prefix))		

a=pd.DataFrame(names)
a.to_excel("File_list.xlsx")

