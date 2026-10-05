---
title: 00003 Set LED Count
authors:
  - joe_starr
status: high
---

## Goals

The use case models the setting of the count of LED commendable in the array.  

### Happy Outcome

When the use case completes successfully the number of LED is set.  

### Sad Outcome

When the use case completes unsuccessfully a failure is handled.

## Preconditions

- A serial device is connected.
- An LED array is connected.

## Actors

## Trigger

An upstream actor commands a change to the LED count.

## Scenario

1. The count data is sent to the device.  
1. An error occurs:
    1. Set error state
    1. Report a disconnect error
