import logging
import pyautogui
import time
import tkinter as tk

from inputHandler import InputHandler
from prokeUtils import ProkeUtils
from threadManager import ThreadManager
from tkinter import ttk

timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


class WindowHandler:

    def __init__(self, width, height, title):
        self.root = tk.Tk()
        self.width = width
        self.height = height
        self.title = title
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)

        self.pokemon_to_stop = tk.Entry()
        self.catch_routine_text = tk.Text()

        self.spinbox_move_1 = tk.Spinbox()
        self.spinbox_move_2 = tk.Spinbox()
        self.spinbox_move_3 = tk.Spinbox()
        self.spinbox_move_4 = tk.Spinbox()

        self.move_1_selector = tk.Checkbutton()
        self.move_2_selector = tk.Checkbutton()
        self.move_3_selector = tk.Checkbutton()
        self.move_4_selector = tk.Checkbutton()

        self.do_update_window = False

        self.create_window()
        self.update_window()

    def run(self):
        self.root.mainloop()

    def create_window(self):
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.title(self.title)

        self.create_widgets()

    def create_widgets(self):
        logging.debug('{}: in create_widgets'.format(timestamp))
        self.canvas.place(x=0, y=0)
        logging.debug('{}: create notify_configuration'.format(timestamp))
        self.create_notify_configuration_widgets()
        logging.debug('{}: create find_pokemon_widgets '.format(timestamp))
        self.create_find_pokemon_widgets()
        logging.debug('{}: create train_evs_widgets '.format(timestamp))
        self.create_train_evs_widgets()
        logging.debug('{}: create pp_widgets'.format(timestamp))
        self.create_pp_widgets()
        logging.debug('{}: create config_selector_widgets'.format(timestamp))
        self.create_config_selector_widgets()
        logging.debug('{}: create catch_routine_widgets'.format(timestamp))
        self.create_catch_routine_widgets()
        logging.debug('{}: create  template_widgets'.format(timestamp))
        self.create_template_widgets()

    def create_find_pokemon_widgets(self):

        self.canvas.create_rectangle(5, 25, 290, 85, outline="light grey")

        pokemon_to_stop_section_label = tk.Label(self.root, text="Find Pokemon", fg="Red", font=("Arial Bold", 13))
        pokemon_to_stop_section_label.place(x=90, y=10)

        pokemon_to_stop_label = tk.Label(self.root, text="Pokemon to find", fg="Red", font=("Arial Bold", 8))
        pokemon_to_stop_label.place(x=30, y=35)

        self.pokemon_to_stop = tk.Entry(self.root, width=20)
        self.pokemon_to_stop.place(x=10, y=56)

        pokemon_to_stop_button = tk.Button(self.root, text="Find Pokemon",
                                           command=lambda: (
                                               ThreadManager.thread_fight_and_find_1(self.pokemon_to_stop.get().lower()),
                                               InputHandler.inputs["notify_configuration"].update({"discord_id": f"{self.discord_id.get()}"}),
                                               self.update_window_handler(True),
                                               self.input_refresh(),
                                           ),
                                           width=10, height=1, padx=0, pady=1, font=("Arial", 7), relief=tk.GROOVE)
        pokemon_to_stop_button.place(x=140, y=55)

        pokemon_to_stop_cancel_button = tk.Button(self.root, text="Cancel",
                                                  command=lambda: (
                                                      ThreadManager.thread_cancel(),
                                                      self.update_window_handler(False),
                                                      self.input_refresh(),
                                                  ),
                                                  relief=tk.GROOVE, width=10, height=1, padx=0, pady=1, font=("Arial", 7))
        pokemon_to_stop_cancel_button.place(x=210, y=55)

    def create_train_evs_widgets(self):
        self.canvas.create_rectangle(5, 105, 290, 185, outline="light grey")

        evs_label = tk.Label(self.root, text="Farm EVS", fg="Red", font=("Arial Bold", 13))
        evs_label.place(x=100, y=90)

        evs_button = tk.Button(self.root, text="Start evs",
                               command=lambda: (
                                   ThreadManager.thread_fight_and_find_2(),
                                   InputHandler.inputs["notify_configuration"].update({"discord_id": f"{self.discord_id.get()}"}),
                                   self.update_window_handler(True),
                                   self.input_refresh(),
                                   self.update_window(),
                               ), width=10, height=1, padx=0, pady=1, font=("Arial", 7), relief=tk.GROOVE)
        evs_button.place(x=80, y=117)

        evs_cancel_button = tk.Button(self.root, text="Cancel",
                                      command=lambda: (
                                          ThreadManager.thread_cancel(),
                                          self.update_window_handler(False),
                                          self.input_refresh(),
                                          self.update_window(),
                                      ),
                                      width=10, height=1, padx=0, pady=1, font=("Arial", 7), relief=tk.GROOVE)
        evs_cancel_button.place(x=140, y=117)

        # UI evs and cath
        evs_stop_label = tk.Label(self.root, text="Catch while evsing", fg="Red", font=("Arial Bold", 8))
        evs_stop_label.place(x=17, y=140)

        self.pokemon_to_stop_while_evs = tk.Entry(self.root, width=20)
        self.pokemon_to_stop_while_evs.place(x=10, y=160)

        evs_stop_button = tk.Button(self.root, text="Evs & Catch",
                                    command=lambda: (
                                        ThreadManager.thread_fight_and_find_3(self.pokemon_to_stop_while_evs.get().lower()),
                                        InputHandler.inputs["notify_configuration"].update({"discord_id": f"{self.discord_id.get()}"}),
                                        self.update_window_handler(True),
                                        self.input_refresh(),
                                        self.update_window(),
                                    ),
                                    width=10, height=1, padx=0, pady=1, font=("Arial", 7), relief=tk.GROOVE)
        evs_stop_button.place(x=140, y=160)

        evs_stop_cancel_button = tk.Button(self.root, text="Cancel",
                                           command=lambda: (
                                               ThreadManager.thread_cancel(),
                                               self.update_window_handler(False),
                                               self.input_refresh(),
                                               self.update_window(),
                                           ),
                                           width=10, height=1, padx=0, pady=1, font=("Arial", 7), relief=tk.GROOVE)
        evs_stop_cancel_button.place(x=210, y=160)

    def create_config_selector_widgets(self):
        self.canvas.create_rectangle(5, 215, 290, 434, outline="light grey")

        # UI Config selector
        label_config = tk.Label(self.root, text="Config selector", width=12, height=1, padx=1, pady=1, font=("Arial", 13))
        label_config.place(x=85, y=200)

        # UI MOVE CONFIG SELECTOR
        label_move_config = tk.Label(self.root, text="Move to use", width=11, height=1, padx=0, pady=1, font=("Arial", 11))
        label_move_config.place(x=17, y=225)

        self.move_1_value = tk.IntVar()
        self.move_1_selector = tk.Checkbutton(self.root, text="Move 1", variable=self.move_1_value, onvalue=1, offvalue=0,
                                              command=lambda: (
                                                  InputHandler.inputs["moves_selector"].update({"1": self.move_1_value.get()}),
                                                  InputHandler.inputs["pp"]["info"].update({"1": self.spinbox_move_1.get()})
                                              ),
                                              width=10, height=1, padx=0, pady=0, font=("Arial", 9))
        self.move_1_selector.place(x=65, y=262)

        self.move_2_value = tk.IntVar()
        self.move_2_selector = tk.Checkbutton(self.root, text="Move 2", variable=self.move_2_value, onvalue=1, offvalue=0,
                                              command=lambda: (
                                                  InputHandler.inputs["moves_selector"].update({"2": self.move_2_value.get()}),
                                                  InputHandler.inputs["pp"]["info"].update({"2": self.spinbox_move_2.get()}),
                                              ),
                                              width=10, height=1, padx=0, pady=0, font=("Arial", 9))
        self.move_2_selector.place(x=65, y=279)

        self.move_3_value = tk.IntVar()
        self.move_3_selector = tk.Checkbutton(self.root, text="Move 3", variable=self.move_3_value, onvalue=1, offvalue=0,
                                              command=lambda: (
                                                  InputHandler.inputs["moves_selector"].update({"3": self.move_3_value.get()}),
                                                  InputHandler.inputs["pp"]["info"].update({"3": self.spinbox_move_3.get()}),
                                              ),
                                              width=10, height=1, padx=0, pady=0, font=("Arial", 9))
        self.move_3_selector.place(x=65, y=296)

        self.move_4_value = tk.IntVar()
        self.move_4_selector = tk.Checkbutton(self.root, text="Move 4", variable=self.move_4_value, onvalue=1, offvalue=0,
                                              command=lambda: (
                                                  InputHandler.inputs["moves_selector"].update({"4": self.move_4_value.get()}),
                                                  InputHandler.inputs["pp"]["info"].update({"4": self.spinbox_move_4.get()}),
                                              ),
                                              width=10, height=1, padx=0, pady=0, font=("Arial", 9))
        self.move_4_selector.place(x=65, y=313)

        # UI MOVEMENT CONFIG
        label_movement_config = tk.Label(self.root, text="Movement type", width=11, height=1, padx=0, pady=1,
                                         font=("Arial", 11))
        label_movement_config.place(x=24, y=355)

        self.movement_value = tk.StringVar()
        self.horizontal_movement_radio = tk.Radiobutton(self.root, text="Horizontal movement", variable=self.movement_value, value="HORIZONTAL",
                                                   command=lambda: InputHandler.inputs.update({"movement_type": self.movement_value.get()}))
        self.horizontal_movement_radio.place(x=30, y=375)
        self.vertical_movement_radio = tk.Radiobutton(self.root, text="Vertical movement", variable=self.movement_value, value="VERTICAL",
                                                 command=lambda: InputHandler.inputs.update({"movement_type": self.movement_value.get()}))
        self.vertical_movement_radio.place(x=30, y=392)
        self.square_movement_radio = tk.Radiobutton(self.root, text="Square movement", variable=self.movement_value, value="SQUARE",
                                               command=lambda: InputHandler.inputs.update({"movement_type": self.movement_value.get()}))
        self.square_movement_radio.place(x=30, y=409)

        self.horizontal_movement_radio.invoke()

        # UI MOVE CONFIG SELECTOR
        label_evs_config = tk.Label(self.root, text="Evs to improve", width=11, height=1, padx=0, pady=1, font=("Arial", 11))
        label_evs_config.place(x=170, y=225)

        self.atk_selector_value = tk.IntVar()
        self.atk_selector = tk.Checkbutton(self.root, text="ATK", variable=self.atk_selector_value, onvalue=1, offvalue=0,
                                           command=lambda: InputHandler.inputs["evs_to_train_selector"].update({"ATK": self.atk_selector_value.get()}))
        self.atk_selector.place(x=185, y=245)

        self.def_selector_value = tk.IntVar()
        self.def_selector = tk.Checkbutton(self.root, text="DEF", variable=self.def_selector_value, onvalue=1, offvalue=0,
                                           command=lambda: InputHandler.inputs["evs_to_train_selector"].update({"DEF": self.def_selector_value.get()}))
        self.def_selector.place(x=185, y=262)

        self.spd_selector_value = tk.IntVar()
        self.spd_selector = tk.Checkbutton(self.root, text="SPD", variable=self.spd_selector_value, onvalue=1, offvalue=0,
                                           command=lambda: InputHandler.inputs["evs_to_train_selector"].update({"SPD": self.spd_selector_value.get()}))
        self.spd_selector.place(x=185, y=279)

        self.sp_atk_selector_value = tk.IntVar()
        self.sp_atk_selector = tk.Checkbutton(self.root, text="SP.ATK", variable=self.sp_atk_selector_value, onvalue=1, offvalue=0,
                                              command=lambda: InputHandler.inputs["evs_to_train_selector"].update({"SPATK": self.sp_atk_selector_value.get()}))
        self.sp_atk_selector.place(x=185, y=296)

        self.sp_def_selector_value = tk.IntVar()
        self.sp_def_selector = tk.Checkbutton(self.root, text="SP.DEF", variable=self.sp_def_selector_value, onvalue=1, offvalue=0,
                                              command=lambda: InputHandler.inputs["evs_to_train_selector"].update({"SPDEF": self.sp_def_selector_value.get()}))
        self.sp_def_selector.place(x=185, y=313)

        self.hp_selector_value = tk.IntVar()
        self.hp_selector = tk.Checkbutton(self.root, text="HP", variable=self.hp_selector_value, onvalue=1, offvalue=0,
                                          command=lambda: InputHandler.inputs["evs_to_train_selector"].update({"HP": self.hp_selector_value.get()}))
        self.hp_selector.place(x=185, y=330)

    def create_pp_widgets(self):
        self.enable_pp_value = tk.IntVar()
        self.enable_pp = tk.Checkbutton(self.root, text="Enable PP manager", variable=self.enable_pp_value,
                                   onvalue=1, offvalue=0,
                                   command=lambda: (
                                       InputHandler.inputs["pp"].update({"enabled": self.enable_pp_value.get()}),
                                       self.update_window(),
                                   )
                                   )
        self.enable_pp.place(x=30, y=242)

        self.spinbox_move_1 = tk.Spinbox(self.root, from_=0, to=50, width=6, font=("Arial Bold", 7))
        self.spinbox_move_1.place(x=35, y=266)
        self.spinbox_move_2 = tk.Spinbox(self.root, from_=0, to=50, width=6, font=("Arial Bold", 7))
        self.spinbox_move_2.place(x=35, y=283)
        self.spinbox_move_3 = tk.Spinbox(self.root, from_=0, to=50, width=6, font=("Arial Bold", 7))
        self.spinbox_move_3.place(x=35, y=300)
        self.spinbox_move_4 = tk.Spinbox(self.root, from_=0, to=50, width=6, font=("Arial Bold", 7))
        self.spinbox_move_4.place(x=35, y=317)

    def create_notify_configuration_widgets(self):
        self.canvas.create_rectangle(5, 455, 290, 510, outline="light grey")

        label_notify_config = tk.Label(self.root, text="Notify Configuration", width=16, height=1, padx=1, pady=1,
                                       font=("Arial Bold", 13))
        label_notify_config.place(x=70, y=440)

        discord_label = tk.Label(self.root, text="Discord Id (number)", fg="black", font=("Arial Bold", 8))
        discord_label.place(x=71, y=465)

        self.discord_id = tk.Entry(self.root, width=20, )
        self.discord_id.place(x=60, y=485)

        self.jingle_var = tk.IntVar()
        self.jingle_selector = tk.Checkbutton(self.root, text="Jingle", variable=self.jingle_var, onvalue=1, offvalue=0,
                                         command=lambda: InputHandler.inputs["notify_configuration"].update({"jingle": self.jingle_var.get()}))
        self.jingle_selector.place(x=180, y=483)

    def create_catch_routine_widgets(self):
        self.canvas.create_rectangle(300, 25, 570, 380, outline="light grey")

        self.catch_routine_text = tk.Text(width=16, height=20)
        self.catch_routine_text.bind("<KeyRelease>", self.update_catch_routine_text)
        self.catch_routine_text.place(x=310, y=40)

        catch_routine_label = tk.Label(self.root, text="Catch routine", fg="black", font=("Arial Bold", 13))
        catch_routine_label.place(x=345, y=10)

        change_pokemon_button = tk.Button(self.root, text="changePokemon(position)", command=lambda: self.catch_routine_text_handler("changePokemon(2)") , width=18, height=1, padx=0, pady=1, font=("Arial", 7), relief=tk.GROOVE)
        change_pokemon_button.place(x=450, y=40)

        make_move_button = tk.Button(self.root, text="makeMove(position)", command=lambda: self.catch_routine_text_handler("makeMove(1)"), width=18, height=1, padx=0, pady=1, font=("Arial", 7), relief=tk.GROOVE)
        make_move_button.place(x=450, y=60)

        catch_button = tk.Button(self.root, text="catch(tries,pokeball)", command=lambda: self.catch_routine_text_handler("catch(3,1)"), width=18, height=1, padx=0, pady=1, font=("Arial", 7), relief=tk.GROOVE)
        catch_button.place(x=450, y=80)

        run_button = tk.Button(self.root, text="run(tries)", command=lambda: self.catch_routine_text_handler("run(5)"), width=18, height=1, padx=0, pady=1, font=("Arial", 7), relief=tk.GROOVE)
        run_button.place(x=450, y=100)

        self.enable_catch_routine_value = tk.IntVar()
        self.enable_catch_routine = tk.Checkbutton(self.root, text="Enable", variable=self.enable_catch_routine_value, onvalue=1, offvalue=0,
                                              command=lambda: InputHandler.inputs["catch"].update({"enabled": self.enable_catch_routine_value.get()}))
        self.enable_catch_routine.place(x=450, y=130)

    def catch_routine_text_handler(self, txt):
        self.catch_routine_text.insert(tk.END, f"{txt}")
        self.catch_routine_text.focus_set()
        pyautogui.press("enter")

    def update_catch_routine_text(self, event):
        InputHandler.inputs["catch"]["routine"] = self.catch_routine_text.get("1.0", tk.END).split("\n")[:-1]
        print(InputHandler.inputs["catch"])

    def create_template_widgets(self):
        self.canvas.create_rectangle(300, 400, 570, 530, outline="light grey")

        template_label = tk.Label(self.root, text="Templates", fg="black", font=("Arial Bold", 13))
        template_label.place(x=345, y=385)

        self.save_template_text = tk.Entry(self.root, width=26)
        self.save_template_text.place(x=310, y=420)

        save_template_button = tk.Button(self.root, text="Save template",
                                         command=lambda: self.save_template(), width=13,
                                         height=1, padx=0, pady=1, font=("Arial", 7), relief=tk.GROOVE)
        save_template_button.place(x=480, y=420)

        templates = ProkeUtils.get_templates()
        self.create_load_template_dropdown_widget(templates)

        load_template_button = tk.Button(self.root, text="Load template",
                                         command=lambda: self.load_template(),
                                         width=13,
                                         height=1, padx=0, pady=1, font=("Arial", 7), relief=tk.GROOVE)
        load_template_button.place(x=480, y=450)
        delete_template_button = tk.Button(self.root, text="Delete template",
                                         command=lambda: self.delete_template(self.selected_template.get()),
                                         width=13,
                                         height=1, padx=0, pady=1, font=("Arial", 7), relief=tk.GROOVE)
        delete_template_button.place(x=480, y=480)

    def update_window_handler(self, value):
        self.do_update_window = value

    def update_window_tick(self):
        while True:
            time.sleep(5)
            if not self.do_update_window:
                continue

            self.update_window()

    def update_window(self):
        self.pokemon_to_stop.delete(0, "end")
        self.pokemon_to_stop.insert(0, InputHandler.inputs["pokemon_to_stop"])

        self.pokemon_to_stop_while_evs.delete(0, "end")
        self.pokemon_to_stop_while_evs.insert(0, InputHandler.inputs["pokemon_to_stop_while_evs"])

        self.atk_selector.select() if InputHandler.inputs["evs_to_train_selector"]["ATK"] else self.atk_selector.deselect()
        self.def_selector.select() if InputHandler.inputs["evs_to_train_selector"]["DEF"] else self.def_selector.deselect()
        self.spd_selector.select() if InputHandler.inputs["evs_to_train_selector"]["SPD"] else self.spd_selector.deselect()
        self.sp_atk_selector.select() if InputHandler.inputs["evs_to_train_selector"]["SPATK"] else self.sp_atk_selector.deselect()
        self.sp_def_selector.select() if InputHandler.inputs["evs_to_train_selector"]["SPDEF"] else self.sp_def_selector.deselect()
        self.hp_selector.select() if InputHandler.inputs["evs_to_train_selector"]["HP"] else self.hp_selector.deselect()

        self.move_1_selector.select() if InputHandler.inputs["moves_selector"]["1"] else self.move_1_selector.deselect()
        self.move_2_selector.select() if InputHandler.inputs["moves_selector"]["2"] else self.move_2_selector.deselect()
        self.move_3_selector.select() if InputHandler.inputs["moves_selector"]["3"] else self.move_3_selector.deselect()
        self.move_4_selector.select() if InputHandler.inputs["moves_selector"]["4"] else self.move_4_selector.deselect()

        if not InputHandler.inputs["pp"]["enabled"]:
            self.enable_pp.deselect()
            self.spinbox_move_1.configure(state="disabled")
            self.spinbox_move_2.configure(state="disabled")
            self.spinbox_move_3.configure(state="disabled")
            self.spinbox_move_4.configure(state="disabled")
        else:
            self.enable_pp.select()
            self.spinbox_move_1.configure(state="normal")
            self.spinbox_move_2.configure(state="normal")
            self.spinbox_move_3.configure(state="normal")
            self.spinbox_move_4.configure(state="normal")

        self.spinbox_move_1.delete(0, "end")
        self.spinbox_move_1.insert(0, InputHandler.inputs["pp"]["info"]["1"])

        self.spinbox_move_2.delete(0, "end")
        self.spinbox_move_2.insert(0, InputHandler.inputs["pp"]["info"]["2"])

        self.spinbox_move_3.delete(0, "end")
        self.spinbox_move_3.insert(0, InputHandler.inputs["pp"]["info"]["3"])

        self.spinbox_move_4.delete(0, "end")
        self.spinbox_move_4.insert(0, InputHandler.inputs["pp"]["info"]["4"])

        if InputHandler.inputs["movement_type"] == "HORIZONTAL":
            self.horizontal_movement_radio.invoke()

        if InputHandler.inputs["movement_type"] == "VERTICAL":
            self.vertical_movement_radio.invoke()

        if InputHandler.inputs["movement_type"] == "SQUARE":
            self.square_movement_radio.invoke()

        self.discord_id.delete(0, "end")
        self.discord_id.insert(0, InputHandler.inputs["notify_configuration"]["discord_id"])
        self.jingle_selector.select() if InputHandler.inputs["notify_configuration"]["jingle"] else self.jingle_selector.deselect()

        self.catch_routine_text.delete("1.0", "end")
        self.catch_routine_text.insert("1.0", "\n".join(InputHandler.inputs["catch"]["routine"]))

        self.enable_catch_routine.select() if InputHandler.inputs["catch"]["enabled"] else self.enable_catch_routine.deselect()

    def input_refresh(self):
        InputHandler.inputs = {
            "pokemon_to_stop": self.pokemon_to_stop.get(),
            "pokemon_to_stop_while_evs": self.pokemon_to_stop_while_evs.get(),
            "evs_to_train_selector": {
                "ATK": self.atk_selector_value.get(),
                "DEF": self.def_selector_value.get(),
                "SPD": self.spd_selector_value.get(),
                "SPATK": self.sp_atk_selector_value.get(),
                "SPDEF": self.sp_def_selector_value.get(),
                "HP": self.hp_selector_value.get(),
            },
            "moves_selector": {
                "1": self.move_1_value.get(),
                "2": self.move_2_value.get(),
                "3": self.move_3_value.get(),
                "4": self.move_4_value.get(),
            },
            "pp": {
                "enabled": self.enable_pp_value.get(),
                "info": {
                    "1": self.spinbox_move_1.get(),
                    "2": self.spinbox_move_2.get(),
                    "3": self.spinbox_move_3.get(),
                    "4": self.spinbox_move_4.get(),
                }
            },
            "movement_type": self.movement_value.get(),
            "notify_configuration": {
                "jingle": self.jingle_var.get(),
                "discord_id": self.discord_id.get(),
            },
            "catch": {
                "enabled": self.enable_catch_routine_value.get(),
                "routine": self.catch_routine_text.get("1.0", tk.END).split("\n")[:-1]
            }
        }

    def save_template(self):
        self.input_refresh()
        ProkeUtils.save_template(self.save_template_text.get())

        templates = ProkeUtils.get_templates()
        self.create_load_template_dropdown_widget(templates)

    def load_template(self):
        ProkeUtils.load_template(self.selected_template.get())
        self.update_window()

    def delete_template(self, filename):
        ProkeUtils.delete_template(filename)

        templates = ProkeUtils.get_templates()
        self.create_load_template_dropdown_widget(templates)

    def create_load_template_dropdown_widget(self, templates):
        self.selected_template = tk.StringVar()
        load_template_listbox = ttk.Combobox(self.root, state="readonly", textvariable=self.selected_template, width=23, values=templates)
        load_template_listbox.place(x=310, y=450)
