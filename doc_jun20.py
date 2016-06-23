import sys

import os

import pygame

import pygame.camera

import time

import RPi.GPIO as GPIO

import subprocess



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



def record(runtime):

        global i

        start_time = time.time()

        last_frame = 0

        current_frame = 0



        fps = 0

        filenames = []

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



                        filename = "/home/pi/usbdrv/photos/image_%s.jpg" % i

                        print (i)

                        pygame.image.save(imagen, filename)

                        filenames.append(filename)

                        cmd = "cd /home/pi/Desktop/Desktop-Uploader;./dropbox_uploader.sh upload /home/pi/Desktop/Dropbox-Uploader/ /"

                        # no block, it starts a sub process.

                        p = subprocess.Popen(cmd , shell=True,

stdout=subprocess.PIPE, stderr=subprocess.PIPE)



                        #draw all updates

                        pygame.display.update()

                        i = i+1

                        #check for quite events

                        #for event in pygame.event.get():

                                #if event.type == pygame.QUIT:

                                        #webcam.stop()

                                        #pygame.quit()

                                        #sys.exit()



        return filenames



while True:



        runtime = 0

        start_time = time.time()

        last_frame = 0

        current_frame = 0

        fps = 0

        filenames = []

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

                filenames = record(1)



                screen.fill((0,0,0))

                delete_option = "Press button again to delete?"

                text4 = font.render(delete_option, True, (255,255,255))



                screen.blit(text4, (220, 220))

                pygame.display.update()



                cur_time = time.time()



                while time.time() - cur_time < 4:

                        input_state2 = GPIO.input(16)

                        if input_state2 == False:

                                for fileName in filenames:

                                        os.remove(fileName)

                                break

                screen.fill((0,0,0))

                thank_you = "Thanks for your pictures!"

                text3 = font.render(thank_you, True, (255,255,255))



                screen.blit(text3, (220, 220))

                pygame.display.update()



                time.sleep(3)
        
        input_state3 = GPIO.input(13)
        if input_state3 == False:
                print ('got false command')                                                                                                                                                             

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
                



        
