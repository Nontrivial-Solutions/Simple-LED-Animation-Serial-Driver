---
title: 00001 Get Command
authors:
  - joe_starr
status: high
---

## Goals

The use case models the receipt of a single serial command.

### Happy Outcome

When the use case completes successfully a command is processed by the serial client.  

### Sad Outcome

When the use case completes unsuccessfully a failure is handled.

## Preconditions

- A serial device is connected.

## Actors

- [Server](../actors/00001_server.md)

## Trigger

A server sends a serial command to the device.

## Scenario

1. The serial device is verified
1. The serial command is processed
1. An error occurs:
    1. Set error state
    1. Report a disconnect error
