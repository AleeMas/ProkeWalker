from win32gui import GetWindowText, GetForegroundWindow, SetForegroundWindow, FindWindow

import logging
import pypokedex
import random
import time
import traceback

from playerMoves import PlayerMoves
from inputHandler import InputHandler
from memoryOperation import MemoryOperation
from screenOperation import ScreenOperation
from prokeUtils import ProkeUtils

timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


class Player:
    def __init__(self):
        self.finding_flag = False
        self.player_moves = PlayerMoves()

    def walk(self):
        logging.debug('{}: player is calling walk moves'.format(timestamp))
        self.player_moves.walk()

    def attack(self):
        logging.debug('{}: player is calling attack'.format(timestamp))
        while ScreenOperation.is_fighting():
            logging.debug('{}: player is calling fight moves'.format(timestamp))
            self.player_moves.fight()
            if not self.player_moves.make_random_move():

                self.escape(8)
                logging.debug('{}: finding flag set to false'.format(timestamp))
                self.finding_flag = False
                break

            time.sleep(1)

    def catch_routine(self, pokemon):
        logging.debug('{}: in catch_routine'.format(timestamp))
        catch_routine = InputHandler.inputs['catch']['routine']
        if pokemon == "abra":
            logging.debug('{}: pokemon is abra'.format(timestamp))
            catch_routine = ["catch(3,1)"]

        for command in catch_routine:

            if self.finding_flag:
                action = command[0:command.find("(")]
                args = command[command.find("(") + 1: command.find(")")].split(",")
                print(f"{action}, {args}")

                if action == "changePokemon":
                    self.player_moves.change_pokemon(args[0])

                elif action == "makeMove":
                    self.player_moves.fight()
                    self.player_moves.make_move(args[0])

                elif action == "catch":
                    self.player_moves.catch(args,pokemon)

                elif action == "run":
                    self.escape(8)

    def escape(self, tries):
        logging.debug('{}: player is calling escape moves'.format(timestamp))
        return self.player_moves.escape(tries)

    def play(self, pokemon_to_fight, pokemon_to_stop):
        logging.debug('{}: in play'.format(timestamp))
        self.finding_flag = True

        handle = FindWindow(0, "PROClient")
        SetForegroundWindow(handle)

        while self.finding_flag:
            if GetWindowText(GetForegroundWindow()) == "PROClient":
                logging.debug('{}: PROClient is selected'.format(timestamp))
                if ScreenOperation.is_fighting():
                    poke_id = MemoryOperation.get_pokemon_id()
                    try:
                        pokemon = pypokedex.get(dex=poke_id).name
                        logging.debug('{}: -------------------------'.format(timestamp))
                        logging.info('{}: meet pokemon: {}'.format(timestamp, pokemon))
                        if ScreenOperation.is_rare():
                            ProkeUtils.thread_send_notification(f"{pokemon.capitalize()} rare found <@{InputHandler.inputs['notify_configuration']['discord_id']}>")
                            self.finding_flag = False
                            break

                        if pokemon in pokemon_to_stop:
                            logging.info('{}: meet pokemon: {} and it is a pokemon to stop'.format(timestamp, pokemon))
                            ProkeUtils.thread_send_notification(f"{pokemon.capitalize()} found <@{InputHandler.inputs['notify_configuration']['discord_id']}>")
                            if InputHandler.inputs["catch"]["enabled"]:
                                logging.debug('{}: player is calling catch routine'.format(timestamp))
                                self.catch_routine(pokemon)
                                continue
                            break

                        if pokemon in pokemon_to_fight:
                            logging.debug('{}: meet pokemon attacking for evs'.format(timestamp))
                            # print(f"{pokemon} trovato, lo attacco per evs")
                            self.attack()
                        else:
                            logging.debug('{}: escape from battle'.format(timestamp))
                            if not self.escape(8):
                                break
                            time.sleep(0.2 + random.random() * 0.3)

                    except Exception as e:
                        logging.error('{}: error while playing {}, error: {}'.format(timestamp, e, traceback.format_exc()))
                        self.finding_flag = False
                        self.escape(8)
                        # print(str(e))
                        # traceback.print_exc()

                else:
                    while not ScreenOperation.is_fighting() and self.finding_flag:
                        if GetWindowText(GetForegroundWindow()) == "PROClient":
                            self.walk()
                        time.sleep(0.1)

            time.sleep(0.2 + random.random() * 0.3)

    def stop(self):
        logging.debug('{}: in stop'.format(timestamp))
        self.finding_flag = False
