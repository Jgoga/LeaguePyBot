import cv2
import numpy as np
from mss import mss
import time
import win32api, win32con, win32gui
import pydirectinput
from PIL import Image
import pytesseract
import concurrent.futures
import account_league
import threading
from pyWinhook import HookManager
import os
import gc

## PARAMETERS & CONSTANTS

pydirectinput.FAILSAFE = False
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

RATIO = 1

# Client
CLIENT_BOX = {'left': int(320/RATIO), 'top': int(180/RATIO), 'width': int(1280/RATIO), 'height': int(720/RATIO)}
CLIENT_LOGIN_BOX = {'left': int(480/RATIO), 'top': int(200/RATIO), 'width': int(100/RATIO), 'height': int(150/RATIO)}
CLIENT_PLAY_BOX = {'left': int(330/RATIO), 'top': int(160/RATIO), 'width': int(200/RATIO), 'height': int(80/RATIO)}
CLIENT_MATCHMAKING_BOX = {'left': int(730/RATIO), 'top': int(820/RATIO), 'width': int(250/RATIO), 'height': int(100/RATIO)}
CLIENT_GGSCREEN_BOX = {'left': int(800/RATIO), 'top': int(200/RATIO), 'width': int(300/RATIO), 'height': int(60/RATIO)}
CLIENT_GGNEXT_BOX = {'left': int(920/RATIO), 'top': int(780/RATIO), 'width': int(100/RATIO), 'height': int(100/RATIO)}

# In-game
EOG_BOX = {'left': int(860/RATIO), 'top': int(600/RATIO), 'width': int(200/RATIO), 'height': int(80/RATIO)}
FIGHT_BOX = {'left': int(300/RATIO), 'top': int(0/RATIO), 'width': int(1620/RATIO), 'height': int(800/RATIO)}
START_BOX = {'left': int(1000/RATIO), 'top': int(300/RATIO), 'width': int(600/RATIO), 'height': int(400/RATIO)}
SHOP_BOX = {'left': int(350/RATIO), 'top': int(130/RATIO), 'width': int(730/RATIO), 'height': int(760/RATIO)}
SHOP_OPEN_BOX = {'left': int(350/RATIO), 'top': int(775/RATIO), 'width': int(90/RATIO), 'height': int(95/RATIO)}
SHOP_CONSUMABLE_BOX = {'left': int(375/RATIO), 'top': int(195/RATIO), 'width': int(45/RATIO), 'height': int(295/RATIO)}
SHOP_STARTER_BOX = {'left': int(505/RATIO), 'top': int(330/RATIO), 'width': int(275/RATIO), 'height': int(60/RATIO)}
SHOP_BOOTS_BOX = {'left': int(375/RATIO), 'top': int(530/RATIO), 'width': int(45/RATIO), 'height': int(215/RATIO)}
SHOP_BASIC_BOX = {'left': int(500/RATIO), 'top': int(440/RATIO), 'width': int(500/RATIO), 'height': int(70/RATIO)}
SHOP_EPIC_BOX = {'left': int(500/RATIO), 'top': int(560/RATIO), 'width': int(500/RATIO), 'height': int(145/RATIO)}
SHOP_LEGENDARY_BOX = {'left': int(500/RATIO), 'top': int(750/RATIO), 'width': int(555/RATIO), 'height': int(70/RATIO)}
GOLD_BOX = {'left': int(1200/RATIO), 'top': int(1045/RATIO), 'width': int(90/RATIO), 'height': int(22/RATIO)}
INVENTORY_BOX = {'left': int(1130/RATIO), 'top': int(940/RATIO), 'width': int(190/RATIO), 'height': int(100/RATIO)}
MINIMAP_BOX = {'left': int(1640/RATIO), 'top': int(800/RATIO), 'width': int(280/RATIO), 'height': int(280/RATIO)}
MINIMAP_CORNER_BOX = {'left': int(1630/RATIO), 'top': int(790/RATIO), 'width': int(60/RATIO), 'height': int(60/RATIO)}
PLAYER_BOX = {'left': int(660/RATIO), 'top': int(200/RATIO), 'width': int(600/RATIO), 'height': int(400/RATIO)}

ILLAOI_ITEMS = [{'name': 'doranblade', 'price': 450, 'bought': False, 'box': SHOP_STARTER_BOX, 'pos': (int(695/RATIO),int(350/RATIO))},
                {'name': 'healthpotion', 'price': 50, 'bought': False, 'box': SHOP_CONSUMABLE_BOX, 'pos': (int(400/RATIO),int(215/RATIO))},
                {'name': 'ward', 'price': 0, 'bought': False, 'box': SHOP_CONSUMABLE_BOX, 'pos': (int(400/RATIO),int(290/RATIO))},
                {'name': 'longsword', 'price': 350, 'bought': False, 'box': SHOP_BASIC_BOX, 'pos': (int(640/RATIO),int(465/RATIO))},
                {'name': 'rubycrystal', 'price': 400, 'bought': False, 'box': SHOP_BASIC_BOX, 'pos': (int(700/RATIO),int(465/RATIO))},
                {'name': 'phage', 'price': 350, 'bought': False, 'box': SHOP_EPIC_BOX, 'pos': (int(1030/RATIO),int(585/RATIO))},
                {'name': 'sheen', 'price': 700, 'bought': False, 'box': SHOP_EPIC_BOX, 'pos': (int(530/RATIO),int(585/RATIO))},
                {'name': 'rubycrystal', 'price': 400, 'bought': False, 'box': SHOP_BASIC_BOX, 'pos': (int(700/RATIO),int(465/RATIO))},
                {'name': 'kindledgem', 'price': 400, 'bought': False, 'box': SHOP_EPIC_BOX, 'pos': (int(695/RATIO),int(585/RATIO))},
                {'name': 'divine', 'price': 700, 'bought': False, 'box': SHOP_BOX, 'pos': (int(615/RATIO),int(775/RATIO))},
                {'name': 'boots', 'price': 300, 'bought': False, 'box': SHOP_BOOTS_BOX, 'pos': (int(400/RATIO),int(555/RATIO))},
                {'name': 'clotharmor', 'price': 300, 'bought': False, 'box': SHOP_BASIC_BOX, 'pos': (int(530/RATIO),int(465/RATIO))},
                {'name': 'platedboots', 'price': 500, 'bought': False, 'box': SHOP_BOOTS_BOX, 'pos': (int(400/RATIO),int(700/RATIO))},
                {'name': 'longsword', 'price': 350, 'bought': False, 'box': SHOP_BASIC_BOX, 'pos': (int(640/RATIO),int(465/RATIO))},
                {'name': 'rubycrystal', 'price': 400, 'bought': False, 'box': SHOP_BASIC_BOX, 'pos': (int(700/RATIO),int(465/RATIO))},
                {'name': 'phage', 'price': 350, 'bought': False, 'box': SHOP_EPIC_BOX, 'pos': (int(1030/RATIO),int(585/RATIO))},
                {'name': 'pickaxe', 'price': 875, 'bought': False, 'box': SHOP_BASIC_BOX, 'pos': (int(865/RATIO),int(465/RATIO))},
                {'name': 'rubycrystal', 'price': 400, 'bought': False, 'box': SHOP_BASIC_BOX, 'pos': (int(700/RATIO),int(465/RATIO))},
                {'name': 'sterak', 'price': 725, 'bought': False, 'box': SHOP_LEGENDARY_BOX, 'pos': (int(925/RATIO),int(775/RATIO))},
                {'name': 'pickaxe', 'price': 875, 'bought': False, 'box': SHOP_BASIC_BOX, 'pos': (int(865/RATIO),int(465/RATIO))},
                {'name': 'tiamat', 'price': 325, 'bought': False, 'box': SHOP_EPIC_BOX, 'pos': (int(640/RATIO),int(655/RATIO))},
                {'name': 'longsword', 'price': 350, 'bought': False, 'box': SHOP_BASIC_BOX, 'pos': (int(640/RATIO),int(465/RATIO))},
                {'name': 'vampscepter', 'price': 550, 'bought': False, 'box': SHOP_EPIC_BOX, 'pos': (int(810/RATIO),int(585/RATIO))},
                {'name': 'ravenous', 'price': 1200, 'bought': False, 'box': SHOP_LEGENDARY_BOX, 'pos': (int(1035/RATIO),int(775/RATIO))},
                {'name': 'hammer', 'price': 1100, 'bought': False, 'box': SHOP_EPIC_BOX, 'pos': (int(585/RATIO),int(655/RATIO))},
                {'name': 'deathdance', 'price': 200, 'bought': False, 'box': SHOP_LEGENDARY_BOX, 'pos': (int(865/RATIO),int(775/RATIO))}]

AHRI_ITEMS = [  {'name': 'doranring', 'price': 400, 'bought': False, 'box': SHOP_STARTER_BOX, 'pos': (int(695/RATIO),int(350/RATIO))},
                {'name': 'healthpotion', 'price': 50, 'bought': False, 'box': SHOP_CONSUMABLE_BOX, 'pos': (int(400/RATIO),int(215/RATIO))},
                {'name': 'healthpotion', 'price': 50, 'bought': False, 'box': SHOP_CONSUMABLE_BOX, 'pos': (int(400/RATIO),int(215/RATIO))},
                {'name': 'ward', 'price': 0, 'bought': False, 'box': SHOP_CONSUMABLE_BOX, 'pos': (int(400/RATIO),int(290/RATIO))},
                {'name': 'amplifyingtome', 'price': 435, 'bought': False, 'box': SHOP_BASIC_BOX, 'pos': (int(755/RATIO),int(465/RATIO))},
                {'name': 'amplifyingtome', 'price': 435, 'bought': False, 'box': SHOP_BASIC_BOX, 'pos': (int(755/RATIO),int(465/RATIO))},
                {'name': 'lostchapter', 'price': 430, 'bought': False, 'box': SHOP_EPIC_BOX, 'pos': (int(530/RATIO),int(660/RATIO))},
                {'name': 'blastingwand', 'price': 850, 'bought': False, 'box': SHOP_BASIC_BOX, 'pos': (int(925/RATIO),int(465/RATIO))},
                {'name': 'luden', 'price': 1250, 'bought': False, 'box': SHOP_BOX, 'pos': (int(550/RATIO),int(400/RATIO))},
                {'name': 'boots', 'price': 300, 'bought': False, 'box': SHOP_BOOTS_BOX, 'pos': (int(400/RATIO),int(550/RATIO))},
                {'name': 'sorcerershoes', 'price': 800, 'bought': False, 'box': SHOP_BOOTS_BOX, 'pos': (int(400/RATIO),int(630/RATIO))},
                {'name': 'amplifyingtome', 'price': 435, 'bought': False, 'box': SHOP_BASIC_BOX, 'pos': (int(755/RATIO),int(465/RATIO))},
                {'name': 'blastingwand', 'price': 850, 'bought': False, 'box': SHOP_BASIC_BOX, 'pos': (int(925/RATIO),int(465/RATIO))},
                {'name': 'akuma', 'price': 1715, 'bought': False, 'box': SHOP_BOX, 'pos': (int(550/RATIO),int(775/RATIO))},
                {'name': 'amplifyingtome', 'price': 435, 'bought': False, 'box': SHOP_BASIC_BOX, 'pos': (int(755/RATIO),int(465/RATIO))},
                {'name': 'armguard', 'price': 465, 'bought': False, 'box': SHOP_EPIC_BOX, 'pos': (int(811/RATIO),int(580/RATIO))},
                {'name': 'zhonya', 'price': 1600, 'bought': False, 'box': SHOP_LEGENDARY_BOX, 'pos': (int(700/RATIO),int(775/RATIO))},
                {'name': 'bansheeveil', 'price': 2500, 'bought': False, 'box': SHOP_LEGENDARY_BOX, 'pos': (int(755/RATIO),int(775/RATIO))}]


# Global variables

shop_list = ILLAOI_ITEMS
first_pick = 'ahri'
second_pick = 'illaoi'
current_screen = 'unknown'
last_screen = 'unknown'
game_state = 'start'
sct = mss()

## LOGGING

# TODO: Needs a function to create the log files folder if non existing

# Logfile constant
LOGFILE = "logs/log-"+str(time.time())+".txt"

# Timestamp for log files
def log_timestamp():
    timestamp = "["+time.strftime('%H:%M:%S')+"]"
    return timestamp


## MOUSE AND KEYBOARD

# Move the mouse to coordinates
def move_mouse(x, y):
    try:
        win32api.SetCursorPos((x,y))
    except:
        print(f"{log_timestamp()} Couldn't lock mouse, 10s sleep...", file=open(LOGFILE, 'a'))
        time.sleep(10)

# Left click
def left_click(x, y):
    move_mouse(x, y)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(0.1)

# Right click
def right_click(x, y):
    move_mouse(x, y)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
    time.sleep(0.1)

# Write chars one by one
def keyboard_write(message):
    for letter in message:
        if letter.isupper():
            pydirectinput.keyDown('shift')
            pydirectinput.press(letter.lower())
            pydirectinput.keyUp('shift')
        else:
            pydirectinput.press(letter)

# Global hotkey class to quit the script ('k')
class Keystroke_Watcher(object):
    def __init__(self):
        self.hm = HookManager()
        self.hm.KeyDown = self.on_keyboard_event
        self.hm.HookKeyboard()

    def on_keyboard_event(self, event):
        try:
            if event.KeyID  == 75: #k
                self.stop_script()
        finally:
            return True

    def stop_script(self):
        print(f"{log_timestamp()} Exiting script...", file=open(LOGFILE, 'a'))
        os.system("taskkill /IM python.exe /f") # lol bruteforce

    def shutdown(self):
        win32gui.PostQuitMessage(0)
        self.hm.UnhookKeyboard()

# Object listening to global hotkey
def listen_k():
    watcher = Keystroke_Watcher()
    win32gui.PumpMessages()


## VISION

# Screenshots
def capture_window(bounding_box):
    sct_img = sct.grab(bounding_box)
    width = bounding_box['width']
    height = bounding_box['height']
    sct_img_resized = cv2.resize(np.array(sct_img),(width,height))
    del sct_img
    gc.collect()
    return sct_img_resized

# Lookup and return x, y coordinates
def lookup(bounding_box, template):
    sct_img = capture_window(bounding_box)
    x, y, *_ = template_match(sct_img, template)
    del sct_img
    gc.collect()
    return (x, y)

# Lookup specific to the multithread loop inside farm_lane
def lookup_thread(bounding_box, template):
    sct_img = capture_window(bounding_box)
    x, y, name, loc, width, height = template_match(sct_img, template)
    return name, loc, width, height, sct_img, bounding_box['left'], bounding_box['top']

# Infinite loop to look for a pattern until found
def look_for(bounding_box, template, once=False):
    while True:
        x, y = lookup(bounding_box, template)
        if x != 0 and y != 0:
            break
        if once:
            break
    return int(x+bounding_box['left']), int(y+bounding_box['top'])

# Matching template to the screenshot taken
def template_match(img_bgr, template_img):
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template_img, 0)
    name = template_img.split('/')[-1].split('.')[0]
    width = int(template.shape[1]/RATIO)
    height = int(template.shape[0]/RATIO)
    template = cv2.resize(template, (width,height))
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.89
    if name == 'minion': threshold = 0.98
    if 'tower' in name: threshold = 0.84
    if 'shop' in template_img: threshold = 0.94
    if 'inventory' in template_img: threshold = 0.84
    if name == 'start' or name == 'ward': threshold = 0.80
    loc = np.where(res > threshold)
    x = 0
    y = 0
    for pt in zip(*loc[::-1]):
        x += pt[0]
        y += pt[1]
        break
    if x != 0 and y != 0:
        x += width * RATIO / 2
        y += height * RATIO / 2

    del img_bgr
    del img_gray
    del template
    del res
    gc.collect()
    
    return int(x), int(y), name, loc, width, height

# Pixel color on a match to understand if ally (blue), enemy (red) or self (yellow)
def mark_the_spot(sct_img, pt, width, height, name):
    x = 0
    y = 0
    side = None
    if pt[0] != 0 and pt[1] != 0:
        x += int((width * RATIO / 2) + pt[0])
        y += int((height * RATIO / 2) + pt[1])
        color = tuple(int(x) for x in sct_img[y][x])
        if color[0] > 120 and color[2] < 120: side = "ally"
        elif color[2] > 120 and color[0] < 120: side = "enemy"
        else: side = "neutral"
        if name == 'low':
            offset = 0
            yellow_pixels = []
            while offset < int(25/RATIO):
                color = tuple(int(x) for x in sct_img[y][pt[0]-offset])
                if color[0] < 100 and color[1] > 150 and color[2] > 150:
                    print(f"{log_timestamp()} Low life pixel color match {color} at position ({y},{pt[0]-offset}) and offset {offset}...", file=open(LOGFILE, 'a'))
                    yellow_pixels.append(color)
                offset += 1
            if len(yellow_pixels) == 0:
                x = 0
                y = 0

    del sct_img
    gc.collect()

    return x, y, side

# Watch the screen and update the current_screen global variable with the latest perceived screen
def screen_watcher():
    global current_screen
    global last_screen

    while True:
        print(f"{log_timestamp()} Current screen is: {current_screen}, last screen is {last_screen}") #, file=open(LOGFILE, 'a'))
        if current_screen != 'unknown': last_screen = current_screen
        if lookup(CLIENT_LOGIN_BOX, 'patterns/client/login.png') != (0,0):
            current_screen = 'login'
        elif lookup(CLIENT_PLAY_BOX, 'patterns/client/play.png') != (0,0):
            current_screen = 'play'
        elif lookup(CLIENT_MATCHMAKING_BOX, 'patterns/client/matchmaking.png') != (0,0):
            current_screen = 'matchmaking'
        elif lookup(MINIMAP_CORNER_BOX, 'patterns/minimap/corner.png') != (0,0):
            current_screen = 'ingame'
        elif lookup(EOG_BOX, 'patterns/client/endofgame.png') != (0,0):
            current_screen = 'endofgame'
        elif lookup(CLIENT_GGSCREEN_BOX, 'patterns/client/ggscreen.png') != (0,0):
            current_screen = 'postmatch'
        else:
            current_screen = 'unknown'


## CLIENT MENU

# Login sequence
def login():
    left_click(x=int(400/RATIO), y=int(420/RATIO))
    counter = 1
    while True:
        if counter == 1:
            print(f"{log_timestamp()} Typing login...", file=open(LOGFILE, 'a'))
            keyboard_write(account_league.login)
        elif counter == 2:
            print(f"{log_timestamp()} Typing password...", file=open(LOGFILE, 'a'))
            keyboard_write(account_league.password)
        elif counter == 7:
            print(f"{log_timestamp()} Logging in...", file=open(LOGFILE, 'a'))
            pydirectinput.press('enter')
            time.sleep(5)
        elif counter == 8:
            print(f"{log_timestamp()} Starting game", file=open(LOGFILE, 'a'))
            pydirectinput.press('enter')
            break
        pydirectinput.press('tab')
        counter += 1

# Click sequence for menus
def screen_sequence(path, steps):
    for step in steps:
        print(f"{log_timestamp()} Next click is {step}", file=open(LOGFILE, 'a'))
        left_click(*look_for(CLIENT_BOX, path+step+'.png'))
        time.sleep(0.1)
        left_click(int(1070/RATIO),int(710/RATIO)) # Accept key fragment reward
        time.sleep(0.1)

# Click the menus to go to the correct matchmaking
def play(ai=True):
    if ai: screen_sequence(path='patterns/client/', steps=['play', 'ai', 'beginner', 'confirm'])
    else: screen_sequence(path='patterns/client/', steps=['play', 'training', 'practice', 'confirm', 'gamestart'])

# Queue for matchmaking and pick a champ
def matchup():
    global shop_list
    global game_state

    while True:

        if current_screen == 'matchmaking':
            left_click(*look_for(CLIENT_BOX, 'patterns/client/matchmaking.png'))

        if lookup(CLIENT_BOX, 'patterns/client/accept.png') != (0,0):
            left_click(int(955/RATIO), int(750/RATIO))

        elif lookup(CLIENT_BOX, 'patterns/client/pickerror.png') != (0,0):
            left_click(int(960/RATIO), int(550/RATIO))

        elif lookup(CLIENT_BOX, 'patterns/client/lock.png') != (0,0):
            print(f"{log_timestamp()} Sequence Champselect...", file=open(LOGFILE, 'a'))
            x, y = look_for(CLIENT_BOX, 'patterns/champselect/' + first_pick + '.png', once=True)
            if (x, y) != (0, 0): left_click(x, y)
            time.sleep(0.1)
            x, y = look_for(CLIENT_BOX, 'patterns/client/lock.png', once=True)
            if (x, y) != (0, 0): left_click(x, y)
            time.sleep(0.1)
            x, y = look_for(CLIENT_BOX, 'patterns/champselect/' + second_pick +'.png', once=True)
            if (x, y) != (0, 0): left_click(x, y)
            time.sleep(0.1)

        elif lookup(CLIENT_BOX, 'patterns/champselect/illaoipicked.png') != (0,0):
            print(f"{log_timestamp()} Locked Illaoi...", file=open(LOGFILE, 'a'))
            shop_list = ILLAOI_ITEMS

        elif lookup(CLIENT_BOX, 'patterns/champselect/ahripicked.png') != (0,0):
            print(f"{log_timestamp()} Locked Ahri...", file=open(LOGFILE, 'a'))
            shop_list = AHRI_ITEMS

        elif last_screen == 'ingame':
            print(f"{log_timestamp()} Game has started...", file=open(LOGFILE, 'a'))
            game_state = 'start'
            break

# Postmatch and rematch
def postmatch():
    global shop_list
    global game_state

    for item in shop_list:
        item['bought'] = False
    
    game_state = 'stop'

    time.sleep(5)

    while True:
        if lookup(CLIENT_GGNEXT_BOX, 'patterns/client/ggnext.png') != (0,0):
            print(f"{log_timestamp()} GG someone...", file=open(LOGFILE, 'a'))
            left_click(int(590/RATIO),int(550/RATIO))
        elif lookup(CLIENT_BOX, 'patterns/client/ok.png') != (0,0):
            print(f"{log_timestamp()} Found a post end game OK button to click...", file=open(LOGFILE, 'a'))
            pydirectinput.press('space')
        elif lookup(CLIENT_BOX, 'patterns/client/rematch.png') != (0,0):
            print(f"{log_timestamp()} Found the rematch button to click, exiting loop...", file=open(LOGFILE, 'a'))
            left_click(int(765/RATIO),int(865/RATIO))
            left_click(int(765/RATIO),int(845/RATIO))
            break
        else: # Lazy method to pick a champ reward
            print(f"{log_timestamp()} Just clicking at 1385, 570...", file=open(LOGFILE, 'a'))
            left_click(int(1385/RATIO),int(570/RATIO))
        time.sleep(1)

## GAMEPLAY

# Run on game start to level 3rd spell and to start shopping only after 15sc
def game_start():
    time.sleep(10)
    print(f"{log_timestamp()} Level up E spell", file=open(LOGFILE, 'a'))
    pydirectinput.keyDown('ctrl')
    pydirectinput.press('e')
    pydirectinput.keyUp('ctrl')
    time.sleep(5)
    if last_screen == 'ingame':
        buy_from_shop(shop_list)

# OCR to read the gold
def check_number(box):
    conf = r'--oem 3 --psm 6 outputbase digits'
    sct_img = capture_window(GOLD_BOX)
    sct_img = cv2.cvtColor(sct_img, cv2.COLOR_BGR2GRAY)
    sct_img = 0 - sct_img
    ksize = (3,3)
    sct_img = cv2.blur(sct_img, ksize)
    sct_img[sct_img < 100] = 0
    sct_img[sct_img > 200] = 255
    pil_img = Image.fromarray(cv2.cvtColor(sct_img, cv2.COLOR_BGR2RGB))
    text = pytesseract.image_to_string(pil_img, config=conf)
    try:
        number = 0
        number += int(text)
    except:
        number = 0
    return number

# Loop to buy a list of items from shop
def buy_from_shop(items):
    time.sleep(2)
    pydirectinput.press('p')
    for item in items:
        if item['bought'] == True:
            continue
        elif item['bought'] == False and check_number(GOLD_BOX) >= item['price']:
            buy_item(item)
        else:
            print(f"{log_timestamp()} Not enough gold for {item['name']}", file=open(LOGFILE, 'a'))
            break
    pydirectinput.press('p')
    if last_screen == 'ingame':
        go_toplane()

# Buy one item from shop
def buy_item(item):
    while True:
        if lookup(SHOP_OPEN_BOX, 'patterns/shop/open.png') == (0,0):
            print(f"{log_timestamp()} Opening shop..", file=open(LOGFILE, 'a'))
            pydirectinput.press('p')
        left_click(int(755/RATIO),int(155/RATIO))
        print(f"{log_timestamp()} Buying {item['name']}", file=open(LOGFILE, 'a'))
        if item['name'] in ['akuma', 'luden', 'divine']:
            left_click(int(545/RATIO),int(155/RATIO))
            time.sleep(0.5)
            right_click(*item['pos'])
            time.sleep(0.5)
        else:
            right_click(*item['pos'])
        left_click(int(755/RATIO),int(155/RATIO))
        if last_screen != 'ingame':
            break
        elif lookup(INVENTORY_BOX, 'patterns/inventory/'+item['name']+'.png') != (0,0):
            print(f"{log_timestamp()} Bought {item['name']}", file=open(LOGFILE, 'a'))
            item['bought'] = True
            break
        elif lookup(INVENTORY_BOX, 'patterns/inventory/empty.png') == (0,0):
            print(f"{log_timestamp()} Inventory full", file=open(LOGFILE, 'a'))
            break
        elif item['price'] > check_number(GOLD_BOX):
            print(f"{log_timestamp()} Insufficient gold for {item['price']}", file=open(LOGFILE, 'a'))
            break
        else:
            print(f"{log_timestamp()} Retrying to buy {item['name']}", file=open(LOGFILE, 'a'))

# Go back to lane, check if camera lock is on
def go_toplane():
    pydirectinput.keyDown('shift')
    right_click(int(1675/RATIO), int(890/RATIO))
    pydirectinput.keyUp('shift')
    print(f"{log_timestamp()} Going toplane...", file=open(LOGFILE, 'a'))
    print(f"{log_timestamp()} Sleep 25sc while walking...", file=open(LOGFILE, 'a'))
    time.sleep(15)
    if lookup(PLAYER_BOX, 'patterns/unit/player.png') == (0,0) and last_screen == 'ingame':
        print(f"{log_timestamp()} Can't see player, lock camera", file=open(LOGFILE, 'a'))
        pydirectinput.press('y')
    time.sleep(10)
    if last_screen == 'ingame':
        farm_lane()

# Level up abilities at the beginning of each farm_lane cycle
def level_up_abilities():
    pydirectinput.keyUp('shift')
    pydirectinput.keyDown('ctrl')
    pydirectinput.press('r')
    time.sleep(0.1)
    pydirectinput.press('w')
    time.sleep(0.1)
    pydirectinput.press('q')
    time.sleep(0.1)
    pydirectinput.press('e')
    pydirectinput.keyUp('ctrl')
    pydirectinput.keyUp('ctrl')

# Go back to base and shop
def back_and_recall():
    pydirectinput.keyUp('shift')
    right_click(int(1665/RATIO), int(1060/RATIO))
    pydirectinput.press('f')
    pydirectinput.press('g')
    pydirectinput.press('s')
    time.sleep(10) 
    pydirectinput.press('b')
    time.sleep(10)
    buy_from_shop(shop_list)

# Retreat
def fall_back(x=int(1680/RATIO), y=int(890/RATIO), timer=0):
    pydirectinput.keyUp('shift')
    pydirectinput.press('s')
    right_click(x, y)
    time.sleep(timer)

# Attack
def attack_position(x, y, q=False, w=True, e=False, r=False, target_champion=False, spelltarget=(0,0)):
    pydirectinput.keyDown('shift')
    if target_champion: pydirectinput.keyDown('c')
    right_click(x, y)
    if target_champion: pydirectinput.keyUp('c')
    pydirectinput.keyUp('shift')
    if spelltarget == (0,0): spelltarget = (x, y)
    left_click(spelltarget[0], spelltarget[1])
    if w: pydirectinput.press('w')
    if q: pydirectinput.press('q')
    if e: pydirectinput.press('e')
    if r: pydirectinput.press('r')

# Needed to calculate the average position of a group of units
def average_tuple_list(tuple_list):
    length = len(tuple_list)
    first = sum(v[0] for v in tuple_list)
    second = sum(v[1] for v in tuple_list)
    average_tuple = (int(first/length), int(second/length))
    print(f"{log_timestamp()} average_tuple: {average_tuple}", file=open(LOGFILE, 'a'))
    return average_tuple

# What to do when game ends
def end_of_game():
    print(f'{log_timestamp()} End of game button', file=open(LOGFILE, 'a'))
    time.sleep(1)
    left_click(int(960/RATIO), int(640/RATIO))

# Main loop to look for patterns and decide how to fight
def farm_lane():

    patterns = [{'box': PLAYER_BOX, 'pattern': 'patterns/unit/low.png'},
                {'box': START_BOX, 'pattern': 'patterns/shop/start.png'},
                {'box': FIGHT_BOX, 'pattern': 'patterns/unit/minion.png'},
                {'box': FIGHT_BOX, 'pattern': 'patterns/unit/champion.png'},
                {'box': FIGHT_BOX, 'pattern': 'patterns/unit/tower.png'},
                {'box': FIGHT_BOX, 'pattern': 'patterns/unit/tower2.png'}]

    loop_time = time.time()

    while True:
        
        low_life = False
        start_point = False
        nb_enemy_minion = 0
        pos_enemy_minion = []
        pos_closest_enemy_minion = (int(960/RATIO),int(540/RATIO))
        nb_enemy_champion = 0
        pos_enemy_champion = (0, 0)
        nb_enemy_tower = 0
        nb_ally_tower = 0
        nb_ally_minion = 0
        pos_ally_minion = []
        pos_safer_ally_minion = (int(960/RATIO),int(540/RATIO))
        pos_riskier_ally_minion = (int(960/RATIO),int(540/RATIO))
        pos_safe_player = (int(960/RATIO),int(540/RATIO))
        pos_median_enemy_minion = (int(960/RATIO),int(540/RATIO))

        level_up_abilities()

        # Start pattern matching threads
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = [executor.submit(lookup_thread, *(pattern['box'], pattern['pattern'])) for pattern in patterns]
            for f in concurrent.futures.as_completed(results):
                name, loc, width, height, sct_img, left, top = f.result()

                for pt in zip(*loc[::-1]):
                    x, y, side = mark_the_spot(sct_img, pt, width, height, name)

                    if (x, y) != (0, 0):
                        x = x + left
                        y = y + top
                        pass
                    else:
                        continue

                    if name == 'start': start_point = True
                    if name == 'low': low_life = True
                    if name == 'minion' and side == 'enemy': 
                        nb_enemy_minion += 1
                        pos_enemy_minion.append((x, y))
                    if name == 'champion' and side == 'enemy':
                        nb_enemy_champion += 1
                        pos_enemy_champion = (x, y)
                    if 'tower' in name and side == 'enemy':
                        nb_enemy_tower += 1
                    if 'tower' in name and side == 'ally':
                        nb_ally_tower += 1
                    if name == 'minion' and side == 'ally': 
                        nb_ally_minion += 1
                        pos_ally_minion.append((x, y))

                del sct_img
                del loc
                gc.collect()

        # Calculating positions
        if nb_ally_minion > 0:
            pos_safer_ally_minion = min(pos_ally_minion,key=lambda item:item[0])
            print(f"{log_timestamp()} pos_safer_ally_minion: {pos_safer_ally_minion}", file=open(LOGFILE, 'a'))
            # pos_riskier_ally_minion = max(pos_ally_minion,key=lambda item:item[0])
            risky_minions = []
            for pos_one_ally in pos_ally_minion:
                pos_x = int((pos_one_ally[0] / int(1920/RATIO))*100)
                pos_y = 100 - int((pos_one_ally[1] / int(1080/RATIO))*100)
                risky_minions.append(int((pos_x + pos_y) / 2))
            # max(enumerate(a), key=lambda x: x[1])[0]
            pos_riskier_ally_minion = pos_ally_minion[risky_minions.index(max(risky_minions))]
            print(f"{log_timestamp()} pos_riskier_ally_minion: {pos_riskier_ally_minion}", file=open(LOGFILE, 'a'))
            pos_safe_player = (max(pos_safer_ally_minion[0]-int(50/RATIO), int(0/RATIO)), min(pos_safer_ally_minion[1]+int(50/RATIO), int(1080/RATIO)))
            print(f"{log_timestamp()} pos_safe_player: {pos_safe_player}", file=open(LOGFILE, 'a'))
        if nb_enemy_minion > 0:
            pos_closest_enemy_minion = min(pos_enemy_minion,key=lambda item:item[0])
            pos_median_enemy_minion = average_tuple_list(pos_enemy_minion)
            print(f"{log_timestamp()} pos_median_enemy_minion: {pos_median_enemy_minion} and type: {type(pos_median_enemy_minion)}", file=open(LOGFILE, 'a'))

        # Logging
        print(f"{log_timestamp()} low_life: {low_life} | start_point: {start_point}", file=open(LOGFILE, 'a'))
        print(f"{log_timestamp()} nb_enemy_minion: {nb_enemy_minion} | pos_enemy_minion: {pos_enemy_minion}", file=open(LOGFILE, 'a'))
        print(f"{log_timestamp()} nb_enemy_champion: {nb_enemy_champion} | pos_enemy_champion: {pos_enemy_champion}", file=open(LOGFILE, 'a'))
        print(f"{log_timestamp()} nb_enemy_tower: {nb_enemy_tower} | nb_ally_tower: {nb_ally_tower}", file=open(LOGFILE, 'a'))
        print(f"{log_timestamp()} nb_ally_minion: {nb_ally_minion} | pos_ally_minion: {pos_ally_minion}", file=open(LOGFILE, 'a'))

        # Priority conditions
        if current_screen == 'endofgame':
            end_of_game()
            break
        elif last_screen != 'ingame':
            break
        elif low_life:
            print(f'{log_timestamp()} low life', file=open(LOGFILE, 'a'))
            back_and_recall()
            break
        elif start_point:
            print(f'{log_timestamp()} back at the shop', file=open(LOGFILE, 'a'))
            buy_from_shop(shop_list)
            break

        # fight sequences
        if nb_enemy_minion > 0 or nb_enemy_champion > 0:

            # fall back if no allies or 2- minions + a tower or if tower + champion or too many enemies
            if nb_ally_minion == 0  or (nb_ally_minion <= 2 and nb_enemy_tower > 0) or (nb_enemy_tower > 0 and nb_enemy_champion > 0) or nb_enemy_champion > 3:
                print(f'{log_timestamp()} falling back', file=open(LOGFILE, 'a'))
                fall_back(timer=2)
                attack_position(int(960/RATIO), int(540/RATIO))

            # primarily attack champions
            elif nb_enemy_champion > 0:
                print(f'{log_timestamp()} attack enemy champion', file=open(LOGFILE, 'a'))
                if (nb_enemy_minion > nb_ally_minion and nb_ally_tower == 0):
                    fall_back(1)
                attack_position(*pos_enemy_champion, q=True, e=True, r=True, target_champion=True)

            # normal attack sequence
            else:
                print(f'{log_timestamp()} fight, back if lower numbers', file=open(LOGFILE, 'a'))
                if nb_enemy_minion > nb_ally_minion and nb_ally_tower == 0:
                    fall_back()
                attack_position(*pos_closest_enemy_minion, spelltarget=pos_median_enemy_minion, q=True)

        # if no enemies follow minions
        elif nb_ally_minion > 0 and (pos_riskier_ally_minion[0] > int(960/RATIO) or pos_riskier_ally_minion[1] < int(450/RATIO)):
            print(f'{log_timestamp()} follow ally minions', file=open(LOGFILE, 'a'))
            pydirectinput.keyDown('shift')
            right_click(*pos_riskier_ally_minion)
            pydirectinput.keyUp('shift')

        # no one around, might be lost go back to lane tower
        else:
            print(f"{log_timestamp()} I feel lost... walking to top tower...", file=open(LOGFILE, 'a'))
            fall_back()

        print(f'{log_timestamp()} FPS {round(1 /(time.time() - loop_time), 2)}\n', file=open(LOGFILE, 'a'))
        loop_time = time.time()


# Main program loop
def main():
    print(f"{log_timestamp()} Main script starting in 5 seconds...", file=open(LOGFILE, 'a'))
    time.sleep(5)
    global game_state

    while True:
        if current_screen == 'login': login()
        if current_screen == 'play': play()
        if current_screen == 'matchmaking': matchup()
        if current_screen == 'ingame' and game_state == 'start': 
            game_start()
            game_state = 'playing'
        if current_screen == 'postmatch': postmatch()


# Start the program and different threads
if __name__ == '__main__':
    threads = []
    threads.append(threading.Thread(target=listen_k))
    threads.append(threading.Thread(target=main))
    threads.append(threading.Thread(target=screen_watcher))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()