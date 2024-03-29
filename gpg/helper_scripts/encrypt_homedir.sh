#!/usr/bin/env bash
set -ex

sudo apt install -y cryptsetup ecryptfs-utils rsync
sudo modprobe ecryptfs
echo ecryptfs | sudo tee -a /etc/modules-load.d/modules.conf

set +e
id temp
TEMP_EXIST=$?

set -e
if [ $TEMP_EXIST -ne 0 ]; then
    sudo useradd -m temp
    echo "set password for 'temp'"
    sudo passwd temp
fi

cat <<EOF | sudo tee /usr/local/bin/encrypt_homedir_step2.sh  
#!/usr/bin/env bash
whoami

if [ "\$(whoami)" = "root" ]; then

#the user to encrypt is the second to last user

set -e
enc_user=\$(cat /etc/passwd | tail -n 2 | head -n 1 | grep -Eo '^[a-zA-Z0-9]+')
read -p "Are you sure you want to encrypt username: \$enc_user? This is a \
destructive action and cannot easily be undone." -n 1 -r
if [[ \$REPLY =~ ^[Yy]$ ]]
then
    ecryptfs-migrate-home -u \$enc_user
fi

echo "You MUST log out and login as \$enc_user before rebooting!!!"
echo "Please run ecryptfs-unwrap-passphrase (in ~/backup-crypt-key.sh after logging back in"

else
echo "You must execute this as root: try 'sudo encrypt_homedir_step2.sh'"
fi
EOF

echo -e "#!/bin/bash \necryptfs-unwrap-passphrase" > $HOME/backup-crypt-key.sh
chmod +x $HOME/backup-crypt-key.sh

sudo chown root:root /usr/local/bin/encrypt_homedir_step2.sh
sudo chmod 700 /usr/local/bin/encrypt_homedir_step2.sh

echo -e "ALL \tALL=(root) NOPASSWD: /usr/local/bin/encrypt_homedir_step2.sh" | sudo tee /etc/sudoers.d/encrypt_step

echo "Log out and log in as temp now, then run 'sudo encrypt_homedir_step2.sh'"