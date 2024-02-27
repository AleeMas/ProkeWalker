# ProkeWalker for Pokemon Revolution Online
The ProkeWalker is a bot made to assist trainers in optimizing their gameplay experience assisting the actions in the Pokemon Revolution Online universe that are repeated and become boring . This bot allowe trainers to find specific Pokemon and train Evs and catch.
## Features
- Find Pokemon: run out from all Pokemon except the one you're looking for, it stop when it find the Pokemon sending you a notification

- Farm EVs: fight all the pokemon that drop the EVs you want, using random moves or the one you insert


- Catch while EVsing: fights with moves you selected or random moves against pokemon giving evs selected below, but stops if it encounters the Pokemon written in the box sending you a notification

- Catch routine: with the catch routine you can configurate your own steps of operations when you find a Pokemon that you want to catch:
  - changePokemon(position), this will change Pokemon with the one you chose from 1 to 6
  - makeMoves(position), this will chose the move the Pokemon you have in combat will to from 1 to 4
  - catchTries(tries,pokeball), this will try to catch the Pokemon "tries" times using the pokeball you choose depending the position if has in your bag
  - run(tries), this option will escape from the battle "tries" times, use this in case bot won't catch the pokemon after the tries you chose in the previous operation

*Notification
To get notified on Discord, jingle or both compile form in the notification section. Notify is starting if you find the Pokemon you're looking for or if there is a rare Pokemon (shiny form)

## Important
- Be sure you always open before the game and then start the bot
- Edit discord web hook to get notify about catch in your preferred discord (constant.py)
- Chose your prefered jingle, if you want edit it in the folder sounds.

![Test Image](ProkeWalkerUI.png)
