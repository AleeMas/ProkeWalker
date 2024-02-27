from inputHandler import InputHandler
from prokeUtils import ProkeUtils
from screenOperation import ScreenOperation

import logging
import pyautogui
import random
import time
timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


class PlayerMoves:

    def __init__(self):
        self.wait_fight_flag = False
        self.catch_flag = False

    def walk(self):

        if InputHandler.inputs["movement_type"] == "HORIZONTAL":
            logging.debug('{}:walking horizontal'.format(timestamp))
            pyautogui.keyDown('d')
            time.sleep(0.5 + random.random() * 0.7)
            pyautogui.keyDown('a')

            pyautogui.keyUp('d')
            time.sleep(0.5 + random.random() * 0.7)
            pyautogui.keyUp('a')

        elif InputHandler.inputs["movement_type"] == "VERTICAL":
            logging.debug('{}:walking vertical'.format(timestamp))
            pyautogui.keyDown('w')
            time.sleep(0.5 + random.random() * 0.7)
            pyautogui.keyDown('s')

            pyautogui.keyUp('w')
            time.sleep(0.5 + random.random() * 0.7)
            pyautogui.keyUp('s')

        elif InputHandler.inputs["movement_type"] == "SQUARE":
            logging.debug('{}:walking square'.format(timestamp))
            pyautogui.press('a')
            time.sleep(random.random() * 0.2)
            pyautogui.press('w')
            time.sleep(random.random() * 0.2)
            pyautogui.press('d')
            time.sleep(random.random() * 0.2)
            pyautogui.press('s')

    def fight(self):
        # print('inizio ciclo fight')
        # print(f"condizione totale: {(not ScreenOperation.is_selected_fighting()) and ScreenOperation.is_fighting()}")
        # print(f"condizione not: {(not ScreenOperation.is_selected_fighting())}")
        # print(f"condizione screen is fighint: {ScreenOperation.is_fighting()}")
        logging.debug('{}: in fight'.format(timestamp))
        pyautogui.press('1')
        logging.debug('{}: 1 pressed'.format(timestamp))
        time.sleep(1.5)

    def make_random_move(self):
        logging.debug('{}: in make_random_move'.format(timestamp))
        move_set = set()
        move_pp_finished = True
        logging.debug('Chek available moves')
        for key, value in InputHandler.inputs["moves_selector"].items():
            logging.debug('{}: key:{} | Value{}'.format(timestamp, key, value))
            if value:
                logging.debug('Moves load')
                move_set.add(key)
                move_pp_finished = False

        logging.debug('{}: Moves available:{}'.format(timestamp, move_set))
        if move_pp_finished:
            pyautogui.press("7")
            ProkeUtils.send_notification(f" Ho finito le mosse <@{InputHandler.inputs['notify_configuration']['discord_id']}>")
            logging.debug('{}: finished moves'.format(timestamp))
            return False

        move = random.sample(move_set, 1)[0]
        logging.debug('{}: Move selected'.format(timestamp))

        if InputHandler.inputs["pp"]["enabled"]:
            logging.debug('{}: updating pp'.format(timestamp))
            self.pp_update(move)

        pyautogui.press(move)
        logging.debug('{}: did move {}'.format(timestamp, move))
        return True

    def escape(self, tries):
        logging.debug('{}: in escape '.format(timestamp))
        escaped = 0
        while ScreenOperation.is_fighting() and escaped < tries:
            logging.debug('{}: tries number: {} max: {} '.format(timestamp, tries, escaped))
            pyautogui.press('4')
            time.sleep(0.2 + random.random() * 0.4)
            pyautogui.press('4')
            time.sleep(0.2 + random.random() * 0.4)
            escaped = escaped + 1

        if escaped == tries:
            logging.debug('{}: fail to escape'.format(timestamp))
            ProkeUtils.send_message(f"I can't escape <@{InputHandler.inputs['notify_configuration']['discord_id']}>")
            return False

        return True

    def change_pokemon(self, arg):
        logging.debug('{}: in change pokemon '.format(timestamp))
        logging.debug('{}: selecting pokemon'.format(timestamp))
        # print(f"-\nSeleziono pokemon")
        pyautogui.press("2")
        time.sleep(2)
        # print(f"Metto pokemon {arg}")
        logging.debug('{}: pokemon:{} in fight'.format(timestamp,arg))
        pyautogui.press(arg)
        # print("Entro in wait_fight()")
        logging.debug('{}: '.format(timestamp))
        self.wait_fight()

    def make_move(self, arg):
        logging.debug('{}: in make_move'.format(timestamp))
        time.sleep(2)
        logging.debug('{}: pressing: {}'.format(timestamp, arg))
        pyautogui.press(arg)
        if (not self.pp_update(arg)) and InputHandler.inputs["pp"]["enabled"]:
            logging.debug('{}: pp enabled and i finished moves'.format(timestamp))
            ProkeUtils.send_message(f"Ho finito le mosse <@{InputHandler.inputs['notify_configuration']['discord_id']}>")
        self.wait_fight()

    def wait_fight(self):
        logging.debug('{}: in wait_fight'.format(timestamp))
        self.wait_fight_flag = True

        logging.debug('{}: flag wait:{}'.format(timestamp, self.wait_fight_flag))
        flag = not ScreenOperation.is_fighting()
        while flag and self.wait_fight_flag:
            logging.debug('{}: waiting'.format(timestamp, self.wait_fight_flag))
            flag = not ScreenOperation.is_fighting()
            time.sleep(1)

    def catch(self, args,pokemon):
        logging.debug('{}: in catch'.format(timestamp))
        catch_try = 0
        self.catch_flag = True
        logging.debug('{}: flag catch:{}'.format(timestamp,self.catch_flag))
        while catch_try < int(args[0]) and self.catch_flag:
            pyautogui.press("3")
            time.sleep(1.5)
            pyautogui.press(args[1])
            logging.debug('{}: waiting 20second'.format(timestamp))
            time.sleep(20)
            if not ScreenOperation.is_fighting():
                logging.info('{}: catch pokemon {}'.format(timestamp, pokemon))
                break
            logging.info('{}: failed catch {}'.format(timestamp, pokemon))
            catch_try = catch_try + 1

    def pp_update(self, move):
        logging.debug('{}: in pp_update'.format(timestamp))
        pp = InputHandler.inputs["pp"]["info"][move]
        if int(pp) > 1:
            InputHandler.inputs["pp"]["info"].update({move: f"{int(pp)-1}"})
            logging.debug('{}: move{} : pp{}'.format(timestamp, move, int(pp)-1))
            return True
        else:
            InputHandler.inputs["pp"]["info"].update({move: f"{int(pp)-1}"})
            logging.debug('{}: move{} : pp{}'.format(timestamp, move, int(pp) - 1))
            InputHandler.inputs["moves_selector"].update({move: False})
            logging.debug('{}: move {} removed'.format(timestamp, move))
            return False

    def stop(self):
        logging.debug('{}: in stop'.format(timestamp))
        self.wait_fight_flag = False
        logging.debug('{}: waiting fight flag set to false'.format(timestamp))
        self.catch_flag = False
        logging.debug('{}: catch fight flag set to false'.format(timestamp))

