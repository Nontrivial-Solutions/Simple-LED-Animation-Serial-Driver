---
title: 00002 Set LED state 
authors:
  - joe_starr
status: high
---

## Goals

The use case models the setting of the state of the LED array.  

### Happy Outcome

When the use case completes successfully the connected LED array is in the correct state.  

### Sad Outcome

When the use case completes unsuccessfully a failure is handled.

## Preconditions

- A serial device is connected.
- An LED array is connected.

## Actors

## Trigger

An upstream actor commands a state change.

## Scenario

1. The state data is sent to the LED array.  
1. An error occurs:
    1. Set error state
    1. Report a disconnect error
