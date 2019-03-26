import pyautogui

#permet de récupérer le controle de la souris si on la bouge pendant le script
pyautogui.FAIL_SAFE = True
pyautogui.PAUSE = 1

#dimensions écran
height, width = pyautogui.size()

'''déplace la souris aux coordonnées indiquées en x temps (timeTravel) et clique'''
def moveMouseToAndClick(x, y , timeTravel):
    pyautogui.moveTo(x, y, timeTravel)
    pyautogui.click()


if __name__ == '__main__':
    #bouge la souris en 800, 400 en 2s
    moveMouseToAndClick(800, 400, 2)