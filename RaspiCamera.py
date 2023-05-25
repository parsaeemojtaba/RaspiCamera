# This script enables capturing single or multiple bracketed images via Raspberry Pi camera modules using Raspistill functions.
import os
import subprocess
import datetime
import numpy as np

class RaspiCamera:
    def __init__(self, make_timelapse_capture_dir=True, capture_store_dir=None, capture_main_dir_name=None):
        self.make_capture_dir = make_timelapse_capture_dir
        
        if self.make_capture_dir:
            # Generate a sub-folder name based on the current date and time
            date = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            print('New images are capturing at time (sub-folder name) >>> ', date)

            # Set the directory where captures will be stored
            current_path = os.getcwd() if capture_store_dir is None else capture_store_dir
            captures_main_dir = 'CameraCaptures' if capture_main_dir_name is None else capture_main_dir_name
            captures_main_dir_path = os.path.join(current_path, captures_main_dir)

            # Create the main directory if it doesn't exist
            if not os.path.exists(captures_main_dir_path):
                os.mkdir(captures_main_dir_path)

            # Set read and write permissions for the main directory
            cmd_line = 'sudo chmod a+w ' + captures_main_dir_path
            run_chmod = subprocess.Popen(cmd_line, shell=True, stderr=subprocess.PIPE,
                                         stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                         universal_newlines=False)
            run_chmod.stdout.read()

            # Create a new sub-folder for the current capture session
            new_capture_folder_path = os.path.join(captures_main_dir_path, str(date))
            os.mkdir(new_capture_folder_path)

            # Set read and write permissions for the new sub-folder
            cmd_line = 'sudo chmod a+w ' + new_capture_folder_path
            run_chmod = subprocess.Popen(cmd_line, shell=True, stderr=subprocess.PIPE,
                                         stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                         universal_newlines=False)
            run_chmod.stdout.read()

            self.captures_main_dir_path = captures_main_dir_path
            self.new_capture_folder_path = new_capture_folder_path

        elif not self.make_capture_dir:
            print('Captured image(s) will be stored in the current directory!')

        else:
            print('Error in making a directory to store captured image(s)!')
                
    def capture_single_picture(self, img_width, img_height, img_file_name, img_file_ext,
                              iso, shutter_speed, white_balance, rgain, bgain,
                              cam_num=0, frame_mode=0, framerate=15, ex_mode='antishake',  
                              img_brightness=50, img_contrast=0, img_saturation=0, img_sharpness=0,
                              jpeg_quality=100):
        
        image_file_path = str(img_file_name) + str(img_file_ext)
        
        if self.make_capture_dir:
            image_file = str(img_file_name) + str(img_file_ext)
            image_file_path = os.path.join(self.new_capture_folder_path, str(image_file))
        
        print(image_file_path)
        print('Capturing image, please wait...')   
        
        cmd_line = self.capture_picture(cam_num, img_width, img_height, image_file_path,
                                        iso, shutter_speed, white_balance, rgain, bgain,
                                        frame_mode, framerate, ex_mode,  
                                        img_brightness, img_contrast, img_saturation, img_sharpness,
                                        jpeg_quality)
        
        try:
            print(cmd_line)
            run_cam = self.run_raspi_cam(cmd_line)
            output_run_cam = run_cam.communicate()
        except:
            print('Error in capturing a single image!')
            pass
        
        return (image_file_path, output_run_cam)

    def capture_multiple_pictures(self, img_width, img_height, img_file_name, img_file_ext,
                                  iso, shutter_speed_array, white_balance, rgain, bgain,
                                  cam_num=0, frame_mode=0, framerate=15, ex_mode='antishake', 
                                  img_brightness=50, img_contrast=0, img_saturation=0, img_sharpness=0,
                                  jpeg_quality=100):
        
        image_file_path_list = []
        output_run_cam_list = []
        
        for i in range(len(shutter_speed_array)):
            shutter_speed = shutter_speed_array[i]
            img_file_name_x = img_file_name + '_' + str(i+1)
            print('Capturing image >>> ', str(i+1))   

            image_file_path = str(img_file_name_x) + str(img_file_ext)
            
            if self.make_capture_dir:
                image_file = str(img_file_name_x) + str(img_file_ext)
                image_file_path = os.path.join(self.new_capture_folder_path, str(image_file))
            
            print(image_file_path)
            
            cmd_line = self.capture_picture(cam_num, img_width, img_height, image_file_path,
                                            iso, shutter_speed, white_balance, rgain, bgain,
                                            frame_mode, framerate, ex_mode,  
                                            img_brightness, img_contrast, img_saturation, img_sharpness,
                                            jpeg_quality)
            
            try:
                run_cam = self.run_raspi_cam(cmd_line)
                output_run_cam = run_cam.communicate()

                image_file_path_list.append(image_file_path)
                output_run_cam_list.append(output_run_cam)
            except:
                print('Error in capturing multiple images, non-stereo mode!')
                image_file_path_list.append(np.nan)
                output_run_cam_list.append(np.nan)
                pass
            
        return (image_file_path_list, output_run_cam_list)

    def capture_picture(self, cam_num, img_width, img_height, image_file_path,
                        iso, shutter_speed, white_balance, rgain, bgain,
                        frame_mode, framerate, ex_mode,  
                        img_brightness, img_contrast, img_saturation, img_sharpness,
                        jpeg_quality):
        
        cmd_line = 'sudo raspistill -cs ' + str(cam_num) + \
                   ' -w ' + str(img_width) + \
                   ' -h ' + str(img_height) + \
                   ' -md ' + str(frame_mode) + \
                   ' -ISO ' + str(iso) + \
                   ' -ss ' + str(shutter_speed) + \
                   ' -ex ' + str(ex_mode) + \
                   ' -awb ' + str(white_balance) + \
                   ' -awbg ' + str(rgain) + ',' + str(bgain) + \
                   ' -br ' + str(img_brightness) + \
                   ' -co ' + str(img_contrast) + \
                   ' -sa ' + str(img_saturation) + \
                   ' -sh ' + str(img_sharpness) + \
                   ' -q ' + str(jpeg_quality) + \
                   ' -o ' + str(image_file_path) + \
                   ' --nopreview'

        return cmd_line
    
    def run_raspi_cam(self, cmd_line):
        run_cam = subprocess.Popen(cmd_line, shell=True, stderr=subprocess.PIPE, 
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE,  
                                   universal_newlines=False)
        return run_cam
