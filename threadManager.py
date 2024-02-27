import logging
import threading
import time

from inputHandler import InputHandler
from player import Player
from prokeUtils import ProkeUtils

timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


class ThreadManager:
    player = Player()

    @staticmethod
    def thread_fight_and_find_1(pokemon_to_stop):
        logging.debug('{}: in thread_fight_and_find_1'.format(timestamp))
        logging.debug('{}: pokemon_to_fight: {} pokemon_to_stop: {}'.format(timestamp, set(), pokemon_to_stop))
        thread = threading.Thread(target=lambda: ThreadManager.player.play(set(), pokemon_to_stop))
        thread.start()

    @staticmethod
    def thread_fight_and_find_2():
        logging.debug('{}: in thread_fight_and_find_2'.format(timestamp))
        pokemon_to_fight = []

        for key,value in InputHandler.inputs["evs_to_train_selector"].items():
            if value:
                pokemon_to_fight.extend(ProkeUtils.load_config_evs_file(f"pokeKill-{key}.txt"))
        logging.debug('{}: pokemon_to_fight: {} pokemon_to_stop: {}'.format(timestamp, pokemon_to_fight, set()))
        thread = threading.Thread(target=lambda: ThreadManager.player.play(pokemon_to_fight, set()))
        thread.start()

    @staticmethod
    def thread_fight_and_find_3(pokemon_to_stop):
        logging.debug('{}: in thread_fight_and_find_3'.format(timestamp))
        pokemon_to_fight = []
        for key, value in InputHandler.inputs["evs_to_train_selector"].items():
            if value:
                pokemon_to_fight.extend(ProkeUtils.load_config_evs_file(f"pokeKill-{key}.txt"))
        logging.debug('{}: pokemon_to_fight: {} pokemon_to_stop: {}'.format(timestamp, pokemon_to_fight, pokemon_to_stop))
        thread = threading.Thread(target=lambda: ThreadManager.player.play(pokemon_to_fight, pokemon_to_stop))
        thread.start()

    @staticmethod
    def thread_cancel():
        logging.debug('{}: in thread_cancel'.format(timestamp))
        ThreadManager.player.stop()
        ThreadManager.player.player_moves.stop()
        ProkeUtils.to_play = False
        pass


