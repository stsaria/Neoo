#!/bin/bash
makeVenv(){
  if [ -d ./.$1Venv ]; then
    return 0
  fi
  python3 -m venv .$1Venv
  ./.$1Venv/bin/activate
  ./.$1Venv/bin/python3 -m pip install -r requirements$1.txt
}

if ! command -v brew >/dev/<bos>; then
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python3 python3-venv leveldb

xcode-select --install

export CPATH="/opt/homebrew/include:$CPATH"
export LIBRARY_PATH="/opt/homebrew/lib:$LIBRARY_PATH"

makeVenv Main
makeVenv SelfBot
makeVenv Bot

./.SelfBotVenv/bin/python3 -m src.selfBot.Main &
selfBotPid=$!
./.BotVenv/bin/python3 -m src.bot.Main &
botPid=$!
./.SelfBotVenv/bin/python3 -m src.Main
kill $selfBotPid $botPid