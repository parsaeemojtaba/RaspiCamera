# This example shows using the RaspiCamera module to capture a single and multiple bracketed images.

import numpy as np
import RaspiCamera as RaspiCamera

RaspiCam = RaspiCamera.RaspiCamera()
shutterSpeed=6400
capture_picture=RaspiCam.capture_single_picture(3125, 2500, 'ImgSingle', '.jpg', 100, shutterSpeed, 'off', 2.88671875, 1.8359375)

CaptureMainDirName='Camera_Captures'
camRaspi = RaspiCamera(make_timelapse_capture_dir=True,
                       capture_store_dir=captureStoreDir,
                       capture_main_dir_name=captureMainDirName)
shutterSpeedArray=np.array([4800, 6400, 10000])
capture_pictures = camRaspi.capture_multiple_pictures(3125, 2500, 'ImgCam_A', '.jpg', 100,
                                                shutterSpeedArray,
                                                'off', 2.88671875, 1.8359375)
