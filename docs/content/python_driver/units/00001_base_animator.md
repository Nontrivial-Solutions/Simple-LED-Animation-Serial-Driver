---
title: Base LED Array Device 
authors:
  - joe_starr
date: 2026-07-13
---

## Description

This unit describes the functionality of the base LED animation serial handling class. The class
maintains a serial connection to a physical device to which it issues commands.

### Members

### Public Interfaces

#### Constructor and Valid Constructor

The constructor method takes in a collection of data:

- Serial port name: A string representing which serial port to use to connect to the Fastrak.  
- Baudrate: A baudrate to use for the serial connection.
- Serial timeout: How long to wait for the serial connection.
- LED count: Indicates the number of LED to control.  
- Run setup flag: Indicates if the constructor should also set up the Fastrak.
- LED Color: Indicates what color the active LED should be set to.

##### State Machine

```mermaid
stateDiagram-v2
    state "Initalize members" as im
    state "Run basic setup" as rbs 
    state do_setup <<choice>>
    [*] --> im
    im --> do_setup
    do_setup --> [*]: Setup not requested
    do_setup --> rbs: Setup requested
    rbs --> [*]

```

#### Connect

Attempt to connect the configured serial device.

##### State Machine

```mermaid
stateDiagram-v2
    state "Connect device" as cd 
    state is_connected <<choice>>
    [*] --> is_connected
    is_connected --> [*]: Is connected
    is_connected --> cd: Is not connected
    cd --> [*]

```

#### Compute and Send State

Compute the state of the LED array and send updates to the Arduino.

##### State Machine

```mermaid
stateDiagram-v2
    state "Compute State" as cs 
    state "Send State Updates" as ssu
    state "Fail" as f
    state is_connected <<choice>>
    [*] --> cs 
    cs --> ssu
    ssu --> is_connected
    is_connected --> [*]: State is correct
    is_connected --> f: State is incorrect
    f --> [*]

```

#### Set LED Array Off

Set the state of the LED array to off.  

##### State Machine

```mermaid
stateDiagram-v2
    state "Command state off" as cs 
    [*] --> cs 
    cs --> [*]

```

## Unit Test Description

No unit tests
