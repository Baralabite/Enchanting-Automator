#===============[Imports]===============#
import ctypes
import time
import win32api, win32con
from PIL import ImageGrab

##TODO Need to fix spider shover timing a little
##TODO Need to make sure to get lapis/book out of table before leaving

#===============[Constants]===============#

#List of Virtual Key Codes, and their corresponding ascii characters
keys = {0: [0x30], 1:[0x31], 2:[0x32], 3:[0x33], 4:[0x34], 5:[0x35], 6:[0x36], 7:[0x37], 8:[0x38], 9:[0x39],
        "a":[0x41], "b":[0x41], "c":[0x43], "d":[0x44], "e":[0x45], "f":[0x46], "g":[0x47], "h":[0x48], "i":[0x49],
         "j":[0x4A], "k":[0x4B], "l":[0x4C], "m":[0x4D], "n":[0x4E], "o":[0x4F], "p":[0x50], "q":[0x51], "r":[0x52],
         "s":[0x53], "t":[0x54], "u":[0x55], "v":[0x56], "w":[0x57], "x":[0x58], "y":[0x59], "z":[0x5A],  "/":[0x6F],
        " ":[0x20], "ENTER":[0x0D], "_":[0xA0, 0xBD], "SHIFT":[0xA0], "ESCAPE":[0x1B]}

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

"""
Presses key

Hex hexKeyCode: Virtual Key Code to simulate pressing. Keys dict has vkc to unicode
"""
def pressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( hexKeyCode, 0x48, 0, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

"""
Releases pressed key

Hex hexKeyCode: Virtual Key Code to simulate releasing. Keys dict has vkc to unicode
"""
def releaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( hexKeyCode, 0x48, 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

"""
Types a key, giving option press shift while doing so

Hex   hexKeyCode: Press and release specified hexKeyCode. Keys dict has vkc to unicode
Bool  uppercase: Specified whether shift should be pressed while typing key.
"""
def typeKey(hexKeyCode, uppercase=False):
    if uppercase:
        pressKey(0xA0)
    pressKey(hexKeyCode)
    releaseKey(hexKeyCode)
    if uppercase:
        releaseKey(0xA0)

def typeKeys(keyCodes):
    for k in keyCodes:
        pressKey(k)
    for k in keyCodes:
        releaseKey(k)


"""
Types a string

Str string: Types a specified string. Only works for characters from a-z and /
"""
def typeString(string):
    for c in string:
        typeKeys(keys[c])

"""
Opens chat box, types command, and presses enter

Str string: Command to type
"""
def typeCommand(string):
    typeString("t")             #Opens chat box
    time.sleep(0.1)
    typeString(string)          #Types string
    time.sleep(0.1)
    typeKeys(keys["ENTER"])         #Executes command

"""
tuple pos: (x,y) tuple for where to move the mouse
"""
def moveMouse(pos):
    win32api.SetCursorPos(pos)

"""
Left click at pos

tuple pos: (x,y) tuple for where to move and click the mouse
"""
def leftClick(pos):
    moveMouse(pos)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,pos[0],pos[1],0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,pos[0],pos[1],0,0)

def leftClick_(pos):
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,pos[0],pos[1],0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,pos[0],pos[1],0,0)

"""
Right click at pos

tuple pos: (x,y) tuple for where to move and click the mouse
"""
def rightClick(pos):
    moveMouse(pos)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,pos[0],pos[1],0,0)
    time.sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,pos[0],pos[1],0,0)

"""
Click and drags the mouse

tuple pos1: (x,y) Where to left click mouse
tuple pos2: (x,y) Where to drag the mouse while clicked, and then release
"""
def clickDrag(pos1, pos2):
    moveMouse(pos1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,pos1[0],pos1[1],0,0)
    moveMouse(pos2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,pos2[0],pos2[1],0,0)

"""
Takes a screenshot and saves it as a PIL image type

Tuple crop: (x1, y1, x2, y2) Area to crop
"""
def getImage(crop=None):
    img = ImageGrab.grab()
    if not crop == None:
        img = img.crop(crop)
    return img

"""
Gets average RGB color of image

PILImage img: image to get the average color of
"""
def getAverageRGB(img):
    width, height = img.size
    pixels = img.load()
    r = 0; g = 0; b = 0; cnt = 0    
    for x in range(width):
        for y in range(height):
            cpixel = pixels[x, y]
            r = r + cpixel[0]
            g = g + cpixel[1]
            b = b + cpixel[2]
            cnt += 1
    r = r/cnt
    g = g/cnt
    b = b/cnt
    return (r, g, b)

"""
Saves PIL image as jpeg

Str   filename: Filename to save screenshot as
"""
def saveImage(filename, img):
    img.save(filename, "JPEG")

"""
Compares the img with an average rgb tuple comp

PILImage img: Input image to compare
tuple comp: (r, g, b) Tuple to compare to
"""
def screenLike(img, comp):
    avg = getAverageRGB(img)
    if (avg[0] > comp[0]-Constants.COMPARE_THRESHOLD and avg[0] > comp[0]+Constants.COMPARE_THRESHOLD and
        avg[1] > comp[1]-Constants.COMPARE_THRESHOLD and avg[1] > comp[1]+Constants.COMPARE_THRESHOLD and
        avg[2] > comp[2]-Constants.COMPARE_THRESHOLD and avg[2] > comp[2]+Constants.COMPARE_THRESHOLD):
        return True
    else:
        return False

def countdown(t):
    for x in range(t):
        if x % 5 == 0:
            print("Time: "+str(x)+"s")
        time.sleep(1)
    

#===============[Automation]===============#
class Constants:
    SCREEN_RESOLUTION = (1366, 768)
    CENTER_SCREEN = (int(SCREEN_RESOLUTION[0]/2),int(SCREEN_RESOLUTION[1]/2))
    COMPARE_THRESHOLD = 10

    BOOK_SLOT       = (820, 510)
    LAPIS_SLOT      = (780, 510)
    ENC_BOOK_SLOT   = (550, 320)
    ENC_LAPIS_SLOT  = (590, 320)
    LVL_30_SLOT     = (720, 330)

    HOME_PREFIX     = "auto_"
    QUAD_SPAWNER    = HOME_PREFIX + "quad_spawn"
    LIGHT_SWITCH    = HOME_PREFIX + "light"
    SPIDER_SHOVE    = HOME_PREFIX + "spider_shove"
    KILLING_AREA    = HOME_PREFIX + "kill"
    ENCHANTING_AREA = HOME_PREFIX + "enchant"
    ITEM_DROPOFF    = HOME_PREFIX + "dropoff"
    RECEIVE_XP      = HOME_PREFIX + "recv_xp"
    
    

"""
Starting Conditions:
Lights: On
Spider Shove: Off

Slot 1: Books
Slot 2: Lapis
"""

class Grind:
    def __init__(self):
        self.running = False
        self.currentPos = "null"

        self.lightStatus = True
        self.spiderShove = False

        self.currentSlot = 7

    def teleport(self, home):
        typeCommand("/home "+home)
        self.currentPos = home

    def setSlot(self, slot):
        typeKey(keys[slot][0])
        self.currentSlot = slot

    """
    Based upon the starting conditions, sets the spawner light on or off
    """
    def setLight(self, state):
        if not state == self.lightStatus:
            origPos = self.currentPos
            g.teleport(Constants.LIGHT_SWITCH)
            time.sleep(0.5)
            rightClick(Constants.CENTER_SCREEN)
            time.sleep(0.5)
            g.teleport(origPos)
            self.lightStatus = state
        else:
            print("Light already in that state!")

    """
    Based upon the starting conditions, sets the spider-shove on or off
    """
    def setSpiderShove(self, state):
        if not state == self.spiderShove:
            origPos = self.currentPos
            g.teleport(Constants.SPIDER_SHOVE)
            time.sleep(0.7)
            rightClick(Constants.CENTER_SCREEN)
            time.sleep(0.7)
            g.teleport(origPos)
            self.spiderShove = state
        else:
            print("Spider Shove already in that state!")

    def openEnchantingTable(self):
        origPos = self.currentPos
        self.teleport(Constants.ENCHANTING_AREA)
        time.sleep(0.7)
        rightClick(Constants.CENTER_SCREEN)
        #time.sleep(0.7)
        #self.teleport(origPos)

    def enchantBook(self):
        origPos = self.currentPos
        self.teleport(Constants.ENCHANTING_AREA)
        time.sleep(0.7)
        rightClick(Constants.CENTER_SCREEN)
        time.sleep(0.7)


        pressKey(keys["SHIFT"][0])

        leftClick(Constants.BOOK_SLOT)
        time.sleep(0.3)
        leftClick(Constants.LAPIS_SLOT)
        time.sleep(0.3)
        leftClick(Constants.LVL_30_SLOT)
        time.sleep(0.3)
        leftClick(Constants.ENC_LAPIS_SLOT)
        time.sleep(0.3)
        leftClick(Constants.ENC_BOOK_SLOT)
        time.sleep(0.3)

        releaseKey(keys["SHIFT"][0])
        time.sleep(0.3)
        
        typeKeys(keys["ESCAPE"])
        time.sleep(0.7)

        self.teleport(origPos)

    def spamClick(self, t):
        for x in range(int(t/0.1)):
            leftClick_(Constants.CENTER_SCREEN)
            time.sleep(0.1)

    def killSpiders(self):
        origPos = self.currentPos        
        self.teleport(Constants.KILLING_AREA)

        time.sleep(0.7)
        self.setSpiderShove(True)
        time.sleep(0.7)
        
        pressKey(keys["w"][0])
        for x in range(5):
            pressKey(keys["a"][0])
            self.spamClick(4.5)
            releaseKey(keys["a"][0])
            pressKey(keys["d"][0])
            self.spamClick(4.5)
            releaseKey(keys["d"][0])
        releaseKey(keys["w"][0])

        time.sleep(0.7)
        self.setSpiderShove(False)
        time.sleep(2)
        
        self.teleport(origPos)
            
    """
    Simple function for executing test commands
    """
    def do(self):
        print("Starting grinding in 3...")        
        time.sleep(3)

        self.teleport(Constants.QUAD_SPAWNER)
        time.sleep(5)

        self.setLight(False)

        self.running = True
        self.loop()        

    def loop(self):
        wCnt = 0
        while self.running:
            countdown(140)
            self.killSpiders()
            time.sleep(1)
            self.enchantBook()
            time.sleep(1)

            #New weapon counter
            wCnt += 1
            if wCnt == 3:
                print("Needs new weapon")
                if self.currentSlot == 1:
                    print("Out of weapons! Stopping.")
                    self.running = False
                    break
                else:
                    self.setSlot(self.currentSlot-1)
                    wCnt = 0
        time.sleep(0.7)
        self.setLight(True)
        time.sleep(0.7)
        print("Finished.")
        
                
        
g = Grind()
        
