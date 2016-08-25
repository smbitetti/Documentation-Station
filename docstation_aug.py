#!/usr/bin/python3.4
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

screen = pygame.display.set_mode((800, 480), pygame.FULLSCREEN)

#find, open and start cam

cam_list = pygame.camera.list_cameras()

webcam = pygame.camera.Camera(cam_list[0], (800,480))

webcam.start()

paths = []
usbnames = []
comp = datetime.datetime.now().date()
hi = str(datetime.datetime.now().date())
hi = hi.replace(".", "_")
hi = hi.replace(" ", "_")
hi = hi.replace(":", "_")
#paths.append("/home/pi/usbdrv/%s" %hi)


font = pygame.font.Font(None, 25)

i = 0

def record(runtime):
        global path

        global hi
        
        global i

        start_time = time.time()

        last_frame = 0

        current_frame = 0

        fps = 0

        if True :

                        #grab image...

                        time_left = int(runtime - (time.time() - start_time))

                        imagen = webcam.get_image()

                        imagen = pygame.transform.scale(imagen, (800, 480))



                        last_frame = current_frame
                        current_frame = time.time()
                        ti =str(datetime.datetime.now().time())
                        ti = ti.replace(".", "_")
                        ti = ti.replace(" ", "_")
                        ti = ti.replace(":", "")
                        ti = ti[0:4]

                        fps = 1/(current_frame - last_frame)



                        #display_time = "FPS: %d   Time left: %d" %(fps, time_left)

                        #text = font.render(display_time, True, (255,255,255))



                        screen.blit(imagen, (0,0))



                        usbname = "/home/pi/usbdrv/Photos/%(1)s_%(2)s_%(3)s.jpg" % {"1": hi,"2": ti,"3" : i}

                        pygame.image.save(imagen, usbname)

                        usbnames.append(usbname)

                        pygame.display.update()

                        i = i+1

        return usbnames



while True:



        runtime = 0

        start_time = time.time()

        last_frame = 0

        current_frame = 0

        fps = 0

        usbnames = []

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


       #big pushbutton to take picture 
        input_state = GPIO.input(16)

        if input_state == False:


                usbnames = record(1)

                delete_option = "Press button again to delete?"

                text4 = font.render(delete_option, True, (255,255,255))


                screen.blit(text4, (220, 220))

                pygame.display.update()
                
                cur_time = time.time()

                time.sleep(0.5)


                while time.time() - cur_time < 4 or input_state2 == False :

                        input_state2 = GPIO.input(16)

                        if input_state2 == False:
                                
                                for usbname in usbnames:
                                        
                                         os.remove(usbname)
                                         
                                time.sleep(0.5)
                                
                                break
        #exit documentation program and take to homescreen

        input_state3 = GPIO.input(13)

        
        if input_state3 == False:
                
                        screen.fill((0,0,0))

                        thank_you = "Thanks for your pictures! Don't forget to upload new photos from thumb drive!"

                        text3 = font.render(thank_you, True, (255,255,255))
			text3rect = text3.get_rect()
			text3rect.centerx = screen.get_rect().centerx
			text3rect.centery = screen.get_rect().centery
                        screen.blit(text3, text3rect)

                        pygame.display.update()

                        time.sleep(4)
                        webcam.stop()

                        pygame.quit()

                        sys.exit()

        
