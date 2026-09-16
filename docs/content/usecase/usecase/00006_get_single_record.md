---
title: 00006 Get Single Data Record
authors:
  - joe_starr
status: low 
---

## Goals

The use case models the retrieval of a single data record from a Fastrak device.

### Happy Outcome

When the use case completes successfully a data record is retrieved from the Fastrak.  

### Sad Outcome

When the use case completes unsuccessfully a failure is handled.

## Preconditions

A serial device is connected

## Actors

- [User](../actors/00001_user.md)

## Trigger

A user requests a single data record.  

## Scenario

1. The serial device is verified
1. The serial commands for a single data record to be reported
1. The result is received and sent to the user
1. An error occurs:
    1. Set error state
    1. Report a disconnect error
