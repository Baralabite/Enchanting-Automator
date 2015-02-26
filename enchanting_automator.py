#===============[Imports]===============#
import ctypes
import time
import win32api, win32con

#===============[Constants]===============#
keys = {0: 0x30, 1:0x31, 2:0x32, 3:0x33, 4:0x34, 5:0x35, 6:0x36, 7:0x37, 8:0x38, 9:0x39,
        "a":0x41, "b":0x41, "c":0x43, "d":0x44, "e":0x45, "f":0x46, "g":0x47, "h":0x48, "i":0x49,
         "j":0x4A, "k":0x4B, "l":0x4C, "m":0x4D, "n":0x4E, "o":0x4F, "p":0x50, "q":0x51, "r":0x52,
         "s":0x53, "t":0x54, "u":0x55, "v":0x56, "w":0x57, "x":0x58, "y":0x59, "z":0x5A,  "/":0x6F,
        " ":0x20}

#===============[Support Code]===============#
SendInput = ctypes.windll.user32.SendInput
# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

#===============[Functions]===============#

def pressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( hexKeyCode, 0x48, 0, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def releaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( hexKeyCode, 0x48, 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def typeKey(hexKeyCode, uppercase=False):
    if uppercase:
        pressKey(0xA0)
    pressKey(hexKeyCode)
    releaseKey(hexKeyCode)
    if uppercase:
        releaseKey(0xA0)

def typeString(string):
    for c in string:
        typeKey(keys[c])

def typeCommand(string):
    typeString("t") #Opens chat box
    time.sleep(0.1)
    typeString(string) #Types string
    time.sleep(0.1)
    typeKey(0x0D) #Enter

def moveMouse(pos):
    win32api.SetCursorPos(pos)

def leftClick(pos):
    moveMouse(pos)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,pos[0],pos[1],0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,pos[0],pos[1],0,0)

def rightClick(pos):
    moveMouse(pos)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,pos[0],pos[1],0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,pos[0],pos[1],0,0)

def clickDrag(pos1, pos2):
    moveMouse(pos1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,pos1[0],pos1[1],0,0)
    moveMouse(pos2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,pos2[0],pos2[1],0,0)
