# Intro

This guide picks up from gpg-setup.md to add the subkeys to your onlykey. This ensures that the private key data never gets onto your host machines (except the machine used to generate them).

# Configure your onlykey
Please follow the online guide provided by the vendor.

Ensure that (stored user key mode)[https://docs.crp.to/onlykey-agent.html#setting-stored-key-user-input-mode] is set to button press, not challenge.

# Add subkeys to onlykey

I assume you will be using slots ECC1 and ECC2, so please change them accordingly if needed.

ECC1 = signing subkey
ECC2 = encryption (aka decryption) subkey

## Extract the raw key bytes
The onlykey-cli expects only the raw 32 bytes of the key (for ed25519 keys), so we have to extract them.

Assuming you followed the steps for onlykey in the beginning of the gpg-setup.md guide...

```console
$ python3 extract_keys.py
root GPG passphrase:
[deprecation warnings]
Load these raw key values to OnlyKey by using the OnlyKey App --> Advanced -> Add Private Key
rootkey is now unlocked
rootkey type %s PubKeyAlgorithm.EdDSA
rootkey value:
2c9948c41e557be0f414ec60eda7183c30769545f0f77e7c571ac61c2e2a96ed
subkey values:
subkey id BECFA3C1AE191D15
subkey value
3427765d43fbf067c62f4dc0438aaa8e56c4df9f6c05f9b0caf29ccd6866aa00
Saved key to /home/pi/gnupg-workspace/BECFA3C1AE191D15-raw.hex
subkey id 5912A795E90DD2CF
subkey value
e309c2269bfb32012049ed746eb1d68edaaf2fba656e3a865ebd97d83277c64a
Saved key to /home/pi/gnupg-workspace/5912A795E90DD2CF-raw.hex
subkey id 3F29127E79649A3D
subkey value
7abf23b34f9a37c9db1d7af20fa29cc144ac0372ffae36ca73778ed08fb88b27
Saved key to /home/pi/gnupg-workspace/3F29127E79649A3D-raw.hex
```

This creates 3 files containing the raw key data (which is very sensitive!)

## Connect onlykey
- Insert the key, type in the PIN so that the green light stays on.
- Check that the CLI and everything connect:
  - `onlykey-cli wink`
  - a blue light should blink once
- Set key to config mode, hold the #6 key for 5+ seconds, then type your PIN again.


## Send to onlykey
There is no actual difference between signing and auth, except on the agent side. So you can use a signing key to authenticate.
Only key will therefore take the first two keys. Note the key IDs:

```console
$ gpg -K
sec   rsa4096/0xFF3E7D88647EBCDB 2017-10-09 [C]
      Key fingerprint = 011C E16B D45B 27A5 5BA8  776D FF3E 7D88 647E BCDB
uid                            Dr Duh <doc@duh.to>
ssb   rsa4096/0xBECFA3C1AE191D15 2017-10-09 [S] [expires: 2018-10-09]
ssb   rsa4096/0x5912A795E90DD2CF 2017-10-09 [E] [expires: 2018-10-09]
ssb   rsa4096/0x3F29127E79649A3D 2017-10-09 [A] [expires: 2018-10-09]
```


We transfer them to the onlykey with `onlykey-cli`

check the id to match, ECC1 signing key, ECC2 decrypt key

```console
$ onlykey-cli setkey ECC1 x s $(cat $GNUPGHOME/BECFA3C1AE191D15-raw.hex)
Successfully set ECC Key
$ onlykey-cli setkey ECC2 x d $(cat $GNUPGHOME/5912A795E90DD2CF-raw.hex)
```

You can now remove your onlykey.

## Clean up on secure machine

We will use secure rm `srm` to ensure the sensitive files are deleted. If you are on a memory-only "live boot" system then you don't really need to worry about this, but it won't hurt.

```console
$ srm -v $GNUPGHOME/*.hex
```

# Set up developer workstation

Assuming a mac, starting from here: https://docs.crp.to/onlykey-agent.html#gpg-agent-quickstart-guide-stored-keys

Download your public key. If you already submitted it to a keyserver, just navigate there and download it, i.e. https://keys.openpgp.org/
Otherwise, you will have to transfer it to your workstation. (On the previous guide it was transferred to a usb drive on a file called something like `gpg-John Doe <jd@example.com>-2022-05-13.asc`)

```console
$ mkdir -p ~/.gnupg/public/
$ mv Downloads/gpg-0xFF3E7D88647EBCDB-2022-05-13.asc ~/.gnupg/public/
```

## Set onlykey to use your public key and onlykey for the gpg agent

Install the required agent
```console
$ pip3 install onlykey-agent
[pip3 output ...]
```

```console
$ onlykey-gpg init "John Doe <jd@example.com>" -sk ECC1 -dk ECC2 -i ~/.gnupg/public/gpg-0xFF3E7D88647EBCDB-2022-05-13.asc
gpg: inserting ownertrust of 6
gpg: checking the trustdb
gpg: marginals needed: 3  completes needed: 1  trust model: pgp
gpg: depth: 0  valid:   1  signed:   0  trust: 0-, 0q, 0n, 0m, 0f, 1u
sec   ed25519 2022-05-13 [C]
      06EECE1EAFBFA0709574CBA2125F052F7FC6955
uid           [ultimate] John Doe <jd@example.com>
ssb   ed25519 2022-05-13 [S] [expires: 2023-05-13]
ssb   cv25519 2022-05-13 [E] [expires: 2023-05-13]
ssb   ed25519 2022-05-13 [A] [expires: 2023-05-13]
```

Then add the gpg config to your shell config file, assuming you use zsh (the default on MacOS now, and a great idea in general - see the starship and ohmyzsh projects) you would run the following command:
```console
$ echo "export GNUPGHOME=${HOME}/.gnupg/onlykey" >> ~/.zshrc
```
---

to set the keyid without having to type it all out
```console
$ KEYID=$(gpg -K | grep "\[S\]" | awk '{split($0, array, " "); print array[2]} | tail -c 19')
$


$ gpg --output private_auth.asc --armor --export-secret-key [hex of auth key]
$ gpg --output private_signing.asc --armor --export-secret-key [hex of sign key]
$ gpg --output private_encrypt.asc --armor --export-secret-key [hex of encryption key]
```
