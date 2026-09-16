---
title: 00010 Clear Data Buffer 
authors:
  - joe_starr
status: high
---

## Goals

The use case models the clearing of the streaming data buffer for reuse.  

### Happy Outcome

When the use case completes successfully the streaming data buffer is emptied.

### Sad Outcome

When the use case completes unsuccessfully a failure is handled.

## Preconditions

- A serial device is connected.

## Actors

- [User](../actors/00001_user.md)

## Trigger

A user request the streaming buffer to be emptied.  

## Scenario

1. The serial device is verified
1. The device is verified not streaming
1. The streaming buffer is emptied
1. An error occurs:
    1. Set error state
    1. Report a disconnect or recording error
