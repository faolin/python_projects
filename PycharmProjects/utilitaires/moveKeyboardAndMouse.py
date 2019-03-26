import pyautogui
import random
from random import randint
import time
#permet de récupérer le controle de la souris si on la bouge pendant le script
pyautogui.FAIL_SAFE = True
pyautogui.PAUSE = 1

#dimensions écran
height, width = pyautogui.size()
#positions des icones des légendes dans l'écran de séléction
positionsLegende = [[800,400] , [600, 300]]

'''déplace la souris aux coordonnées indiquées en x temps (timeTravel) et clique'''
def moveMouseToAndClick(x, y , timeTravel):
    pyautogui.moveTo(x, y, timeTravel)
    pyautogui.click()


def boucleInfinie():
    for posLegend in positionsLegende:
        print(posLegend)
        #clique sur le bouton lancer la game
        moveMouseToAndClick(randint(800, 900), randint(400, 500), random.uniform(1, 2.5))
        #attends entre 5 et 10s que l'on trouve une game
        time.sleep(randint(5, 10))
        #clique sur la légende que l'on veut séléctionner
        moveMouseToAndClick(posLegend[0], posLegend[1], random.uniform(1, 2.5))
        #on attends entre 15 et 20s le temps que la game se lance et que l'on puisse sauter
        time.sleep(randint(15, 20))
        #on appuie sur la touche ee que notre légende saute du ship si il est le leader de saut
        pyautogui.press('e')
        #on attends entre 4 et 6 min
        time.sleep(randint(240, 360))
        #on appuie sur la touche échap
        pyautogui.press('esc')
        #on clique sur le bouton retour au salon
        moveMouseToAndClick(randint(100, 200), randint(400, 500), random.uniform(1, 2.5))
    #quand on a finit de jouer toutes les légendes de la liste l'on recommence a 0
    boucleInfinie()

if __name__ == '__main__':
    boucleInfinie()







