import pygame
import rtmidi
import sys
import time

import ctypes
from ctypes import wintypes


import pythoncom, sys, logging
import pyWinhook as pyHook


# Initialize pygame
pygame.init()

display = pygame.display.set_mode((300, 300))
pygame.display.set_caption("Mapping monitor")
font = pygame.font.SysFont('Arial', 30)
clock = pygame.time.Clock()


duration = 100 #Duration of scene 1

global i
i = 0

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
                    text = str(counter).rjust(3) 
                if counter == 0:
                    # Send a note on message to the MIDI output
                    note_on = [0x90, 90, 1] # channel 1, middle A, velocity 112
                    midiout.send_message(note_on)
                    time.sleep(200/1000)
                    # Send a note off message to the MIDI output
                    note_off = [0x80, 90, 0] # channel 1, middle A, velocity 0
                    midiout.send_message(note_off)
                    text = str("Scene switch") 
        
            if event == EventP:
                counter = duration
                i = i + 1 

            hm = pyHook.HookManager()
            hm.KeyDown = OnKeyboardEvent
            hm.HookKeyboard()

            display.fill((255, 255, 255))
            text_played = font.render(str(i), True, (0,0,0))
            display.blit(text_played, (25, 25))
            display.blit(font.render(text, True, (0, 0, 0)), (150, 25))
            pygame.display.flip()
            clock.tick(60)
        