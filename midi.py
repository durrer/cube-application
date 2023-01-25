import pygame
import rtmidi
import sys
import time
import json

import ctypes
from ctypes import wintypes


import pythoncom, sys, logging
import pyWinhook as pyHook

import datetime

 # Initialize pygame
pygame.init()

display = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Mapping monitor")
font = pygame.font.SysFont('Arial', 30)
clock = pygame.time.Clock()

global i
i = int(input("Initial number of starts : "))

global duration
duration = 412 #Duration of scene 1

counter, text = duration, "Let's gooo!"
pygame.time.set_timer(pygame.USEREVENT, 1000)


#Always on top 
hwnd = pygame.display.get_wm_info()['window']
user32 = ctypes.WinDLL("user32")
user32.SetWindowPos.restype = wintypes.HWND
user32.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, wintypes.INT, wintypes.INT, wintypes.INT, wintypes.INT, wintypes.UINT]
user32.SetWindowPos(hwnd, -1, 600, 300, 0, 0, 0x0001)


EventP=pygame.event.Event(pygame.USEREVENT, attr1='EventP')
EventA=pygame.event.Event(pygame.USEREVENT, attr1='EventA')

def OnKeyboardEvent(event):            
    if event.Ascii == 112:  # key pressed is 'p'
        if counter < 390: 
            print ("Key P detected")
            logging.log(10,chr(event.Ascii))
            # Send a note on message to the MIDI output
            note_on = [0x90, 60, 1] # channel 1, middle C, velocity 112
            midiout.send_message(note_on)
            time.sleep(200/1000)
            # Send a note off message to the MIDI output
            note_off = [0x80, 60, 0] # channel 1, middle C, velocity 0
            midiout.send_message(note_off)
            pygame.event.post(EventP)
            # Data to be written
            x = datetime.datetime.now()
            dictionary = {
                "id": i,
                "year": x.year,
                "month": x.month,
                "day": x.day,
                "time":x.strftime("%H:%M:%S")
            }
 
            # Serializing json
            json_object = json.dumps(dictionary, indent=5)
 
            # Writing to sample.json
            with open("data.txt", "a") as outfile:
                outfile.write(json_object)
            return True          
    if event.Ascii == 97: #key pressed is 'a'
        print ("Key A detected")                                     
        # Send a note on message to the MIDI output
        note_on = [0x90, 90, 1] # channel 1, middle C, velocity 112
        midiout.send_message(note_on)
        time.sleep(200/1000)
        # Send a note off message to the MIDI output
        note_off = [0x80, 90, 0] # channel 1, middle C, velocity 0
        midiout.send_message(note_off)
        return True
    else:
        return True

# Create a new MIDI out object
midiout = rtmidi.MidiOut()

# Open the first available MIDI output port
available_ports = midiout.get_ports()
if available_ports:
    print(available_ports)
    midiout.open_port(1)
else:
    print("FAIL")

# Main loop
while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Close the MIDI output
                del midiout
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT: 
                counter -= 1
                if counter != 0:
                    counter_text = abs(counter)
                    if counter < 0:
                        text_before = "Od poslední návštevy uběhlo: "
                    else:
                        text_before = ""
                    text_H =  counter_text // 3600
                    text_M = (counter_text % 3600) // 60
                    text_S = (counter_text % 3600) % 60
                    text = text_before + str(text_H)+ " H " + str(text_M)+ " M " + str(text_S)+ " S"
                    #text = str(counter).rjust(3) 
                if counter == 0:
                    # Send a note on message to the MIDI output
                    note_on = [0x90, 90, 1] # channel 1, middle A, velocity 112
                    midiout.send_message(note_on)
                    time.sleep(200/1000)
                    # Send a note off message to the MIDI output
                    note_off = [0x80, 90, 0] # channel 1, middle A, velocity 0
                    midiout.send_message(note_off)
                    text = str("Scene switch") 
                    print ("Scene switch")
        
            if event == EventP:
                counter = duration
                i = i + 1 

            hm = pyHook.HookManager()
            hm.KeyDown = OnKeyboardEvent
            hm.HookKeyboard()

            display.fill((0, 0, 0))
            text_played_string = "{} people have already seen".format(i) 
            
            text_played = font.render(str(text_played_string), True, (255,255,255))
            display.blit(text_played, (25, 25))
            display.blit(font.render(text, True, (255, 255, 255)), (25, 125))
            pygame.display.flip()
            clock.tick(60)
        