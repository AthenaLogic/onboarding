# The plan

We will do the following steps.

*Reasoning*
Yubikeys are gpg-cards so they support card-edit and the like. We can hope that only key will add those features in the future, but until then, the onlykey cannot generate subkeys on its own. So we will create a "root" authority, as securely as we can, then issue subkeys from there. We will load those subkeys to the onlykey so that only 

# 1. Set up your onlykey
Follow directions at https://docs.crp.to/usersguide.html#initial-setup

- ensure you set "Derived Key User Input Mode" to "Button Press"

## Notes:

- OnlyKey supports RSA OpenPGP keys of sizes 2048 and 4096.
- OnlyKey supports ECC OpenPGP keys of type X25519 and NIST256P1
- Decryption operations using a 2048 size key takes about 2 seconds, with 4096 size key it takes about 9 seconds.

RSA 2048 is deprecated now, so we will use the newer ECC format.


# 2. Install required tools

## Install gnupg
```console
$ brew install gnupg
```

## Install onlykey agent
``` console
$ pip3 install onlykey-agent
```

# 3. Create GPG keys

## Create master key on the hardware token

### Use onlykey to generate keys
We will specify the current unix timestamp to make this harder to recreate.

**It will still ask for the 3 digit challenge code, but because you set "Button Press" you can press any button**

```console
$ onlykey-gpg init "John Doe <jd@gmail.com>" -t $(date +%s)
Enter the 3 digit challenge code on OnlyKey to authorize <gpg://John Doe <jd@gmail.com>|ed25519>
6 5 5
Enter the 3 digit challenge code on OnlyKey to authorize <gpg://John Doe <jd@gmail.com>|ed25519>
2 3 3
gpg: inserting ownertrust of 6
gpg: checking the trustdb
gpg: marginals needed: 3  completes needed: 1  trust model: pgp
gpg: depth: 0  valid:   1  signed:   0  trust: 0-, 0q, 0n, 0m, 0f, 1u
sec   ed25519 2022-05-12 [SC]
      273BCC623CB32CE1FA27911804F210A3BF24B54D
uid           [ultimate] John Doe <jd@gmail.com>
ssb   cv25519 2022-05-12 [E]
```

### Add config to shell config file
```console
$ echo "GNUPGHOME=~/.gnupg/onlykey" >> ~/.zshrc
```

This GNUPGHOME contains your hardware keyring and agent settings. This agent software assumes all keys are backed by hardware devices so you can’t use standard GPG keys in GNUPGHOME (if you do mix keys you’ll receive an error when you attempt to use them).

If you wish to switch back to your software keys unset GNUPGHOME.

### Reset your shell

Load the new gpg config
```console
$ reset
```

Verify the gpg agent loaded and can read your keys:
```console
$ gpg -K
/Users/[your username]/.gnupg/onlykey/pubring.kbx
-----------------------------------------------
sec   ed25519 2022-05-12 [SC]
      273BCC623CB32CE1FA27911804F210A3BF24B54D
uid           [ultimate] John Doe <jd@gmail.com>
ssb   cv25519 2022-05-12 [E]
```

## Load a temp directory
```console
$ TMPDIR=$(mktemp -dt gpg)
$ cd $TMPDIR
$ pwd
/var/folders/r9/2ktnrhq15z12k12268gp1l8r0000gn/T/gpg.ohLCfR6D
```

## Create the rest of the keys
```console
$ MYEMAIL="jd@gmail.com"
$ gpg --edit-key --expert $MYEMAIL
gpg (GnuPG) 2.3.6; Copyright (C) 2021 Free Software Foundation, Inc.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Secret key is available.

sec  ed25519/C5837318D04642EE
     created: 1970-01-01  expires: never       usage: SC
     trust: ultimate      validity: ultimate
ssb  cv25519/CFBE654004BC886E
     created: 1970-01-01  expires: never       usage: E
[ultimate] (1). Holland Gibson <holland.gibson@gmail.com>
gpg>
```
