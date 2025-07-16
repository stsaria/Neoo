#!/bin/bash
makeVenv(){
  if [ -d ./.$1Venv ]; then
    return 0
  fi
  python3 -m venv .$1Venv
  source ./.$1Venv/bin/activate
  ./.$1Venv/bin/python3 -m pip install -r requirements$1.txt
}

sudo apt update && sudo apt upgrade -y && sudo apt install -y python3 python3-venv python3-plyvel libleveldb-dev

sudo chmod -R 700 ./

makeVenv Main
makeVenv SelfBot
makeVenv Bot

./.SelfBotVenv/bin/python3 -m src.selfBot.Main &
selfBotPid=$!
./.BotVenv/bin/python3 -m src.bot.Main &
botPid=$!
./.MainVenv/bin/python3 -m src.Main
kill $selfBotPid $botPid