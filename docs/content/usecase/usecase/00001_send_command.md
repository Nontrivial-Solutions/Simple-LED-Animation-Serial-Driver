---
title: 00001 Send Command
authors:
  - joe_starr
status: high
---

## Goals

The use case models the sending of a single command to a Fastrak.  

### Happy Outcome

When the use case completes successfully a command is issued to the Fastrak.  

### Sad Outcome

When the use case completes unsuccessfully a failure is handled.

## Preconditions

- A serial device is connected.

## Actors

- [User](../actors/00001_user.md)

## Trigger

A user sends a serial command to the device.

## Scenario

1. The serial device is verified
1. The serial command is sent
1. An error occurs:
    1. Set error state
    1. Report a disconnect error
