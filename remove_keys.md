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
```
