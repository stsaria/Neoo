sudo apt update && sudo apt upgrade && sudo apt install python3-plyvel libleveldb-dev
mkdir ~/.pip
echo "[global]
break-system-packages=yes" > ~/.pip/pip.conf