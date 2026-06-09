(explanation-fde-recovery-key)=

# Full Disk Encryption (FDE) recovery keys

Landscape Server provides a centralized way to request, store, and manage recovery keys for managed instances. This document describes how Landscape Server requests Landscape Client to generate a recovery key via the snapd API.

FDE recovery keys can be generated for target instances that meet the following requirements:

- TPM-backed Full Disk Encryption must be enabled.
- snapd version `2.74` or higher.
- Landscape Client version `26.04` or higher with the `FDERecoveryKeyManager` plugin enabled.

## Overview

The recovery key generation process is handled via Landscape activities. See {ref}`explanation-activities` for details on how activities are delivered to clients.

## Key request (Landscape Server -> Landscape Client)

When an administrator requests a new or replacement recovery key for an instance, Landscape Server creates a `GenerateFDERecoveryKeyRequest` activity. Landscape Server sends a `fde-recovery-key` message to Landscape Client in the following form:

```json
{
  "type": "fde-recovery-key",
  "operation-id": "<ACTIVITY_ID>",
  "action": "generate",
}
```

Field descriptions:

- `operation-id`: Unique identifier of the activity.
- `action`: The operation to perform. Currently `generate` is the only supported value.

## Landscape Client execution

Once Landscape Client receives the `fde-recovery-key` message, it executes the following steps via snapd API calls:

1. Check to see if a `landscape-recovery-key` keyslot exists.
    - If found, Landscape Client prepares to replace the existing keyslot.
    - If not found, Landscape Client prepares to add a new keyslot.
1. Generate the recovery key.
1. Add or replace the `landscape-recovery-key` keyslot using the new recovery key.
1. Store the recovery key temporarily in memory to be included in the response message back to Landscape Server.

```{note}
The recovery key is not saved to disk during this process. If Landscape Client exits before reporting to Server, the recovery key will be lost and the administrator should request a new key.
```

## Key reporting (Landscape Client -> Landscape Server)

Once the execution is complete, Landscape Client sends a `fde-recovery-key` message to Landscape Server in the following form:

```json
{
  "operation-id": "<ACTIVITY_ID>",
  "recovery-key": "<RECOVERY_KEY>",
  "result-text": "<OUTPUT>",
  "successful": true,
}
```

Field descriptions:

- `operation-id`: Unique identifier of the activity.
- `recovery-key`: Recovery key which can be used to unlock the encrypted disk. Can be omitted if the recovery key generation failed.
- `result-text`: If the activity failed, this will have the error message. Otherwise, it will be "Generated new FDE recovery key."
- `successful`: If True, the recovery key generation was successful. Landscape Client uses this to determine if the recovery key in-memory is accurate.

## Landscape Server storage

Once Landscape Server receives the recovery key, it adds the recovery key to the Landscape Server Secrets Storage.

If the computer related to a recovery key is removed from Landscape, the recovery key is also removed from the Secrets Storage.
