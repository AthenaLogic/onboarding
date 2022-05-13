# Intro

This guide picks up from gpg-setup.md to add the subkeys to your onlykey. This ensures that the private key data never gets onto your host machines (except the machine used to generate them).

# Configure your onlykey
Please follow the online guide provided by the vendor.

# Add subkeys to onlykey

I assume you will be using slots ECC1 and ECC2, so please change them accordingly if needed.

ECC1 = signing subkey
ECC2 = encryption (aka decryption) subkey

## Extract the raw key bytes
The onlykey-cli expects only the raw 32 bytes of the key (for ed25519 keys), so we have to extract them.

Assuming you followed the steps for onlykey in the beginning of the gpg-setup.md guide...

```console
$ python3 extract_keys.py
```

This creates 3 files containing the raw key data (which is very sensitive!)



## Clean up

We will use secure rm `srm` to ensure the sensitive files are deleted. If you are on a memory-only "live boot" system then you don't really need to worry about this, but it won't hurt.

```console
$ srm -rf $GNUPGHOME/export
```

---

I have had trouble using the onlykey-cli to add keys, so we'll have to use the app.

```console
$ cd $GNUPGHOME
$ mkdir export
```

to set the keyid without having to type it all out
```console
$ KEYID=$(gpg -K | grep "\[S\]" | awk '{split($0, array, " "); print array[2]} | tail -c 19')
$


$ gpg --output private_auth.asc --armor --export-secret-key [hex of auth key]
$ gpg --output private_signing.asc --armor --export-secret-key [hex of sign key]
$ gpg --output private_encrypt.asc --armor --export-secret-key [hex of encryption key]
```

## Ensure onlykey connects

Plug it in and enter the PIN
```console
$ onlykey-cli wink
```

The blue light will flash!

## Transfer subkeys

We won't transfer the root/master key, only the subkeys so we can use them on other machines without actually transferring the private key data.

Make sure you don't overwrite keys you are already using.

```console
$

```
