# This script enables capturing single or multiple bracketed images via Raspberry Pi camera modules using Raspistill functions.

import os
import subprocess
import datetime
import numpy as np

class runRaspiStillCamera:
    def __init__(self, CameraNum=1, MakeTimelapsCaptrueDir='Yes', CaptureStoreDir=None, CaptureMainDirName=None):
        self.CamNum=CameraNum
        self.makeCaptureDir=MakeTimelapsCaptrueDir
        if MakeTimelapsCaptrueDir=='Yes':
            date = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            print('New images are captering at time (sub-folder name) >>> ',date)

            if CaptureStoreDir==None:
                currentPath=os.path.abspath(os.getcwd())
            else:
                currentPath=CaptureStoreDir

            if CaptureMainDirName==None:
                CapturesMainDir='Captures_Camera_'+str(CameraNum) if not CameraNum==1 else 'Captures'
            else:
                CapturesMainDir=CaptureMainDirName
            CapturesMainDirPath=os.path.join(currentPath,CapturesMainDir)
            
            if not os.path.exists(CapturesMainDirPath):
                os.mkdir(CapturesMainDirPath)
            if os.path.exists(CapturesMainDirPath):
                CmdLine='sudo chmod a+w '+CapturesMainDirPath
                runChmod=subprocess.Popen(CmdLine, shell=True, stderr=subprocess.PIPE, 
                                    stdin=subprocess.PIPE, stdout=subprocess.PIPE,  
                                    universal_newlines=False)
                runChmod.stdout.read()

            NewCaptureFolderPath=os.path.join(CapturesMainDirPath,str(date))
            os.mkdir(NewCaptureFolderPath)
            CmdLine='sudo chmod a+w '+NewCaptureFolderPath
            runChmod=subprocess.Popen(CmdLine, shell=True, stderr=subprocess.PIPE, 
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE,  
                                universal_newlines=False)
            runChmod.stdout.read()

            self.capturesMainDirPath=CapturesMainDirPath
            self.newCaptureFolderPath=NewCaptureFolderPath

            
        elif MakeTimelapsCaptrueDir=='No':
            print('Captuered image(s) will store in the current directory!')
        
        else:
            print('error in making a directory to store captured image(s)!')
                
        
    def CaptureSinglePicture(self,Imgwidth, Imgheight, ImgFileName, ImgFileExt,
                                     ISO, ShutterSpeed, WhiteBalance, Rgain, Bgain,
                                     FrameMode=0, framerate=5, ExMode='antishake',  
                                     ImgBirghtness=50, ImgContrast=0, ImgSaturation=0, ImgSharpness=0,
                                     JpegQulity=100 ):
        camNum=(self.CamNum)-1
        imageFilePath=str(ImgFileName)+str(ImgFileExt)
        if self.makeCaptureDir=='Yes':
            ImageFile=str(ImgFileName)+str(ImgFileExt)
            imageFilePath=os.path.join(self.newCaptureFolderPath,str(ImageFile))
        
        print('capturing image, please wiat...')         
        CmdLine=self.CapturePicture(camNum, Imgwidth, Imgheight, imageFilePath,
                                     ISO, ShutterSpeed, WhiteBalance, Rgain, Bgain,
                                     FrameMode, framerate, ExMode,  
                                     ImgBirghtness, ImgContrast, ImgSaturation, ImgSharpness,
                                     JpegQulity)
        try:
            runCam=self.runCameraRaspi(CmdLine)
            output_runCam = runCam.communicate()
        except:
            print('error in capturing a single image!')
            pass
        return (imageFilePath, output_runCam)

    def CaptureMultiplePicture(self,Imgwidth, Imgheight, ImgFileName, ImgFileExt,
                                     ISO, ShutterSpeedArray, WhiteBalance, Rgain, Bgain,
                                     FrameMode=0, framerate=5, ExMode='antishake', 
                                     ImgBirghtness=50, ImgContrast=0, ImgSaturation=0, ImgSharpness=0,
                                     JpegQulity=100 ):
        imageFilePathList=[]
        output_runCamList=[]
        for i in range (0, len(ShutterSpeedArray)):
            ShutterSpeed=ShutterSpeedArray[i]
            ImgFileNameX=ImgFileName+'_'+str(i+1)
            print('capturing image >>>>  ',str(i+1))   

            camNum=(self.CamNum)-1
            imageFilePath=str(ImgFileNameX)+str(ImgFileExt)
            if self.makeCaptureDir=='Yes':
                ImageFile=str(ImgFileNameX)+str(ImgFileExt)
                imageFilePath=os.path.join(self.newCaptureFolderPath,str(ImageFile))
                        
            CmdLine=self.CapturePicture(camNum,Imgwidth, Imgheight, imageFilePath,
                                            ISO, ShutterSpeed, WhiteBalance, Rgain, Bgain,
                                            FrameMode, framerate, ExMode,  
                                            ImgBirghtness, ImgContrast, ImgSaturation, ImgSharpness,
                                            JpegQulity)
            try:
                runCam=self.runCameraRaspi(CmdLine)
                output_runCam = runCam.communicate()

                imageFilePathList.append(imageFilePath)
                output_runCamList.append(output_runCam)
            except:
                print('error in capturing multiple images, non stereo mode!')
                imageFilePathList.append(np.nan)
                output_runCamList.append(np.nan)
                pass
            
        return (imageFilePathList, output_runCamList)

    def CapturePicture(self, camNum, Imgwidth, Imgheight, imageFilePath,
                                     ISO, ShutterSpeed, WhiteBalance, Rgain, Bgain,
                                     FrameMode, framerate, ExMode,  
                                     ImgBirghtness, ImgContrast, ImgSaturation, ImgSharpness,
                                     JpegQulity):
        
        CmdLine='sudo raspistill -cs '+str(camNum)+ \
                    ' -w '+str(Imgwidth)+ \
                    ' -h '+str(Imgheight)+ \
                    ' -md '+str(FrameMode)+ \
                    ' -ISO '+str(ISO)+ \
                    ' -ss '+str(ShutterSpeed)+ \
                    ' -fps '+str(framerate)+ \
                    ' -ex '+str(ExMode)+\
                    ' -awb '+str(WhiteBalance)+\
                    ' -awbg '+str(Rgain)+','+str(Bgain)+\
                    ' -br '+str(ImgBirghtness)+\
                    ' -co '+str(ImgContrast)+\
                    ' -sa '+str(ImgSaturation)+\
                    ' -sh '+str(ImgSharpness)+\
                    ' -q '+str(JpegQulity)+\
                    ' -o '+str(imageFilePath)+\
                    ' --nopreview'

        return CmdLine
    
    def runCameraRaspi(self, CmdLine):
        runCam=subprocess.Popen(CmdLine, shell=True, stderr=subprocess.PIPE, 
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE,  
                         universal_newlines=False)
        return runCam
