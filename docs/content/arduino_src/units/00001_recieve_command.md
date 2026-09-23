---
title: Arduino Serial LED Controller 
authors:
  - joe_starr
date: 2026-07-13
---

## Description

This unit describes the functionality of an Arduino serial client. The server controls a collection
of LED. The LED are assumed to be NEOPIXEL and to be in a contiguous strip.

### Serial Interfaces

#### Command Structure

Each command in the serial client is indicated by a case-insensitive letter. Each command is then
terminated with a newline character.

> [!warning]
>
> The command terminator should be included by the client.

#### Commands

##### Set State: `Ss`

The set state command reads a byte array of three tuples from the serial interface. The tuples are
then commanded in order to the LED array.

## Unit Test Description

No unit tests
