from inputHandler import InputHandler

import constant
import logging
import os
import pygame
import requests
import sys
import threading
import time

timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


class ProkeUtils:
    to_play = False
    templates_folder = "./templates"

    @staticmethod
    def send_message(txt):
        logging.debug('{}: in send_message'.format(timestamp))
        payload = {'content': txt}
        requests.post(constant.DISCORD_WEB_HOOK, json=payload)
        logging.debug('{}: discord message sent'.format(timestamp))

    @staticmethod
    def thread_send_notification(txt):
        logging.debug('{}: in thread_send_notification'.format(timestamp))
        thread = threading.Thread(target=lambda: ProkeUtils.send_notification(txt))
        thread.start()

    @staticmethod
    def send_notification(txt):
        logging.debug('{}: in send_notification'.format(timestamp))
        if InputHandler.inputs["notify_configuration"]["discord_id"] != "":
            logging.debug('{}: discord notify enabled'.format(timestamp))
            ProkeUtils.send_message(txt)

        if InputHandler.inputs["notify_configuration"]["jingle"]:
            logging.debug('{}: jingle enabled'.format(timestamp))
            pygame.init()
            logging.debug('{}:paying jingle'.format(timestamp))
            ProkeUtils.to_play = True

            pygame.mixer.music.load(ProkeUtils.resource_path("sounds/jingle.mp3"))

            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy() and ProkeUtils.to_play:
                pygame.time.Clock().tick(10)
            logging.debug('{}: stopped jingle'.format(timestamp))
            pygame.quit()

    @staticmethod
    def load_config_evs_file(filename):
        logging.debug('{}: in load_config_evs_file'.format(timestamp))
        pokemon_to_find = []

        with open(ProkeUtils.resource_path(filename), 'r') as pokeATK:
            for line in pokeATK.readlines():
                if line == "\n":
                    continue
                content = line.lower().strip()
                if content[-1] == ",":
                    content = str(content[:-1])
                pokemon_to_find.extend(content.lower().split(","))

        return pokemon_to_find

    @staticmethod
    def resource_path(relative_path):
        logging.debug('{}: in resource_path'.format(timestamp))
        try:
            base_path = sys._MEIPASS

        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    @staticmethod
    def save_template(filename):
        logging.debug('{}: in save_template'.format(timestamp))
        with open(f"./templates/{filename}", "w") as template:
            template.writelines(str(InputHandler.inputs))

    @staticmethod
    def load_template(filename):
        logging.debug('{}: in load_template'.format(timestamp))
        with open(f"./templates/{filename}", "r") as template:
            InputHandler.inputs = eval("".join(template.readlines()))

    @staticmethod
    def get_templates():
        logging.debug('{}: in get_template'.format(timestamp))
        if not os.path.exists(ProkeUtils.templates_folder):
            logging.debug('{}: making dir for template'.format(timestamp))
            os.makedirs(ProkeUtils.templates_folder)

        return os.listdir(ProkeUtils.templates_folder)

    @staticmethod
    def delete_template(filename):
        logging.debug('{}: in delete_template'.format(timestamp))
        os.remove(f"{ProkeUtils.templates_folder}/{filename}")