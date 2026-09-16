---
title: 00004 End Recording
authors:
  - joe_starr
status: high
---

## Goals

The use case models the end of a recording session for a Fastrak device.

### Happy Outcome

When the use case completes successfully a threadsafe recording is terminated.  

### Sad Outcome

When the use case completes unsuccessfully a failure is handled.

## Preconditions

- A serial device is connected.

## Actors

- [User](../actors/00001_user.md)

## Trigger

A user requests the end of a recording

## Scenario

1. The recording is requested to start
1. An error occurs:
    1. Set error state
    1. Report a recording error
