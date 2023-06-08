# -*- coding: utf-8 -*-
"""NOTE_Task6OCR_Score_BoundingBox_EasyOCR.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1shv3Cnd7x47ERwz4h-NYWxKRqnzS5yH9
"""

#!pip install easyocr

import easyocr
reader = easyocr.Reader(['ch_sim','en']) # this needs to run only once to load the model into memory

from google.colab import drive
drive.mount('/content/drive')

# Importing all necessary libraries
import cv2
import os
import moviepy.video.io.ImageSequenceClip
import re

from PIL import Image, ImageFont, ImageDraw

def NOTE_Task6OCR_Images_from_video(VideoId, folderId):  
  # Read the video from specified path
  cam = cv2.VideoCapture(VideoId)
    
  print(cam.read())  
  try:
        
      # creating a folder named data
      if not os.path.exists(folderId):
          os.makedirs(folderId)
    
  # if not created then raise error
  except OSError:
      print ('Error: Creating directory of data')
    
  # frame
  currentframe = 0
    
  while(True):
        
      # reading from frame
      ret,frame = cam.read()
    
      if ret:
          print(ret)
          # if video is still left continue creating images
          name = folderId + '/frame' + str(currentframe) + '.jpg'
          print ('Creating...' + name)
    
          # writing the extracted images
          cv2.imwrite(name, frame)
    
          # increasing counter so that it will
          # show how many frames are created
          currentframe += 1
      else:
          break
    
  # Release all space and windows once done
  cam.release()
  cv2.destroyAllWindows()

def NOTE_Task6OCR_Crop_all_Image(folderId,Resultsdirectory):
   
  try:
        
      # creating a folder named data
      if not os.path.exists(Resultsdirectory):
          os.makedirs(Resultsdirectory)
    
  # if not created then raise error
  except OSError:
      print ('Error: Creating directory of result data')
    
  Id = 0
  for filename in os.listdir(folderId):
      if filename.endswith('.jpg'):
        NOTE_Task6OCR_CropImages_ScoreBoard(folderId, Resultsdirectory, filename, Id) 
        Id = Id + 1

def NOTE_Task6OCR_Images_to_Video(folderId):

  fps=1

  folderId1 = '/content/drive/MyDrive/NodeOnTheEdge/Goale/Technical/Task6OCR/data/'


  image_files = [os.path.join(folderId,img)
                for img in os.listdir(folderId)
                if img.endswith(".jpg")]
  clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
  clip.write_videofile(folderId1 + 'NOTE_Task6OCR_ScoreBoardDetection1.mp4')

def NOTE_Task6OCR_CropImages_ScoreBoard(directory, resultDirectory, ImageLocation, Id):
    imagelocationdirectory = os.path.join(directory, ImageLocation)
    print(imagelocationdirectory)
    img = Image.open(imagelocationdirectory)


  #  box = (65, 620, 340, 680) #  Osaka Williams
    
    box = (90,940, 500, 1020) # French Open 2023
  
    img2 = img.crop(box)
    nameId = 'TennisScoreBoard_cropped' + str(Id) + '.jpg'

    print(nameId)
    saveto = os.path.join(resultDirectory, nameId)
    img2.save(saveto)

    print(Id)
    result = NOTE_Task6OCR_DetectText_ScoreBoard(saveto)
    result_format = NOTE_Task6OCR_Format_Results_Scoreboard(result)
    NOTE_Task6OCR_PrintonImages(imagelocationdirectory, result_format)

def NOTE_Task6OCR_PrintonImages(Imageslocation, result_format):
    print(result_format)
    

 #   font_path = os.path.join(cv2.__path__[0],'qt','fonts','DejaVuSans.ttf')
 #   font = ImageFont.truetype(font_path, size=128)
   # title_font = ImageFont.truetype('playfair/playfair-font.ttf', 200)
    print(Imageslocation)

    Img = Image.open(Imageslocation)

    image_editable = ImageDraw.Draw(Img)  

    print(result_format)

    image_editable.text((140,100), result_format)

    Img.save(Imageslocation)

def NOTE_TaskOCR6_Get_Digits(TextId):
 
    IsDigitthere = False

    results = ""

    for m in TextId:
        if m.isdigit():
           IsDigitthere = True

    if(IsDigitthere == True):
      results = NOTE_TaskOCR6_Find_Digits(TextId)

    return results

def NOTE_TaskOCR6_Find_Digits(TextId):
    
    p = '[\d]+[.,()\d]+|[\d]*[.][\d]+|[\d]+'

    s = 'he33llo 42 I\'m a 32 string 30 444.4 12,001'
    catch = []

 #   catch[0] = ""

    if re.search(p, TextId) is not None:
       for catch in re.finditer(p, TextId):
           print(catch[0]) # catch is a match object

    return catch[0]

def NOTE_Task6OCR_Test_Get_Result(imagelocationdirectory, Id):

  imagelocationdirectory1 = '/content/drive/MyDrive/NodeOnTheEdge/Goale/Technical/Task6OCR/data/Osaka_Williams/frames709.jpg'

  resultDirectory1 = '/content/drive/MyDrive/NodeOnTheEdge/Goale/Technical/Task6OCR/data/test/'


  img = Image.open(imagelocationdirectory)

  img.show()

  box = (90,940, 500, 1020)
  img2 = img.crop(box)
  nameId = 'TennisScoreBoard_cropped' + str(Id) + '.jpg'

  print(nameId)
  saveto = os.path.join(resultDirectory1, nameId)
  print(saveto)

  img2.save(saveto)

  img2.show()

  print(Id)
  result = NOTE_Task6OCR_DetectText_ScoreBoard(saveto)

  print(result)

  results = ""

  if(len(result) > 0):

    results1 = NOTE_TaskOCR6_Get_Digits(result[0])

    results2 = NOTE_TaskOCR6_Remove_Digits(result[0])

    results3 = NOTE_TaskOCR6_keeponly_letters(results2)

    print(results3)

  #   print(results1)

  print(result[0])

def NOTE_TaskOCR6_Remove_Digits(TextId):

    pattern = r'[0-9]'

    # Match all digits in the string and replace them with an empty string
    results = re.sub(pattern, '', TextId)

    return results

def NOTE_TaskOCR6_keeponly_letters(TextId):
   
    results = re.sub('[^a-zA-Z]+', '', TextId)

    return results

def NOTE_Task6OCR_Format_Results_Scoreboard(result):
 
    results_format = ""

    print(result)
    if(len(result) > 0):

       results = NOTE_TaskOCR6_Get_Digits(result[0])
     
       print(results)

       result1 = NOTE_TaskOCR6_Remove_Digits(result[0])

       result1 = NOTE_TaskOCR6_keeponly_letters(result1)

       results_format = "Player 1 "+ str(result1) + " Sets " + str(results) 
       
       if(len(result) > 1):
    
          results_format = results_format + " Score " + str(result[1]) 
       
       if(len(result) > 2):

          results2 = NOTE_TaskOCR6_Get_Digits(result[2])

          result2 = NOTE_TaskOCR6_Remove_Digits(result[2])

          result2 = NOTE_TaskOCR6_keeponly_letters(result2)

          results_format = results_format + " Player 2 " + str(result2) + " Sets " + str(results2) 

       if(len(result) > 3):
    
          results_format = results_format + " Score " + str(result[3]) 

    else:

       results_format = "Same score"

    return results_format

def NOTE_Task6OCR_DetectText_ScoreBoard(saveto):
    
    result = reader.readtext(saveto, detail=0)

    return result

import os
print(os.getcwd())

videoId = "/content/drive/MyDrive/NodeOnTheEdge/Goale/Technical/Task6OCR/Iga Swiatek vs Coco Gauff - Quarterfinals Highlights I Roland-Garros 2023.mp4"


#20210218_Osaka_v_S Williams_SF.mp4"

folderId = '/content/drive/MyDrive/NodeOnTheEdge/Goale/Technical/Task6OCR/data/Osaka_Williams6'

Resultsdirectory = '/content/drive/MyDrive/NodeOnTheEdge/Goale/Technical/Task6OCR/data/Osaka_Williams_Results6/'

NOTE_Task6OCR_Images_from_video(videoId, folderId)

NOTE_Task6OCR_Crop_all_Image(folderId,Resultsdirectory)

NOTE_Task6OCR_Images_to_Video(folderId)

imagelocationdirectory = "/content/drive/MyDrive/NodeOnTheEdge/Goale/Technical/Task6OCR/data/Osaka_Williams6/frame509.jpg"

TestId = 0

# NOTE_Task6OCR_Test_Get_Result(imagelocationdirectory, TestId)

#!pip install opencv-wrapper
