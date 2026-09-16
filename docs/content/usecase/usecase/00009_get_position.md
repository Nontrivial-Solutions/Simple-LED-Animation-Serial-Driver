---
title: 00009 Get Current Position 
authors:
  - joe_starr
status: high
---

## Goals

The use case models the retrieval of instantanious positional data from the Fastrak.  

### Happy Outcome

When the use case completes successfully the current position of the Fastrak is reported.

### Sad Outcome

When the use case completes unsuccessfully a failure is handled.

## Preconditions

- A serial device is connected.

## Actors

- [User](../actors/00001_user.md)
- [Time](../actors/00002_time.md)

## Trigger

An actor requests the current position from a Fastrak device.  

## Scenario

1. The serial device is verified
1. The position data is obtained from the device
1. An error occurs:
    1. Set error state
    1. Report a disconnect or recording error
