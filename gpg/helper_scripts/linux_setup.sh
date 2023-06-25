#!/usr/bin/env bash


set -ex
sudo apt install -y wget gnupg2 gnupg-agent dirmngr cryptsetup paperkey secure-delete zip

./download_files.sh

cd ~

# mkdir -p ~/bin
# cd -p ~/bin
# echo "PATH=$HOME/bin:$PATH" >> ~/.bashrc
if [ $(uname -m) = "aarch64" ]; then
	wget http://http.us.debian.org/debian/pool/main/h/haskell-hopenpgp-tools/hopenpgp-tools_0.23.7-1_arm64.deb
else
	wget http://http.us.debian.org/debian/pool/main/h/haskell-hopenpgp-tools/hopenpgp-tools_0.23.7-1_amd64.deb
fi

sudo apt install -y ./*.deb

