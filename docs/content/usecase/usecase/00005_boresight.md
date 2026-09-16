---
title: 00005 Boresight
authors:
  - joe_starr
status: high
---

## Goals

The use case models the zeroing of the Fastrak positioning.

### Happy Outcome

When the use case completes successfully the Fastrak positioning is zeroed

### Sad Outcome

When the use case completes unsuccessfully a failure is handled.

## Preconditions

- A serial device is connected.

## Actors

- [User](../actors/00001_user.md)

## Trigger

A user requests the zeroing of the positioning (boresighting) for a Fastrak device.  

## Scenario

1. The user requests boresighting
1. The serial device is verified
1. The serial commands for boresight are sent to the device
1. An error occurs:
    1. Set error state
    1. Report a disconnect or boresight error
