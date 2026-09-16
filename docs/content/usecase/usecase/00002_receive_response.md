---
title: 00002 Wait for Response 
authors:
  - joe_starr
status: low
---

## Goals

The use case models a wait for a response from a Fastrak.  

### Happy Outcome

When the use case completes successfully a response is received from the Fastrak.

### Sad Outcome

When the use case completes unsuccessfully a failure is handled.

## Preconditions

- A serial device is connected.

## Actors

- [User](../actors/00001_user.md)

## Trigger

A user waits for a response from the Fastrak.  

## Scenario

1. The serial device is verified
1. Wait for the Fastrak to send a response.  
1. Report response
1. An error occurs:
    1. Set error state
    1. Report a disconnect error
