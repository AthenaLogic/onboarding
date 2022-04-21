1. Install GPG
```console
brew install gnupg
```

```
# create temp dir
TMPDIR=$(mktemp -dt gpg)
cd $TMPDIR

MYEMAIL="<your new email address>"
$ gpg --full-generate-key
gpg (GnuPG) 2.3.4; Copyright (C) 2021 Free Software Foundation, Inc.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Please select what kind of key you want:
   (1) RSA and RSA
   (2) DSA and Elgamal
   (3) DSA (sign only)
   (4) RSA (sign only)
   (9) ECC (sign and encrypt) *default*
  (10) ECC (sign only)
  (14) Existing key from card
Your selection?
Please select which elliptic curve you want:
   (1) Curve 25519 *default*
   (4) NIST P-384
   (6) Brainpool P-256
Your selection?
Please specify how long the key should be valid.
         0 = key does not expire
      <n>  = key expires in n days
      <n>w = key expires in n weeks
      <n>m = key expires in n months
      <n>y = key expires in n years
Key is valid for? (0)
Key does not expire at all
Is this correct? (y/N)
Key is valid for? (0) 1y
Key expires at Thu Apr 20 17:25:37 2023 EDT
Is this correct? (y/N) n
Key is valid for? (0)
Key does not expire at all
Is this correct? (y/N) y

GnuPG needs to construct a user ID to identify your key.

Real name: G. Holland Gibson
Email address: holland.gibson@gmail.com
Comment:
You selected this USER-ID:
    "G. Holland Gibson <holland.gibson@gmail.com>"

Change (N)ame, (C)omment, (E)mail or (O)kay/(Q)uit? c
Comment: 2022-01-20
You selected this USER-ID:
    "G. Holland Gibson (2022-01-20) <holland.gibson@gmail.com>"

Change (N)ame, (C)omment, (E)mail or (O)kay/(Q)uit? o
We need to generate a lot of random bytes. It is a good idea to perform
some other action (type on the keyboard, move the mouse, utilize the
disks) during the prime generation; this gives the random number
generator a better chance to gain enough entropy.
We need to generate a lot of random bytes. It is a good idea to perform
some other action (type on the keyboard, move the mouse, utilize the
disks) during the prime generation; this gives the random number
generator a better chance to gain enough entropy.
gpg: revocation certificate stored as '/Users/hollandgibson/.gnupg/openpgp-revocs.d/6E25387C4EFBBED11707867194754B0BB673C16A.rev'
public and secret key created and signed.

pub   ed25519 2022-04-20 [SC]
      6E25387C4EFBBED11707867194754B0BB673C16A
uid                      G. Holland Gibson (2022-01-20) <holland.gibson@gmail.com>
sub   cv25519 2022-04-20 [E]
```

```
$ gpg --edit-key --expert $MYEMAIL
gpg (GnuPG) 2.3.4; Copyright (C) 2021 Free Software Foundation, Inc.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Secret key is available.

sec  ed25519/556B413BDEC02EC8
     created: 2022-04-20  expires: never       usage: SC
     trust: ultimate      validity: ultimate
ssb  cv25519/A152BC2633C9CC4B
     created: 2022-04-20  expires: never       usage: E
[ultimate] (1). G. Holland Gibson (2022-01-20) <holland.gibson@gmail.com>

gpg> addkey
Please select what kind of key you want:
   (3) DSA (sign only)
   (4) RSA (sign only)
   (5) Elgamal (encrypt only)
   (6) RSA (encrypt only)
   (7) DSA (set your own capabilities)
   (8) RSA (set your own capabilities)
  (10) ECC (sign only)
  (11) ECC (set your own capabilities)
  (12) ECC (encrypt only)
  (13) Existing key
  (14) Existing key from card
Your selection? 10
Please select which elliptic curve you want:
   (1) Curve 25519 *default*
   (2) Curve 448
   (3) NIST P-256
   (4) NIST P-384
   (5) NIST P-521
   (6) Brainpool P-256
   (7) Brainpool P-384
   (8) Brainpool P-512
   (9) secp256k1
Your selection?
Please specify how long the key should be valid.
         0 = key does not expire
      <n>  = key expires in n days
      <n>w = key expires in n weeks
      <n>m = key expires in n months
      <n>y = key expires in n years
Key is valid for? (0) 1y
Key expires at Thu Apr 20 17:31:01 2023 EDT
Is this correct? (y/N) y
Really create? (y/N) y
We need to generate a lot of random bytes. It is a good idea to perform
some other action (type on the keyboard, move the mouse, utilize the
disks) during the prime generation; this gives the random number
generator a better chance to gain enough entropy.

sec  ed25519/556B413BDEC02EC8
     created: 2022-04-20  expires: never       usage: SC
     trust: ultimate      validity: ultimate
ssb  cv25519/A152BC2633C9CC4B
     created: 2022-04-20  expires: never       usage: E
ssb  ed25519/B840CE4D7C47C87D
     created: 2022-04-20  expires: 2023-04-20  usage: S
[ultimate] (1). G. Holland Gibson (2022-01-20) <holland.gibson@gmail.com>

gpg> addkey
Please select what kind of key you want:
   (3) DSA (sign only)
   (4) RSA (sign only)
   (5) Elgamal (encrypt only)
   (6) RSA (encrypt only)
   (7) DSA (set your own capabilities)
   (8) RSA (set your own capabilities)
  (10) ECC (sign only)
  (11) ECC (set your own capabilities)
  (12) ECC (encrypt only)
  (13) Existing key
  (14) Existing key from card
Your selection? 11

Possible actions for this ECC key: Sign Authenticate
Current allowed actions: Sign

   (S) Toggle the sign capability
   (A) Toggle the authenticate capability
   (Q) Finished

Your selection? a

Possible actions for this ECC key: Sign Authenticate
Current allowed actions: Sign Authenticate

   (S) Toggle the sign capability
   (A) Toggle the authenticate capability
   (Q) Finished

Your selection? s

Possible actions for this ECC key: Sign Authenticate
Current allowed actions: Authenticate

   (S) Toggle the sign capability
   (A) Toggle the authenticate capability
   (Q) Finished

Your selection? q
Please select which elliptic curve you want:
   (1) Curve 25519 *default*
   (2) Curve 448
   (3) NIST P-256
   (4) NIST P-384
   (5) NIST P-521
   (6) Brainpool P-256
   (7) Brainpool P-384
   (8) Brainpool P-512
   (9) secp256k1
Your selection?
Please specify how long the key should be valid.
         0 = key does not expire
      <n>  = key expires in n days
      <n>w = key expires in n weeks
      <n>m = key expires in n months
      <n>y = key expires in n years
Key is valid for? (0) 1y
Key expires at Thu Apr 20 17:31:26 2023 EDT
Is this correct? (y/N) y
Really create? (y/N) y
We need to generate a lot of random bytes. It is a good idea to perform
some other action (type on the keyboard, move the mouse, utilize the
disks) during the prime generation; this gives the random number
generator a better chance to gain enough entropy.

sec  ed25519/556B413BDEC02EC8
     created: 2022-04-20  expires: never       usage: SC
     trust: ultimate      validity: ultimate
ssb  cv25519/A152BC2633C9CC4B
     created: 2022-04-20  expires: never       usage: E
ssb  ed25519/4C10ACD6DEC6E02E
     created: 2022-04-20  expires: 2023-04-20  usage: S
ssb  ed25519/BCF8D0A788628F22
     created: 2022-04-20  expires: 2023-04-20  usage: A
[ultimate] (1). G. Holland Gibson (2022-01-20) <holland.gibson@gmail.com>

gpg> addkey
Please select what kind of key you want:
   (3) DSA (sign only)
   (4) RSA (sign only)
   (5) Elgamal (encrypt only)
   (6) RSA (encrypt only)
   (7) DSA (set your own capabilities)
   (8) RSA (set your own capabilities)
  (10) ECC (sign only)
  (11) ECC (set your own capabilities)
  (12) ECC (encrypt only)
  (13) Existing key
  (14) Existing key from card
Your selection? 12
Please select which elliptic curve you want:
   (1) Curve 25519 *default*
   (2) Curve 448
   (3) NIST P-256
   (4) NIST P-384
   (5) NIST P-521
   (6) Brainpool P-256
   (7) Brainpool P-384
   (8) Brainpool P-512
   (9) secp256k1
Your selection?
Please specify how long the key should be valid.
         0 = key does not expire
      <n>  = key expires in n days
      <n>w = key expires in n weeks
      <n>m = key expires in n months
      <n>y = key expires in n years
Key is valid for? (0) 1y
Key expires at Thu Apr 20 17:31:43 2023 EDT
Is this correct? (y/N) y
Really create? (y/N) y
We need to generate a lot of random bytes. It is a good idea to perform
some other action (type on the keyboard, move the mouse, utilize the
disks) during the prime generation; this gives the random number
generator a better chance to gain enough entropy.

sec  ed25519/556B413BDEC02EC8
     created: 2022-04-20  expires: never       usage: SC
     trust: ultimate      validity: ultimate
ssb  cv25519/A152BC2633C9CC4B
     created: 2022-04-20  expires: never       usage: E
ssb  ed25519/4C10ACD6DEC6E02E
     created: 2022-04-20  expires: 2023-04-20  usage: S
ssb  ed25519/BCF8D0A788628F22
     created: 2022-04-20  expires: 2023-04-20  usage: A
ssb  cv25519/CEA90D62B2180DEF
     created: 2022-04-20  expires: 2023-04-20  usage: E
[ultimate] (1). G. Holland Gibson (2022-01-20) <holland.gibson@gmail.com>

gpg> save
```

# remove the auto-created subkey
Gnupg (on Mac at least) creates an ecruption key that never expires, lets remove it.

```
gpg --list-keys
/Users/hollandgibson/.gnupg/pubring.kbx
---------------------------------------
pub   ed25519 2022-04-20 [SC]
      6E25387C4EFBBED11707867194754B0BB673C16A
uid           [ultimate] G. Holland Gibson <holland.gibson@gmail.com>
sub   cv25519 2022-04-20 [E]
sub   ed25519 2022-04-20 [S] [expires: 2023-04-20]
sub   ed25519 2022-04-20 [A] [expires: 2023-04-20]
sub   cv25519 2022-04-20 [E] [expires: 2023-04-20]
```

see how the first sub key never expires?

```
gpg --list-secret-keys --keyid-format LONG
/Users/hollandgibson/.gnupg/pubring.kbx
---------------------------------------
sec   ed25519/33ACBCAADAEF81F5 2022-04-20 [SC]
      9EEBB01A51D3E4C86C7524AD33ACBCAADAEF81F5
uid                 [ultimate] G. Holland Gibson <holland.gibson@gmail.com>
ssb   cv25519/F239D3169A37A02B 2022-04-20 [E]             <---- THIS ONE!
ssb   ed25519/A6EFD1DAB1DE5E11 2022-04-20 [S] [expires: 2023-04-20]
ssb   ed25519/2BF9775466DAEED3 2022-04-20 [A] [expires: 2023-04-20]
ssb   cv25519/E1C101074307C707 2022-04-20 [E] [expires: 2023-04-20]
```

```
gpg --delete-secret-and-public-keys F239D3169A37A02B!
gpg (GnuPG) 2.3.4; Copyright (C) 2021 Free Software Foundation, Inc.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.


ssb  cv25519/F239D3169A37A02B 2022-04-20 G. Holland Gibson <holland.gibson@gmail.com>

Note: Only the secret part of the shown subkey will be deleted.

Delete this key from the keyring? (y/N) y
This is a secret key! - really delete? (y/N) y

sub  cv25519/F239D3169A37A02B 2022-04-20 G. Holland Gibson <holland.gibson@gmail.com>

Note: Only the shown public subkey will be deleted.

Delete this key from the keyring? (y/N) y
```

# create backups
In the future we'll use multiple solo keys for this
```

gpg --export-ownertrust > $TMPDIR/backup_trustdb.txt
gpg --armor --export-secret-keys <your_email_address> > $TMPDIR/secret_keys_<your_email_address>.asc
###(enter passphrase if prompted)
gpg --armor --export-secret-subkeys <your_email_address> > $TMPDIR/secret_subkeys_<your_email_address>.asc
###(enter passphrase if prompted)

# copy files to a CD/flash drive and keep somewhere VERY SAFE
```

# Copy key to github
`gpg --armor --export $MYEMAIL | pbcopy`

# Tell local git agent to use your GPG keys
```
gpg --list-secret-keys --keyid-format LONG $MYEMAIL
git config --global user.signingkey 6DCB9294B2139D96 # the one with [S]
git config --global gpg.program gpg
git config --global commit.gpgsign true
```

If you have other repos that you want to use other signing keys with, you can just omit the `--global` and run that code in every repo.

# Publish your GPG key
Add the following to gpg.conf:
`keyserver hkps://keys.openpgp.org `


Publish your email
```
gpg --export $MYEMAIL | curl -T - https://keys.openpgp.org
```
Complete verification

```
gpg --refresh-keys
```

```
gpg --refresh-keys
```

Practice finding my gpg key:
```console
$ gpg --auto-key-locate keyserver --locate-keys holland.gibson@gmail.com
pub   ed25519 2022-04-20 [SC]
      6E25387C4EFBBED11707867194754B0BB673C16A
uid           [ultimate] G. Holland Gibson (2022-01-20) <holland.gibson@gmail.com>
sub   cv25519 2022-04-20 [E]
sub   ed25519 2022-04-20 [S] [expires: 2023-04-20]
sub   ed25519 2022-04-20 [A] [expires: 2023-04-20]
sub   cv25519 2022-04-20 [E] [expires: 2023-04-20]
```


# Revoking keys
Once created, GPG keys cannot be edited. You have to revoke and start over, notifying the keyserver (and github)

```
TMPDIR=$(mktemp -dt gpg)
cd $TMPDIR
gpg --output revoke.asc --gen-revoke holland.gibson@gmail.com

sec  ed25519/556B413BDEC02EC8 2022-04-20 G. Holland Gibson (2022-01-20) <holland.gibson@gmail.com>

Create a revocation certificate for this key? (y/N) y
Please select the reason for the revocation:
  0 = No reason specified
  1 = Key has been compromised
  2 = Key is superseded
  3 = Key is no longer used
  Q = Cancel
(Probably you want to select 1 here)
Your decision? 2
Enter an optional description; end it with an empty line:
>
Reason for revocation: Key is superseded
(No description given)
Is this okay? (y/N) y
ASCII armored output forced.
Revocation certificate created.

Please move it to a medium which you can hide away; if Mallory gets
access to this certificate he can use it to make your key unusable.
It is smart to print this certificate and store it away, just in case
your media become unreadable.  But have some caution:  The print system of
your machine might store the data and make it available to others!
```

Import revocation to keyring
```
gpg --import revoke.asc
```

Revoke on server:
```
# get KEY ID
gpg --auto-key-locate keyserver --locate-keys $MYEMAIL
gpg --auto-key-locate keyserver --send-keys 6E25387C4EFBBED11707867194754B0BB673C16A
```
Manually delete on github

Delete revoke certificate
```
cd ~
rm -rf $TMPDIR
```

You will want to keep your old revoked key for decrypting messages that use the old key. If it really annoys you, you can always export it (see backing up above) and keep it for when you need it.


Guides loosely followed:
- https://dev.to/barrage/step-by-step-guide-on-how-to-set-up-yubikey-with-gpg-subkeys-5an8
- https://github.com/drduh/YubiKey-Guide
