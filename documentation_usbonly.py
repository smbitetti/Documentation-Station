#!/usr/bin/python3.4
import sys

import os

import pygame
from tkinter import *
import pygame.camera
import datetime
import time
import RPi.GPIO as GPIO

import subprocess
from subprocess import call


GPIO.setmode(GPIO.BCM)

GPIO.setup(16, GPIO.IN, pull_up_down = GPIO.PUD_UP)

GPIO.setup(13, GPIO.IN, pull_up_down = GPIO.PUD_UP)

GPIO.setup(21, GPIO.IN, pull_up_down = GPIO.PUD_UP)

pygame.init()

pygame.camera.init()

#create fullscreen display

screen = pygame.display.set_mode((700, 400), pygame.FULLSCREEN)

pygame.display.toggle_fullscreen

#find, open and start cam

cam_list = pygame.camera.list_cameras()

webcam = pygame.camera.Camera(cam_list[0], (800,480))

webcam.start()

#webcam2 = pygame.camera.Camera(cam_list[1], (32,24))

#webcam2.start()

font = pygame.font.Font(None, 25)

count = 0
i = 0
partners = ""

class Checkbar(Frame):
    def __init__(self, parent = None, picks = []):
        Frame.__init__(self,parent)
        self.vars = []
        self.counter = 1
        self.words = picks
        self.chks = []
        for pick in picks:
            var = StringVar()
            chk = Checkbutton(self, text = pick, variable = var, onvalue = pick, offvalue = "")
            self.chks.append(chk)
            if self.counter >= 21:
                chk.grid(row = self.counter - 20, column = 30, columnspan = 10, sticky = W+E, padx = 100, pady = 10)
            elif self.counter >= 11:
                chk.grid(row = self.counter - 10, column = 15, columnspan = 10, sticky = W+E, padx = 100, pady = 10)
            else:
                chk.grid(row = self.counter, column = 0, columnspan = 10, sticky = W+E, padx = 100, pady = 10)
            self.counter += 1
            self.vars.append(var)
        ok_button = Button(self, text="OK", command = self.check_button)
        ok_button.grid(row = 0, sticky = W+E)
    def check_button(self):
        global partners
        partners = ""
        p = 0
        for var in self.vars:
            if var.get():
                if partners == "":
                    partners = self.chks[p].config('onvalue')[-1]
                else:
                    partners = partners + "_" + self.chks[p].config('onvalue')[-1]
            p+=1
        root.destroy()
if __name__ == '__main__':
    root =Tk()
    root.attributes('-fullscreen', True)
    with open('roster.txt', 'r') as f:
        data = f.readlines()
        for line in data:
            words = line.split()
    lng = Checkbar(root, words)
    lng.pack(side =TOP, fill = X)
    lng.config(relief=GROOVE, bd = 2)

    Button(root, text = 'Quit', command = root.quit()).pack(side=RIGHT)
    root.mainloop()

paths = []
usbnames = []
comp = datetime.datetime.now().date()
hi =str(datetime.datetime.now().date())
hi = hi.replace(".", "_")
hi = hi.replace(" ", "_")
hi = hi.replace(":", "_")
paths.append("/media/flash/%s" %hi)

stamp = partners
if os.path.exists(paths[count]) is False:
        os.mkdir(paths[count], 0o777);
        paths[count] = paths[count] + "/" + partners
        os.mkdir(paths[count], 0o777)
else:
        paths[count] = paths[count] + "/" + partners
        os.mkdir(paths[count], 0o777)

def record(runtime):

        global i
        
        global path
        
        global hi
        
        start_time = time.time()

        last_frame = 0

        current_frame = 0

        fps = 0

        if True :

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

                        screen.blit(imagen, (0,0))

                        usbname = "/media/flash/%(1)s/%(2)s/%(3)s_%(4)s.jpg" % {"1" : hi, "2":partners, "3":ti, "4": i}

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

        time_left = int(runtime - (time.time() - start_time))

        imagen = webcam.get_image()

        imagen = pygame.transform.scale(imagen, (800, 480))

        last_frame = current_frame

        current_frame = time.time()

        fps = 1/(current_frame - last_frame)

        screen.blit(imagen, (0,0))

        display_msg = "Press the button to take pictures!"

        text2 = font.render(display_msg, True, (0,0,255))

        screen.blit(text2, (220, 220))

        pygame.display.update()

        input_state = GPIO.input(16)

        if input_state == False:

                usbnames = record(1)

                delete_option = "Press button again to delete?"

                text4 = font.render(delete_option, True, (255,255,255))

                screen.blit(text4, (220, 220))

                pygame.display.update()

                cur_time = time.time()

                while time.time() - cur_time < 4 or input_state2 == False :

                        input_state2 = GPIO.input(16)

                        if input_state2 == False:
                                for usbname in usbnames:
                                         os.remove(usbname)
                                time.sleep(0.5)
                                break
        
        input_state3 = GPIO.input(13)
        
        if input_state3 == False:
                
                screen.fill((0,0,0))

                thank_you = "Thanks for your pictures!"

                text3 = font.render(thank_you, True, (255,255,255))

                screen.blit(text3, (220, 220))

                pygame.display.update()

                time.sleep(2)
                webcam.stop()

                pygame.quit()

                sys.exit()

        input_state4 = GPIO.input(21)
            
        if input_state4 == False:
            screen = pygame.display.set_mode((0, 0), 0)
            road = ""
            if (datetime.datetime.now().date() != comp):
                hi =str(datetime.datetime.now().date())
                hi = hi.replace(".", "_")
                hi = hi.replace(" ", "_")
                hi = hi.replace(":", "_")
            road = "/media/flash/%s" %hi

            if os.path.exists(road) is False:
                os.mkdir(road, 0o777)

            if __name__ == '__main__':
                root =Tk()
                with open('roster.txt', 'r') as f:
                    data = f.readlines()
                    for line in data:
                        words = line.split()
                lng = Checkbar(root, words)
                lng.pack(side =TOP, fill = X)
                lng.config(relief=GROOVE, bd = 2)
                Button(root, text = 'Quit', command = root.quit()).pack(side=RIGHT)
                root.mainloop()

            road = road + "/" + partners
            if os.path.exists(road) is False:
                os.mkdir(road, 0o777)
            if partners !=  stamp or hi != comp:
                paths.append(road)
                count +=1
            stamp = partners
      

                
