import cv2 as cv
import logging
import numpy as np
import time

from PIL import ImageGrab
from prokeUtils import ProkeUtils

timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


class ScreenOperation:

    fight_img = cv.imread(ProkeUtils.resource_path('img/fight.png'), 0)
    selected_fight_img = cv.imread(ProkeUtils.resource_path('img/selected_fight.png'), 0)
    ok_img = cv.imread(ProkeUtils.resource_path('img/ok.png'), 0)

    # Take a full screen screenshot
    @staticmethod
    def get_screenshot():
        logging.debug('{}: in get_screen'.format(timestamp))
        screen = np.array(ImageGrab.grab())
        screen = cv.cvtColor(screen, cv.COLOR_RGB2GRAY)
        return screen

    # Take a screenshot given the coordinates
    @staticmethod
    def get_screenshot_area(x1, y1, x2, y2):
        screen_img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        screen_img = np.array(screen_img)
        screen_img = cv.cvtColor(screen_img, cv.COLOR_RGB2GRAY)
        return screen_img

    @staticmethod
    def is_fighting():
        logging.debug('{}: in is_fighting'.format(timestamp))
        return ScreenOperation.compare_screenshot_to_template(ScreenOperation.fight_img, 0.90)

    @staticmethod
    def is_rare():
        logging.debug('{}: in is_rare'.format(timestamp))
        return ScreenOperation.compare_screenshot_to_template(ScreenOperation.ok_img, 0.60)

    @staticmethod
    def compare_screenshot_to_template(template, accuracy):
        logging.debug('{}: in compare_screen_shot_to_template'.format(timestamp))
        screenshot = ScreenOperation.get_screenshot()

        # for method in methods:
        result = cv.matchTemplate(screenshot, template, cv.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        # print(f"match_val {max_val} | accuracy {accuracy}")

        if max_val > accuracy:
            return True
        else:
            return False
