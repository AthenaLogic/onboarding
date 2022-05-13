# The plan

We will do the following steps:


### *Reasoning*

Yubikeys are gpg-cards so they support card-edit and the like. We can hope that only key will add those features in the future, but until then, the onlykey cannot generate subkeys in a way that we need on its own. So we will create a "root" authority, as securely as we can, then issue subkeys from there. We will load those subkeys to the onlykey so that only.

Ideally, on linux (even a hardened linux VM is a good call), but the mac commands are included when they are separate.

# Install tools

First clone this repo:
```bash
git clone https://github.com/AthenaLogic/onboarding.git
```

mac:
```console
$ brew install gnupg hopenpgp-tools paperkey secure-delete
```

linux:
```console
# apt -y install wget gnupg2 gnupg-agent dirmngr cryptsetup paperkey hopenpgp-tools secure-delete
```

Run the "download_files.sh" script to alleviate entering in all the links:
i.e.
```console
$ cd ~
$ wget https://raw.githubusercontent.com/trustcrypto/trustcrypto.github.io/pages/49-onlykey.rules
$ wget https://raw.githubusercontent.com/drduh/config/master/gpg.conf
```

If you are going to use this hardware to transfer keys to the onlykey (a good idea), then you'll also need the following tools:
https://docs.crp.to/onlykey-agent.html#installation

```console
$ cd ~
$ sudo -s
# apt update && apt upgrade
# apt install python3-pip python3-tk libusb-1.0-0-dev libudev-dev
# exit
$ pip3 install -r onboarding/gpg/requirements.txt
$ sudo -s
# cp 49-onlykey.rules /etc/udev/rules.d/
# udevadm control --reload-rules && udevadm trigger
# reboot
```

# Harden the device

## Work from a temp directory
This is ideal, as all files will get wiped on a reboot.

i.e.
```console
export GNUPGHOME=$(mktemp -d -t gnupg_$(date +%s)
```

However, if you are like me and are booting off a disk you will protect via other means (like in a safe) then we will keep a home workspace

```console
$ export GNUPGHOME=~/gnupg-workspace
$ mkdir -p $GNUPGHOME
```

Either way, secure this folder:
```console
$ sudo -s
# chown <username>:<username> $GNUPGHOME
# chmod 700 $GNUPGHOME
# exit
```

## Harden configuration

We will use drduh's gpg config and then look at all the non-commented lines

```console
$ mv gpg.conf $GNUPGHOME/gpg.conf

$ grep -ve "^#" $GNUPGHOME/gpg.conf
personal-cipher-preferences AES256 AES192 AES
personal-digest-preferences SHA512 SHA384 SHA256
personal-compress-preferences ZLIB BZIP2 ZIP Uncompressed
default-preference-list SHA512 SHA384 SHA256 AES256 AES192 AES ZLIB BZIP2 ZIP Uncompressed
cert-digest-algo SHA512
s2k-digest-algo SHA512
s2k-cipher-algo AES256
charset utf-8
fixed-list-mode
no-comments
no-emit-version
keyid-format 0xlong
list-options show-uid-validity
verify-options show-uid-validity
with-fingerprint
require-cross-certification
no-symkey-cache
use-agent
throw-keyids
```

## Disable networking
Ideally, the device you are using should no longer have access the internet to prevent any malware/keyloggers/etc from sending your gpg info to someone who shouldn't have it.

# Master Key

Drduh has a good explanation
> The first key to generate is the master key. It will be used for certification only: to issue sub-keys that are used for encryption, signing and authentication.

> Important The master key should be kept offline at all times and only accessed to revoke or issue new sub-keys.

> You'll be prompted to enter and verify a passphrase - keep it handy as you'll need it multiple times later.

We will only ever transfer subkeys elsewhere, like to a hardware token (onlykey).



Generate a strong passphrase which could be written down in a secure place or memorized. For example:

```console
$ gpg --gen-random --armor 0 24
ydOmByxmDe63u7gqx2XI9eDgpvJwibNH
```

**IMPORTANT** Save this somewhere in a permanent, secure, offline place. It will be needed to issue new sub-keys after expiration or any other gpg actions using your master key.

We will use ECC curve 25519 as they are supported by onlykey and much more secure than RSA.

There is also no point to setting an expiration to your master key. You could always just extend it, and that's an added headache. Additionally, replacing the master key is a real headache because every person/entity that has used a key derived from your master key would have to get the update.

All the root, master key needs to do is sign (S) and certify (C). Signing isn't even that important, but it allows us to sign a future key which is convenient. You don't need authenticate (A) or encrypt (E) because you'll never use this key for regular operations.

```
$ MYEMAIL="<your primary email address>"
$ gpg --expert --full-generate-key
gpg (GnuPG) 2.3.4; Copyright (C) 2021 Free Software Foundation, Inc.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Please select what kind of key you want:
   (1) RSA and RSA (default)
   (2) DSA and Elgamal
   (3) DSA (sign only)
   (4) RSA (sign only)
   (7) DSA (set your own capabilities)
   (8) RSA (set your own capabilities)
   (9) ECC and ECC
  (10) ECC (sign only)
  (11) ECC (set your own capabilities)
  (13) Existing key
Your selection? 11
Possible actions for a RSA key: Sign Certify Authenticate
Current allowed actions: Sign Certify

   (S) Toggle the sign capability
   (E) Toggle the encrypt capability
   (A) Toggle the authenticate capability
   (Q) Finished

Your selection? s
Possible actions for a RSA key: Sign Certify Authenticate
Current allowed actions: Certify

   (S) Toggle the sign capability
   (E) Toggle the encrypt capability
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
Your selection? 1
Please specify how long the key should be valid.
         0 = key does not expire
      <n>  = key expires in n days
      <n>w = key expires in n weeks
      <n>m = key expires in n months
      <n>y = key expires in n years
Key is valid for? (0) 0
Key does not expire at all
Is this correct? (y/N) y

GnuPG needs to construct a user ID to identify your key.

Real name: John Doe
Email address: jd@example.com
Comment: [Optional - leave blank]
You selected this USER-ID:
    "John Doe <jd@example.com>"

Change (N)ame, (C)omment, (E)mail or (O)kay/(Q)uit? o

We need to generate a lot of random bytes. It is a good idea to perform
some other action (type on the keyboard, move the mouse, utilize the
disks) during the prime generation; this gives the random number
generator a better chance to gain enough entropy.

gpg: /tmp.FLZC0xcM/trustdb.gpg: trustdb created
gpg: key 0xFF3E7D88647EBCDB marked as ultimately trusted
gpg: directory '/tmp.FLZC0xcM/openpgp-revocs.d' created
gpg: revocation certificate stored as '/tmp.FLZC0xcM/openpgp-revocs.d/011CE16BD45B27A55BA8776DFF3E7D88647EBCDB.rev'
public and secret key created and signed.

pub   ed25519/0xFF3E7D88647EBCDB 2022-05-12 [C]
      Key fingerprint = 011C E16B D45B 27A5 5BA8  776D FF3E 7D88 647E BCDB
uid                              John Doe <jd@example.com>
```


Export the key ID as a [variable](https://stackoverflow.com/questions/1158091/defining-a-variable-with-or-without-export/1158231#1158231) (`KEYID`) for use later:

```console
$ export KEYID=0xFF3E7D88647EBCDB
```

# Sign with existing key

(Optional) If you already have a PGP key, you may want to sign the new key with the old one to prove that the new key is controlled by you.

Export your existing key to move it to the working keyring:

```console
$ gpg --export-secret-keys --armor --output /tmp/new.sec
```

Then sign the new key:

```console
$ gpg  --default-key $OLDKEY --sign-key $KEYID
```

# Sub-keys
Edit the master key to add sub-keys:

```console
$ gpg --expert --edit-key $KEYID
gpg (GnuPG) 2.3.4; Copyright (C) 2021 Free Software Foundation, Inc.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Secret key is available.

sec  ed25519/0xFF3E7D88647EBCDB
    created: 2022-05-12  expires: never       usage: SC
    trust: ultimate      validity: ultimate
[ultimate] (1). John Doe <jd@example.com>

gpg>
```

We will add ECC25519 sub keys with an expiration of 1 year. They can be renewed using the offline master key. See [rotating keys](#rotating-keys).

## Signing key
Create a [signing key](https://stackoverflow.com/questions/5421107/can-rsa-be-both-used-as-encryption-and-signature/5432623#5432623) by selecting `addkey` then `(10) ECC (sign only)`:

```console
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
Key expires at Thu May 12 17:31:01 2023 EDT
Is this correct? (y/N) y
Really create? (y/N) y
We need to generate a lot of random bytes. It is a good idea to perform
some other action (type on the keyboard, move the mouse, utilize the
disks) during the prime generation; this gives the random number
generator a better chance to gain enough entropy.

sec  ed25519/0xFF3E7D88647EBCDB
     created: 2022-05-12  expires: never       usage: C
     trust: ultimate      validity: ultimate
ssb  cv25519/A152BC2633C9CC4B
     created: 2022-05-12  expires: never       usage: E
ssb  ed25519/B840CE4D7C47C87D
     created: 2022-05-12  expires: 2023-05-12  usage: S
[ultimate] (1). (1). John Doe <jd@example.com>
```

## Encryption
Next, create an [encryption key](https://www.cs.cornell.edu/courses/cs5430/2015sp/notes/rsa_sign_vs_dec.php) by selecting `(12) ECC (encrypt only)`:

```console
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

sec  ed25519/0xFF3E7D88647EBCDB
     created: 2022-05-12  expires: never       usage: SC
     trust: ultimate      validity: ultimate
ssb  ed25519/B840CE4D7C47C87D
     created: 2022-05-12  expires: 2023-05-12  usage: S
ssb  cv25519/CEA90D62B2180DEF
     created: 2022-05-12  expires: 2023-05-12  usage: E
[ultimate] (1). (1). John Doe <jd@example.com>
```

## Authentication

Finally, create an [authentication key](https://superuser.com/questions/390265/what-is-a-gpg-with-authenticate-capability-used-for).

GPG doesn't provide an authenticate-only key type, so select `(11) ECC (set your own capabilities)` and toggle the required capabilities until the only allowed action is `Authenticate`:

```console
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
Your selection? 1
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

sec  ed25519/0xFF3E7D88647EBCDB
     created: 2022-05-12  expires: never       usage: C
     trust: ultimate      validity: ultimate
ssb  ed25519/0xB840CE4D7C47C87D
     created: 2022-05-12  expires: 2023-05-12  usage: S
ssb  cv25519/0xCEA90D62B2180DEF
     created: 2022-05-12  expires: 2023-05-12  usage: E
ssb  ed25519/0xBCF8D0A788628F22
     created: 2022-05-12  expires: 2023-05-12  usage: A
[ultimate] (1). (1). John Doe <jd@example.com>
```


## Save keys

Finish by saving the keys.

```console
gpg> save
```

## Add extra identities

(Optional) To add additional email addresses or identities, use `adduid`:

```console
gpg> adduid
Real name: John Doe
Email address: john.doe@other.org
Comment:
You selected this USER-ID:
    "John Doe <john.doe@other.org>"

sec  rsa4096/0xFF3E7D88647EBCDB
    created: 2017-10-09  expires: never       usage: C
    trust: ultimate      validity: ultimate
ssb  rsa4096/0xBECFA3C1AE191D15
    created: 2017-10-09  expires: never       usage: S
ssb  rsa4096/0x5912A795E90DD2CF
    created: 2017-10-09  expires: never       usage: E
ssb  rsa4096/0x3F29127E79649A3D
    created: 2017-10-09  expires: never       usage: A
[ultimate] (1). Dr Duh <doc@duh.to>
[ unknown] (2). Dr Duh <DrDuh@other.org>

gpg> trust
sec  rsa4096/0xFF3E7D88647EBCDB
    created: 2017-10-09  expires: never       usage: C
    trust: ultimate      validity: ultimate
ssb  rsa4096/0xBECFA3C1AE191D15
    created: 2017-10-09  expires: never       usage: S
ssb  rsa4096/0x5912A795E90DD2CF
    created: 2017-10-09  expires: never       usage: E
ssb  rsa4096/0x3F29127E79649A3D
    created: 2017-10-09  expires: never       usage: A
[ultimate] (1). Dr Duh <doc@duh.to>
[ unknown] (2). Dr Duh <DrDuh@other.org>

Please decide how far you trust this user to correctly verify other users' keys
(by looking at passports, checking fingerprints from different sources, etc.)

  1 = I don't know or won't say
  2 = I do NOT trust
  3 = I trust marginally
  4 = I trust fully
  5 = I trust ultimately
  m = back to the main menu

Your decision? 5
Do you really want to set this key to ultimate trust? (y/N) y

sec  rsa4096/0xFF3E7D88647EBCDB
    created: 2017-10-09  expires: never       usage: C
    trust: ultimate      validity: ultimate
ssb  rsa4096/0xBECFA3C1AE191D15
    created: 2017-10-09  expires: never       usage: S
ssb  rsa4096/0x5912A795E90DD2CF
    created: 2017-10-09  expires: never       usage: E
ssb  rsa4096/0x3F29127E79649A3D
    created: 2017-10-09  expires: never       usage: A
[ultimate] (1). Dr Duh <doc@duh.to>
[ unknown] (2). Dr Duh <DrDuh@other.org>

gpg> uid 1

sec  rsa4096/0xFF3E7D88647EBCDB
created: 2017-10-09  expires: never       usage: C
    trust: ultimate      validity: ultimate
ssb  rsa4096/0xBECFA3C1AE191D15
    created: 2017-10-09  expires: never       usage: S
ssb  rsa4096/0x5912A795E90DD2CF
    created: 2017-10-09  expires: never       usage: E
ssb  rsa4096/0x3F29127E79649A3D
    created: 2017-10-09  expires: never       usage: A
[ultimate] (1)* Dr Duh <doc@duh.to>
[ unknown] (2). Dr Duh <DrDuh@other.org>

gpg> primary

sec  rsa4096/0xFF3E7D88647EBCDB
created: 2017-10-09  expires: never       usage: C
    trust: ultimate      validity: ultimate
ssb  rsa4096/0xBECFA3C1AE191D15
    created: 2017-10-09  expires: never       usage: S
ssb  rsa4096/0x5912A795E90DD2CF
    created: 2017-10-09  expires: never       usage: E
ssb  rsa4096/0x3F29127E79649A3D
    created: 2017-10-09  expires: never       usage: A
[ultimate] (1)* Dr Duh <doc@duh.to>
[ unknown] (2)  Dr Duh <DrDuh@other.org>

gpg> save
```

By default, the last identity added will be the primary user ID - use `primary` to change that.


# Verify

List the generated secret keys and verify the output:

```console
$ gpg -K
/tmp.FLZC0xcM/pubring.kbx
-------------------------------------------------------------------------
sec   rsa4096/0xFF3E7D88647EBCDB 2017-10-09 [C]
      Key fingerprint = 011C E16B D45B 27A5 5BA8  776D FF3E 7D88 647E BCDB
uid                            Dr Duh <doc@duh.to>
ssb   rsa4096/0xBECFA3C1AE191D15 2017-10-09 [S] [expires: 2018-10-09]
ssb   rsa4096/0x5912A795E90DD2CF 2017-10-09 [E] [expires: 2018-10-09]
ssb   rsa4096/0x3F29127E79649A3D 2017-10-09 [A] [expires: 2018-10-09]
```

Add any additional identities or email addresses you wish to associate using the `adduid` command.

**Tip** Verify with a OpenPGP [key best practice checker](https://riseup.net/en/security/message-security/openpgp/best-practices#openpgp-key-checks):

```console
$ gpg --export $KEYID | hokey lint
```

The output will display any problems with your key in red text. If everything is green, your key passes each of the tests. If it is red, your key has failed one of the tests.

> hokey may warn (orange text) about cross certification for the authentication key. GPG's [Signing Subkey Cross-Certification](https://gnupg.org/faq/subkey-cross-certify.html) documentation has more detail on cross certification, and gpg v2.2.1 notes "subkey <keyid> does not sign and so does not need to be cross-certified". hokey may also indicate a problem (red text) with `Key expiration times: []` on the primary key (see [Note #3](#notes) about not setting an expiry for the primary key).


# Export secret keys

The master key and sub-keys will be encrypted with your passphrase when exported.

Save a copy of your keys:

```console
$ gpg --armor --export-secret-keys $KEYID > $GNUPGHOME/mastersub.asc

$ gpg --armor --export-secret-subkeys $KEYID > $GNUPGHOME/export/subkeys.asc
```

# Revocation certificate

Although we will backup and store the master key in a safe place, it is best practice to never rule out the possibility of losing it or having the backup fail. Without the master key, it will be impossible to renew or rotate subkeys or generate a revocation certificate, the PGP identity will be useless.

Even worse, we cannot advertise this fact in any way to those that are using our keys. It is reasonable to assume this *will* occur at some point and the only remaining way to deprecate orphaned keys is a revocation certificate.

To create the revocation certificate:

``` console
$ gpg --output $GNUPGHOME/revoke-root.asc --gen-revoke $KEYID
```

The `revoke.asc` certificate file should be stored (or printed) in a (secondary) place that allows retrieval in case the main backup fails.

# Backup

Once keys are moved to a hardware token, they cannot be moved again! Create an **encrypted** backup of the keyring on removable media so you can keep it offline in a safe place.

**Tip** The ext2 filesystem (without encryption) can be mounted on both Linux and OpenBSD. Consider using a FAT32/NTFS filesystem for MacOS/Windows compatibility instead.

As an additional backup measure, consider using a [paper copy](https://www.jabberwocky.com/software/paperkey/) of the keys. The [Linux Kernel Maintainer PGP Guide](https://www.kernel.org/doc/html/latest/process/maintainer-pgp-guide.html#back-up-your-master-key-for-disaster-recovery) points out that such printouts *are still password-protected*. It recommends to *write the password on the paper*, since it will be unlikely that you remember the original key password that was used when the paper backup was created. Obviously, you need a really good place to keep such a printout.

**Linux**

Attach another external storage device and check its label:

```console
$ sudo dmesg | tail
mmc0: new high speed SDHC card at address a001
mmcblk0: mmc0:a001 SS16G 14.8 GiB

$ sudo fdisk -l | tail -n 20
Disk /dev/sda: ....

$ sudo mkdir /mnt/usb
$ sudo mount /dev/sda1 /mnt/usb -o uid=<username>,gid=<username>
```

We'll use the relatively weak zip encryption, because I need to transfer the files to a mac, which can't read LUKS.

```console
$ mkdir ~/gpg-backup
$ sudo cp -avi $GNUPGHOME ~/gpg-backup/
$ zip -r -e gpg-backup.zip ~/gpg-backup/
$ cp gpg-backup.zip /mnt/usb/
```

# Upload keys to keyserver

(Optional) Upload the public key to a [public keyserver](https://debian-administration.org/article/451/Submitting_your_GPG_key_to_a_keyserver):

```console
$ gpg --keyserver hkps://keys.openpgp.org --send-key $KEYID
$ gpg --keyserver pgp.mit.edu --send-key $KEYID
$ gpg --gpg --keyserver hkps://keyserver.ubuntu.com:443 --send-key $KEYID
```

Openpgp.org will send you an email that you have to respond to in order to prove you own that email address.

After some time, the public key will propagate to [other](https://pgp.key-server.io/pks/lookup?search=doc%40duh.to&fingerprint=on&op=vindex) [servers](https://pgp.mit.edu/pks/lookup?search=doc%40duh.to&op=index).

# Export public keys

**Important** Without the *public* key, you will not be able to use GPG to encrypt, decrypt, nor sign messages. However, you will still be able to use YubiKey for SSH authentication.

**Linux**

```console
$ gpg --armor --export $KEYID | tee /mnt/usb/gpg-$KEYID-$(date +%F).asc
```

# Export subkeys
## Add subkeys to onlykey

If using an onlykey, please follow the onlykey guide (gpg-add-onlykey.md). Otherwise, export the subkeys so you can import them on another machine

# Export sub keys to file
If not using an onlykey:

```console
$ gpg --export-secret-subkeys --armor $KEYID > ~/subkeychain.asc
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
