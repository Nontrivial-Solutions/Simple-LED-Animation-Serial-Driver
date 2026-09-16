---
title: 00008 Poll Data From Device 
authors:
  - joe_starr
status: high
---

## Goals

The use case models the polling of a data stream from a Fastrak.

### Happy Outcome

When the use case completes successfully the Fastrak data is recorded to a buffer.

### Sad Outcome

When the use case completes unsuccessfully a failure is handled.

## Preconditions

- A serial device is connected.

## Actors

- [Time](../actors/00002_time.md)

## Trigger

A time event requests the recording of a data frame from a Fastrak device.  

## Scenario

1. The serial device is verified
1. The serial data is recorded from the device
1. An error occurs:
    1. Set error state
    1. Report a disconnect or recording error
