class InputHandler:
    inputs = {
        "pokemon_to_stop": "",
        "pokemon_to_stop_while_evs": "",
        "evs_to_train_selector": {
            "ATK": False,
            "DEF": False,
            "SPD": False,
            "SPATK": False,
            "SPDEF": False,
            "HP": False,
        },
        "notify_configuration": {
            "jingle": False,
            "discord_id": "",
        },
        "moves_selector": {
            "1": False,
            "2": False,
            "3": False,
            "4": False,
        },
        "pp": {
            "enabled": False,
            "info": {
                "1": 0,
                "2": 0,
                "3": 0,
                "4": 0,
            }
        },
        "movement_type": "",
        "catch": {
            "enabled": False,
            "routine": []
        }
    }

