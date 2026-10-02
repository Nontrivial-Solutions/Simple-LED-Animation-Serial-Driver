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

##### Set LED Count: `Cc`

###### Format

|   0   |           1            |           2            |
| :---: | :--------------------: | :--------------------: |
|  ID   | Unsigned LED count LSB | Unsigned LED count MSB |

###### Description

The set state command reads

###### Response

No response.

##### Set State: `Ss`

###### Format

|   0   |           1            |           2            |      3       |       4        |       5       |
| :---: | :--------------------: | :--------------------: | :----------: | :------------: | :-----------: |
|  ID   | Unsigned LED index LSB | Unsigned LED index MSB | Unsigned Red | Unsigned Green | Unsigned Blue |

###### Description

The set state command reads an index of an LED in the array and a color that LED should be. The LED
is then commanded into that state.

###### Response

Response is the [CRC32](https://en.wikipedia.org/wiki/Cyclic_redundancy_check) of the current LED
array.

> [!warning]
>
> The CRC32 does not give a guarantee of data integrity. Collisions are possible however collisions
> are unlikely unless intentionally constructed. See
> [Wikipedia on data integrity](https://en.wikipedia.org/wiki/Cyclic_redundancy_check#Data_integrity).

##### Clear LED Array: `Oo`

###### Format

|   0   |
| :---: |
|  ID   |

###### Description

The clear command sets each LED in the array to `#000000`.

###### Response

No response.

## Unit Test Description

No unit tests
