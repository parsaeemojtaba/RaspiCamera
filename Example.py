# This example shows using the RaspiCamera module to capture a single and multiple bracketed images.

import numpy as np
import RaspiCamera as RaspiCamera

CaptureMainDirName='Camera_Captures'
RaspiCam = RaspiCamera.RaspiCamera(CaptureMainDirName)

ShutterSpeed=6400
runStereo=RaspiCam.CaptureSinglePicture(3125, 2500, 'ImgSingle', '.jpg', 100, ShutterSpeed, 'off', 2.88671875, 1.8359375)

ShutterSpeedArray=np.array([3200, 4800, 6400, 10000, 20000])
runStereo=RaspiCam.CaptureMultiplePicture(3125, 2500, 'ImgBracketed', '.jpg', 100, ShutterSpeedArray, 'off', 2.88671875, 1.8359375)
