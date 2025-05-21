(reference-legacy-api-gpg)=
# GPG


The methods available here are for GPG key handling.

## GetGPGKeys

Get info about GPG keys.

This method takes an optional argument:

- `names.#`: A list of GPG keys to get info for. If this is not provided, the call will return all keys for the account.

Example call:

```text
?action=GetGPGKeys&names.1=mykey
```

The method returns JSON serialized info on the keys:

```text
[
    {
        "fingerprint": "aa65:abfd:ffa4:327a:6fa0:6bb1:faa1:83c3:534a:91ee",
        "has_secret": false,
        "id": 10,
        "key_id": "FAA183C3534A91EE",
        "name": "mykey"
    },
    {
        "fingerprint": "afd7:2cef:2aa4:b345:0304:0ab4:20ac:3539:5aaf:ffa4",
        "has_secret": true,
        "id": 1,
        "key_id": "20AC35395AAFFFA4",
        "name": "sign-key"
    }
]
```

## ImportGPGKey

Import a GPG key.

- `name`: Name of the GPG key. It must be unique within the account, start with an alphanumeric character and only contain lowercase letters, numbers and `-` or `+` signs.
- `material`: The text representation of the key.

Example of a valid request:

```text
?action=ImportGPGKey&name=my-key
    &material=-----BEGIN PGP PUBLIC KEY BLOCK-----
        Version: GnuPG v1.4.11 (GNU/Linux)
        mQENBE4xHgQBCADESzhTFEYYCOrvxBCnwtdQZa2DNDf/RbgEEOW/XEh3E5j9kUPj
        .....
        Ci8pOnAXPkVXmT5+um1o8b4bzP4BmGbxemmCdPksJxMt6Qq7n88406M6QPaLj/oz
        -----END PGP PUBLIC KEY BLOCK-----
```

The following error may be raised:

- `DuplicateGPGKey`: A key with same name or fingerprint already exists.
- `GPGKeyImportFailed`: Key import failed.
- `MultipleGPGKey`: The material contains multiple keys.
- `Unauthorised`: The user is not authorised to perform the operation.

The method returns a JSON representation of the stored key:

```text
{
    "fingerprint": "a404:34a3:e40c:1add:94fa:31b4:30a7:5431:a2eb:521a",
    "key_id": "30A75431A2EB521A",
    "id": 11,
    "name": "my-key",
    "has_secret": true
}
```

## RemoveGPGKey

Remove a GPG key.

- `name`: Name of the GPG key.

Example of a valid request:

```text
?action=RemoveGPGKey&name=my-key
```

The following error may be raised:

- `UnknownGPGKey`: No GPG key with the specified name exists.
- `GPGKeyInUse`: The GPG key is currently used by a pocket and can’t be removed.

