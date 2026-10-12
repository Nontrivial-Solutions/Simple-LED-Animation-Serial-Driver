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

Each command in the serial client is indicated by a case-insensitive letter. Following each command
specifier is an ASCII string containing command specific data. The preferred data delimiter is `:`.
Each command is then terminated with a newline character.

> [!warning]
>
> The command terminator should be included by the client.

#### Commands

##### Set LED Count: `Cc`

###### Format

|   0   |                           1                           |
| :---: | :---------------------------------------------------: |
|  ID   | Decimal ASCII representation of an unsigned long int. |

###### Description

The set state command reads

###### Response

No specific response.

##### Set State: `Ss`

###### Format

|   0   |                           1                           |   2   |                         3                         |   4   |                           5                           |   6   |                           7                           |
| :---: | :---------------------------------------------------: | :---: | :-----------------------------------------------: | :---: | :---------------------------------------------------: | :---: | :---------------------------------------------------: |
|  ID   | Decimal ASCII representation of an unsigned long int. |   :   | Decimal ASCII representation of an unsigned char. |   :   | Decimal ASCII representation of an unsigned long int. |   :   | Decimal ASCII representation of an unsigned long int. |

###### Description

The set state command reads an index of an LED in the array and a color that LED should be.

###### Response

No specific response.

##### Get CRC: `Rr`

###### Format

|   0   |
| :---: |
|  ID   |

###### Description

Request the CRC32 of the current LED array.

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

No specific response.

##### Set Show: `Hh`

###### Format

|   0   |
| :---: |
|  ID   |

###### Description

Command the Arduino to update the LED array.

###### Response

No specific response.

##### Set LED Array Off: `Zz`

###### Format

|   0   |
| :---: |
|  ID   |

###### Description

Command the Arduino to clear the LED array.

###### Response

No specific response.

## Unit Test Description

No unit tests
