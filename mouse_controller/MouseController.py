import pyautogui

def move_cursor(screenW, screenH, clocX, clocY):
    clocX = max(0, min(screenW - 1, clocX))
    clocY = max(0, min(screenH - 1, clocY))
    pyautogui.moveTo(clocX, clocY)

def click_mouse():
    pyautogui.click()

def double_click():
    pyautogui.doubleClick()

def right_click():
    pyautogui.rightClick()

def mouse_press():
    pyautogui.mouseDown()

def mouse_release():
    pyautogui.mouseUp()
