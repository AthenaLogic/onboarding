#!/usr/bin/python
import os
import sys
import pgpy
from pathlib import Path
import getpass
from Crypto.Util.number import long_to_bytes

# This python script can parse the private keys out of OpenPGP keys (ed25519 or RSA).
# Replace the passphrase with your OpenPGP passphrase.
rootkey_passphrase = getpass.getpass("root GPG passphrase: ")
# If you use a different passphrase for subkeys (such as rootless subkeys) replace
# the passphrase below with your OpenPGP subkey passphrase
subkey_passphrase = rootkey_passphrase # "example subkey passphrase"

# Or if you would prefer, import key as a file like this
gpghomedir = os.environ['GNUPGHOME']
if gpghomedir[-1] == "/":
    gpghomedir = gpghomedir[:-1]

(rootkey, _) = pgpy.PGPKey.from_file(gpghomedir + '/mastersub.asc')

# Run the script and raw keys will be displayed. Only run this on a
# secure trusted system.

assert rootkey.is_protected
assert rootkey.is_unlocked is False

try:
    print('Load these raw key values to OnlyKey by using the OnlyKey App --> Advanced -> Add Private Key')
    with rootkey.unlock(rootkey_passphrase):
        # rootkey is now unlocked
        assert rootkey.is_unlocked
        print('rootkey is now unlocked')
        print('rootkey type %s', rootkey._key._pkalg)
        if 'RSA' in rootkey._key._pkalg._name_:
            print('rootkey value:')
            #Parse rsa pgp key
            primary_keyp = long_to_bytes(rootkey._key.keymaterial.p)
            primary_keyq = long_to_bytes(rootkey._key.keymaterial.q)
            print(("".join(["%02x" % c for c in primary_keyp])) + ("".join(["%02x" % c for c in primary_keyq])))
            print('rootkey size =', (len(primary_keyp)+len(primary_keyq))*8, 'bits')
            print('subkey values:')
            for subkey, value in rootkey._children.items():
                print('subkey id', subkey)
                sub_keyp = long_to_bytes(value._key.keymaterial.p)
                sub_keyq = long_to_bytes(value._key.keymaterial.q)
                print('subkey value')
                subkey_hexbytes = ""
                subkey_hexbytes = "".join(["%02x" % c for c in sub_keyp]) + "".join(["%02x" % c for c in sub_keyq])
                print(subkey_hexbytes)
                print('subkey size =', (len(primary_keyp)+len(primary_keyq))*8, 'bits')

                keypath = Path(gpghomedir+'/'+subkey+'-raw.hex')
                keypath.write(subkey_hexbytes)
                print("Saved key to", keypath)
        else:
            print('rootkey value:')
            #Parse ed25519 pgp key
            primary_key = long_to_bytes(rootkey._key.keymaterial.s)
            print("".join(["%02x" % c for c in primary_key]))
            print('subkey values:')
            for subkey, value in rootkey._children.items():
                print('subkey id', subkey)
                sub_key = long_to_bytes(value._key.keymaterial.s)
                print('subkey value')
                subkey_hexbytes = "".join(["%02x" % c for c in sub_key])
                print(subkey_hexbytes)

                keypath = Path(gpghomedir+'/'+subkey+'-raw.hex')
                keypath.write(subkey_hexbytes)
                print("Saved key to", keypath)

except:
    print('Unlocking root key failed, attempting rootless subkey unlock.')
    try:
        print('subkey key values:')
        for subkey, value in rootkey._children.items():
            assert value.is_protected
            assert value.is_unlocked is False
            with value.unlock(subkey_passphrase):
                # subkey is now unlocked
                assert value.is_unlocked
                print('subkey is now unlocked')
                print('subkey id', subkey)
                subkey_hexbytes = ""
                if 'RSA' in subkey._key._pkalg._name_:
                    sub_keyp = long_to_bytes(value._key.keymaterial.p)
                    sub_keyq = long_to_bytes(value._key.keymaterial.q)
                    print('subkey value')
                    subkey_hexbytes = "".join(["%02x" % c for c in sub_keyp]) + "".join(["%02x" % c for c in sub_keyq])
                else:
                    sub_key = long_to_bytes(value._key.keymaterial.s)
                    print('subkey value')
                    subkey_hexbytes = "".join(["%02x" % c for c in sub_key])

                keypath = Path(gpghomedir+'/'+subkey+'-raw.hex')
                keypath.write(subkey_hexbytes)
                print("Saved key to", keypath)
            # subkey is no longer unlocked
            assert value.is_unlocked is False

            print()

    except:
        print('Unlocking failed')

# rootkey is no longer unlocked
assert rootkey.is_unlocked is False
