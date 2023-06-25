#!/usr/bin/env bash
set -ex

osname="$(uname -o)"

if [ "$osname" = "GNU/Linux" ]; then
  sudo apt update && sudo apt upgrade -y
  sudo apt install -y python3-pip python3-tk libusb-1.0-0-dev libudev-dev
  # pip3 install onlykey-agent
  sudo cp ~/49-onlykey.rules /etc/udev/rules.d/
  sudo udevadm control --reload-rules && sudo udevadm trigger
elif [ "$osname" = "Darwin" ]; then
  brew install onlykey-agent
else
  set +ex
  echo "Unknown operating system, follow the instructions at https://docs.onlykey.io/onlykey-agent.html#installation"
fi
