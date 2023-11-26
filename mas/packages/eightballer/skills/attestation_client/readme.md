# Attestation Client Skill

## Description

The skill enables abci services reply to requests from the attestation station Autonolas Service.

The skill is effectively a subclass of the Tendermint ABCI.

It is responsible for handling requests from the attestation station and responding to them.

Our additional functionality is to handle the attestation station's to return the attestation station's public key, along the host and port of the attestation station Tendermint RPC server.

This allows participanting Autonolas nodes to enables the attestation station to connect and attest to their availbility.

