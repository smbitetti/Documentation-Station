import sys

import os

import pygame

import pygame.camera
import datetime
import time
import RPi.GPIO as GPIO

import subprocess
from subprocess import call


GPIO.setmode(GPIO.BCM)



GPIO.setup(16, GPIO.IN, pull_up_down = GPIO.PUD_UP)

GPIO.setup(13, GPIO.IN, pull_up_down = GPIO.PUD_UP)

pygame.init()

pygame.camera.init()



#create fullscreen display

screen = pygame.display.set_mode((700, 400), 0)



#find, open and start cam

cam_list = pygame.camera.list_cameras()

webcam = pygame.camera.Camera(cam_list[0], (800,480))

webcam.start()

#webcam2 = pygame.camera.Camera(cam_list[1], (32,24))

#webcam2.start()

font = pygame.font.Font(None, 25)

i = 0

usbnames = []
pinames = []
hi =str(datetime.datetime.now().date())
hi = hi.replace(".", "_")
hi = hi.replace(" ", "_")
hi = hi.replace(":", "_")
print (hi)
path = "/home/pi/Pictures/%s" %hi
path2 = "/mnt/USB/%s" %hi
print (path)
ti =str(datetime.datetime.now().time())
ti = ti.replace(".", "_")
ti = ti.replace(" ", "_")
ti = ti.replace(":", "")
ti = ti[0:4]
if os.path.exists(path) is False:
        os.mkdir(path, 0o777);
        new = "/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload " + path + " " + hi
        call([new], shell=True)
        path = path + "/" + ti
        os.mkdir(path, 0o777)
else:
        path = path + "/" + ti
        os.mkdir(path, 0o777)
if os.path.exists(path2) is False:
        os.mkdir(path2, 0o777)
        path2 = path2 + "/" + ti
        os.mkdir(path2, 0o777)
else:
        path2 = path2 + "/" + ti
        os.mkdir(path2, 0o777)                 
                

def record(runtime):

        global i
        global path
        global hi
        start_time = time.time()

        last_frame = 0

        current_frame = 0

        j = 0

        fps = 0


        if True :

                        #grab image...

                        time_left = int(runtime - (time.time() - start_time))

                        imagen = webcam.get_image()

                        imagen = pygame.transform.scale(imagen, (800, 480))



                        last_frame = current_frame

                        current_frame = time.time()

                        fps = 1/(current_frame - last_frame)



                        #display_time = "FPS: %d   Time left: %d" %(fps, time_left)

                        #text = font.render(display_time, True, (255,255,255))


                        screen.blit(imagen, (0,0))

                        usbname = "/mnt/USB/%(1)s/%(3)s/image_%(2)s.jpg" % {"1" : hi, "2":i, "3":ti}
                        piname = "/home/pi/Pictures/%(1)s/%(3)s/image_%(2)s.jpg" % {"1" : hi, "2":i, "3":ti}
                        print ("file name " + usbname)
                        print ("pi name " + piname)
                        print (path + " " + path2)
                        pygame.image.save(imagen, usbname)
                        pygame.image.save(imagen, piname)

                        usbnames.append(usbname)
                        pinames.append(piname)
                        

                        #cmd = "cd /home/pi/Desktop/Dropbox-Uploader;./dropbox_uploader.sh upload /home/pi/Desktop/Dropbox-Uploader/ /"

                        # no block, it starts a sub process.

                        #p = subprocess.Popen(cmd , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


                        #draw all updates

                        pygame.display.update()

                        i = i+1

                        #check for quite events

                        #for event in pygame.event.get():

                                #if event.type == pygame.QUIT:

                                        #webcam.stop()

                                        #pygame.quit()

                                        #sys.exit()


                        j = j +1
        return usbnames, pinames



while True:



        runtime = 0

        start_time = time.time()

        last_frame = 0

        current_frame = 0

        fps = 0

        usbnames = []
        pinames =[]

        #grab image...

        time_left = int(runtime - (time.time() - start_time))

        imagen = webcam.get_image()

        imagen = pygame.transform.scale(imagen, (800, 480))



        last_frame = current_frame

        current_frame = time.time()

        fps = 1/(current_frame - last_frame)

        screen.blit(imagen, (0,0))

        display_msg = "Press the button to take pictures!"

        text2 = font.render(display_msg, True, (0,0,255))

        #have screenfill with current image if possible

        #screen.fill((0,0,0))

        screen.blit(text2, (220, 220))

        pygame.display.update()



        input_state = GPIO.input(16)

        if input_state == False:



       #folder_name = "/var/www"

               # os.makedirs(folder_name)

                usbnames, pinames = record(1)

                print ("here")


                screen.fill((0,0,0))

                delete_option = "Press button again to delete?"

                text4 = font.render(delete_option, True, (255,255,255))



                screen.blit(text4, (220, 220))

                pygame.display.update()



                cur_time = time.time()



                while time.time() - cur_time < 6:

                        input_state2 = GPIO.input(16)

                        if input_state2 == False:

                                for piname in pinames:
                                        for usbname in usbnames:
                                                os.remove(usbname)
                                        os.remove(piname)
                                break

        
        input_state3 = GPIO.input(13)
        
        if input_state3 == False:
                photoname = "New"
                newname= "/home/pi/Pictures/New"
                
                
                photofile = "/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload " + path + " " + hi
                call([photofile], shell=True)
                screen.fill((0,0,0))

                thank_you = "Thanks for your pictures!"

                text3 = font.render(thank_you, True, (255,255,255))



                screen.blit(text3, (220, 220))

                pygame.display.update()



                time.sleep(2)
                webcam.stop()

                pygame.quit()

                sys.exit()
while True:
        
        input_state3 = GPIO.input(13)
        print ('here')
        if input_state3 == False:
                events = pygame.event.get()
                                                                                                                                                                                                                
        for event in events:

                if event.type == pygame.QUIT:

                        webcam.stop()

                        pygame.quit()

                        sys.exit()
                



        
