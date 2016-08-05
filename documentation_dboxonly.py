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




pygame.init()

pygame.camera.init()
print ("here")
#create fullscreen display

screen = pygame.display.set_mode((700, 400), pygame.FULLSCREEN)

#find, open and start cam

cam_list = pygame.camera.list_cameras()

webcam = pygame.camera.Camera(cam_list[0], (800,480))

webcam.start()

font = pygame.font.Font(None, 25)


paths = []
pinames = []
comp = datetime.datetime.now().date()
hi =str(datetime.datetime.now().date())
hi = hi.replace(".", "_")
hi = hi.replace(" ", "_")
hi = hi.replace(":", "_")
paths.append("/home/pi/Pictures/%s" %hi)

stamp = partners
if os.path.exists(paths[count]) is False:
        os.mkdir(paths[count], 0o777);
        new = "/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload " + paths[count] + " " + hi
        call([new], shell=True)
        paths[count] = paths[count] + "/" + partners
        os.mkdir(paths[count], 0o777)
else:
        paths[count] = paths[count] + "/" + partners
        os.mkdir(paths[count], 0o777)

def record(runtime):

        global i
        print ("here")
        global paths
        global count
        
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

                        fps = 1/(current_frame - last_frame)

                        screen.blit(imagen, (0,0))

                        ti =str(datetime.datetime.now().time())
                        ti = ti.replace(".", "_")
                        ti = ti.replace(" ", "_")
                        ti = ti.replace(":", "")
                        ti = ti[0:4]

                        piname = "/home/pi/Pictures/%(1)s/%(4)s/%(3)s_%(2)s.jpg" % {"1" : hi, "2":i, "3":ti, "4":partners}
                        
                        
                        pygame.image.save(imagen, piname)
                        
                        pinames.append(piname)

                        pygame.display.update()

                        i = i+1
                        
        return pinames



while True:

        runtime = 0

        start_time = time.time()

        last_frame = 0

        current_frame = 0

        fps = 0

        
        pinames =[]

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

                pinames = record(1)

                delete_option = "Press button again to delete?"

                text4 = font.render(delete_option, True, (255,255,255))

                screen.blit(text4, (220, 220))

                pygame.display.update()

                cur_time = time.time()

                while time.time() - cur_time < 4 or input_state2 == False :

                        input_state2 = GPIO.input(16)

                        if input_state2 == False:

                                for piname in pinames:
                                        os.remove(piname)
                                time.sleep(0.5)
                                break
        
        input_state3 = GPIO.input(13)
        
        if input_state3 == False:
                for path in paths:
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
        
        input_state4 = GPIO.input(21)
            
        if input_state4 == False:
            screen = pygame.display.set_mode((0, 0), 0)
            road = ""
            if (datetime.datetime.now().date() != comp):
                hi =str(datetime.datetime.now().date())
                hi = hi.replace(".", "_")
                hi = hi.replace(" ", "_")
                hi = hi.replace(":", "_")
            road = "/home/pi/Pictures/%s" %hi
            if os.path.exists(road) is False:
                os.mkdir(road, 0o777);
                new = "/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload " + road + " " + hi
                call([new], shell=True)
           
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
                screen = pygame.display.set_mode((700, 400), pygame.FULLSCREEN)

            road = road + "/" + partners
            if os.path.exists(road) is False:
                os.mkdir(road, 0o777)
            if partners !=  stamp or hi != comp:
                paths.append(road)
                count +=1
            stamp = partners

