import cv2
import numpy as np
import glob
import os
from pysynth_b import *
from pysynth import mix_files
from playsound import playsound
import random
import math
import moviepy.editor as mp


def make_video(impath, outpath, fgpath, bgpath):
    bgr = cv2.imread(impath)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

    darken = 4
    frame = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    frame[:, :, 0] = gray // darken
    frame[:, :, 1] = gray // darken
    frame[:, :, 2] = gray // darken
    # cv2.imwrite('0.jpg', frame)

    X = bgr.shape[0]
    Y = bgr.shape[1]

    dX = X // 10
    dY = Y // 10

    vsize = (Y, X)
    out = cv2.VideoWriter(outpath,cv2.VideoWriter_fourcc(*'XVID'), 4, vsize)

    NOTES = 'cdefgab'
    notes = []

    back = []
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    colors = hsv[:, :, 0]
    m = np.median(colors)
    background_octave = int(m // 37) + 1
    o = background_octave
    back_tune = (('c%d' % o, 8), ('e%d' % o, 8), ('g%d' % o, 8), ('e%d' % o, 8))
    
    counter = 0
    for x in range(0, X, dX):
        for y in range(0, Y, dY):
            c = bgr[x:x+dX, y:y+dY]
            
            if c.shape[0] < 10 or c.shape[1] < 10:
                continue
            
            hsv = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)
            note_number = np.mean(hsv[:, :, 0]) // 37
            hsv[:, :, 0] = note_number * 37
            hsv[:, :, 1] = 255
            hsv[:, :, 2] = 255
            
            c = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
            frame[x:x+dX, y:y+dY] = c
            
            notes.append((NOTES[int(note_number)], 8))
            back.append(back_tune[counter % len(back_tune)])
            
            out.write(frame)
            counter += 1
            print("frame %d / %d" % (counter, n))

    out.release()
    make_wav(notes, fn=fgpath, bpm=120, leg_stac=1.0, boost = 0)
    make_wav(back, fn=bgpath, bpm=120, leg_stac=1.0, boost = 0)
    

def mix(impath):
    make_video(impath, 'tmp.avi', fgpath='tmp1.wav', bgpath='tmp2.wav')
    mix_files('tmp1.wav', 'tmp2.wav', 'tmp3.wav')
    os.system("ffmpeg -i tmp.avi -i tmp3.wav -c:v copy -c:a aac -strict experimental -y uploads/out.mp4")
    return "uploads/out.mp4"