---
title: Fastrak Device 
authors:
  - joe_starr
date: 2026-07-13
---

## Description

This unit describes the functionality of the Fastrak Device connection class. The class maintains a
serial connection to a physical Fastrak to which it issues commands.

### Members

#### Data

A `bytearray` of data from a data stream session.

### Interfaces

#### Constructor and Valid Class Function

The constructor method takes in a collection of data:

- Serial port name: A string representing which serial port to use to connect to the Fastrak.  
- Baudrate: A baudrate to use for the serial connection.
- Serial timeout: How long to wait for the serial connection.
- Station ID: The ID of the station (peripheral slot) to use on the Fastrak.
- Run setup flag: Indicates if the constructor should also set up the Fastrak.
- Binary or ASCII output flag: Indicates if the output should be ASCII or Binary.
- Polling Rate: The rate to poll the Fastrak in streaming mode.

> [!note]
>
> The position flow only works in binary mode.

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

#### Enable Stream

Enable the streaming of data from a Fastrak device.

##### State Machine

```mermaid
stateDiagram-v2
    state "Command Fastrak into continuous mode" as sc
    state "Create polling thread" as cpt 
    state "Set streaming on" as ss 
    state is_connected <<choice>>
    state is_running <<choice>>
    [*] --> is_connected
    is_connected --> [*]: Is not connected
    is_connected --> is_running : Is connected
    is_running --> [*]: Is streaming 
    is_running --> sc: Is not streaming 
    sc --> cpt
    cpt --> ss 
    ss --> [*]

```

#### Disable Stream

Disable the streaming of data from a Fastrak device.

##### State Machine

```mermaid
stateDiagram-v2
    state "Command Fastrak out of continuous mode" as sc
    state "Close polling thread" as cpt 
    state "Set streaming off" as ss 
    state is_connected <<choice>>
    state is_running <<choice>>
    [*] --> is_connected
    is_connected --> [*]: Is not connected
    is_connected --> is_running : Is connected
    is_running --> sc: Is streaming 
    is_running --> [*]: Is not streaming 
    sc --> cpt
    cpt --> ss 
    ss --> [*]

```

#### Read Line

Request a single data entry from the Fastrak.  

##### State Machine

```mermaid
stateDiagram-v2
    state "Command Fastrak to supply a data record" as sc
    state "Get response" as ss 
    state is_connected <<choice>>
    state is_running <<choice>>
    [*] --> is_connected
    is_connected --> [*]: Is not connected
    is_connected --> is_running : Is connected
    is_running --> sc: Is streaming 
    is_running --> [*]: Is not streaming 
    sc --> ss
    ss --> [*]

```

#### Boresight

Zero the Fastrak.  

##### State Machine

```mermaid
stateDiagram-v2
    state "Command Fastrak to unboresight" as cfu 
    state "Command Fastrak to boresight" as sc
    state is_connected <<choice>>
    state is_running <<choice>>
    [*] --> is_connected
    is_connected --> [*]: Is not connected
    is_connected --> is_running : Is connected
    is_running --> cfu: Is streaming 
    is_running --> [*]: Is not streaming 
    cfu --> sc
    sc --> [*]

```

#### Basic Setup

Run the basic setup for the Fastrak. This sets an active station and output data format.

##### State Machine

```mermaid
stateDiagram-v2
    state "Command Fastrak stations off" as sc
    state "Command Fastrak configured station on" as cfcs
    state "Command Fastrak into binary mode" as cfibm
    state "Command Fastrak output format" as cfof
    state is_connected <<choice>>
    [*] --> is_connected
    is_connected --> [*]: Is connected
    is_connected --> sc: Is not connected 
    sc --> cfcs
    cfcs --> cfibm
    cfibm --> cfof
    cfof --> [*]

```

#### Last Position

Collect the last known position from the Fastrak. If there is no position then report `None`.

##### State Machine

```mermaid
stateDiagram-v2
    state "Read data from Fastrak" as rdff 
    state "Parse packet" as pp 
    state "Get position from polling thread" as gpfpt 
    state is_connected <<choice>>
    state is_running <<choice>>
    [*] --> is_connected
    is_connected --> [*]: Is not connected
    is_connected --> is_running : Is connected
    is_running --> gpfpt: Is streaming 
    is_running --> rdff: Is not streaming 
    rdff --> pp 
    pp --> [*]
    gpfpt --> [*]
```

#### Clear Data Buffer

Clears the streaming data buffer for the Fastrak object.

##### State Machine

```mermaid
stateDiagram-v2
    state "Empty streaming buffer" as esb
    state is_connected <<choice>>
    state is_running <<choice>>
    [*] --> is_connected
    is_connected --> [*]: Is not connected
    is_connected --> is_running : Is connected
    is_running --> [*]: Is streaming 
    is_running --> esb: Is not streaming 
    esb --> [*]

```

## Unit Test Description

### Constructor

#### Positive Tests

> [!test-card] "Initialized component[](){#TestDevice_ID_001}"
>
> Data is passed to the constructor and stored in the private data.
>
> **Inputs:**
> 
> Each argument and all combinations of optional arguments.
>
> **Expected Output:**
>
> Positive response.

#### Negative Tests

No tests for the constructor.

### Connect

#### Positive Tests

> [!test-card] "Device Connected[](){#TestDevice_ID_002}"
>
> A serial device is already connected to an instance of the class. The connect method is called.
>
> **Inputs:**
>
> An instance of the class with a mocked serial device connected.
>
> **Expected Output:**
>
> No response.
>

> [!test-card] "Device Not Connected[](){#TestDevice_ID_003}"
>
> A serial device is not connected to an instance of the class. The connect method is called.
>
> **Inputs:**
>
> A serial mocked device available.
>
> **Expected Output:**
>
> A device is connected.
>

#### Negative Tests

No tests for the connect method.

### Enable Stream

#### Positive Tests

> [!test-card] "A stream is requested[](){#TestDevice_ID_004}"
>
> A stream is requested to start.  
>
> **Inputs:**
>
> - A mocked serial device is connected.
> - A stream is not already running.
>
> **Expected Output:**
>
> The method returns successfully, and a stream is running.
>

> [!test-card] "A stream is running[](){#TestDevice_ID_005}"
>
> A stream is requested to start, but the device is already streaming.  
>
> **Inputs:**
>
> - The mocked serial device is connected.
> - A stream is running.
>
> **Expected Output:**
>
> No response is given.

> [!test-card] "A stream is completed and restarted[](){#TestDevice_ID_025}"
>
> A stream is requested to start after a stream has previously completed.  
>
> **Inputs:**
>
> - A mocked serial device is connected.
> - A stream has previously run.
> - A stream is not already running.
>
> **Expected Output:**
>
> The method returns successfully, and a stream is running.
>

#### Negative Tests

> [!test-card] "A device is not connected[](){#TestDevice_ID_006}"
>
> A stream is requested to start, but no serial device is connected.  
>
> **Inputs:**
>
> - The serial device is not connected.
>
> **Expected Output:**
>
> A disconnected exception is raised.
>

### Disable Stream

#### Positive Tests

> [!test-card] "A stream is requested to close[](){#TestDevice_ID_007}"
>
> A stream is requested to stop.  
>
> **Inputs:**
>
> - A mocked serial device is connected.
> - A stream is running.
>
> **Expected Output:**
>
> The method returns successfully, and a stream is closed and marked not running.
>

#### Negative Tests

> [!test-card] "No stream is running[](){#TestDevice_ID_008}"
>
> A stream is requested to stop, but the device is not streaming.  
>
> **Inputs:**
>
> - The mocked serial device is connected.
> - A stream is not running.
>
> **Expected Output:**
>
> A not running exception is raised.
>

### Read Line

#### Positive Tests

> [!test-card] "A single data frame is requested[](){#TestDevice_ID_009}"
>
> A single data frame is requested from the Fastrak.  
>
> **Inputs:**
>
> - A mocked serial device is connected.
> - A stream is not running
>
> **Expected Output:**
>
> The device responds with a data frame.  
>

#### Negative Tests

> [!test-card] "A single data frame is requested[](){#TestDevice_ID_010}"
>
> A single data frame is requested from the Fastrak.  
>
> **Inputs:**
>
> - A mocked serial device is connected.
> - A stream is running
>
> **Expected Output:**
>
> The device responds with an exception.  
>

> [!test-card] "A device is not connected[](){#TestDevice_ID_011}"
>
> A data frame is requested, but no serial device is connected.  
>
> **Inputs:**
>
> - The serial device is not connected.
>
> **Expected Output:**
>
> A disconnected exception is raised.
>

### Boresight

#### Positive Tests

> [!test-card] "The boresight of a device is requested[](){#TestDevice_ID_012}"
>
> The device is requested to boresight.  
>
> **Inputs:**
>
> - A mocked serial device is connected.
> - A stream is not running.
>
> **Expected Output:**
>
> No response.  
>

#### Negative Tests

> [!test-card] "The boresight of a device is requested[](){#TestDevice_ID_013}"
>
> The device is requested to boresight.  
>
> **Inputs:**
>
> - A mocked serial device is connected.
> - A stream is running.
>
> **Expected Output:**
>
> An exception is raised.
>

> [!test-card] "A device is not connected[](){#TestDevice_ID_014}"
>
> The device is requested to boresight, but no serial device is connected.  
>
> **Inputs:**
>
> - The serial device is not connected.
>
> **Expected Output:**
>
> A disconnected exception is raised.
>

### Basic Setup

#### Positive Tests

> [!test-card] "Command the device to basic setup state[](){#TestDevice_ID_015}"
>
> The device is commanded into its normal operating state.  
>
> **Inputs:**
>
> - A mocked serial device is connected.
>
> **Expected Output:**
>
> No response.  
>

#### Negative Tests

> [!test-card] "A device is not connected[](){#TestDevice_ID_016}"
>
> The device is commanded into its normal operating state, but no serial device is connected.  
>
> **Inputs:**
>
> - The serial device is not connected.
>
> **Expected Output:**
>
> A disconnected exception is raised.
>

> [!test-card] "Command the device to basic setup state, but stream is
> running[](){#TestDevice_ID_017}"
>
> The device is commanded into its normal operating state, but a stream is running.  
>
> **Inputs:**
>
> - A mocked serial device is connected.
> - A stream is running.
>
> **Expected Output:**
>
> A streaming exception is raised.
>

### Last Position

#### Positive Tests

> [!test-card] "Last position while streaming[](){#TestDevice_ID_018}"
>
> Start streaming then retrieve the last streaming position.
>
> **Inputs:**
>
> - A mocked serial device is connected.
>
> **Expected Output:**
>
> Correct last position reported.  
>

> [!test-card] "Last position while not streaming[](){#TestDevice_ID_019}"
>
> Retrieve the current position from the Fastrak.
>
> **Inputs:**
>
> - A mocked serial device is connected.
>
> **Expected Output:**
>
> Correct last position reported.  
>

#### Negative Tests

> [!test-card] "A device is not connected[](){#TestDevice_ID_020}"
>
> The last position is requested but the serial device is not connected.  
>
> **Inputs:**
>
> - The serial device is not connected.
>
> **Expected Output:**
>
> A disconnected exception is raised.
>

> [!test-card] "The driver is in ASCII mode[](){#TestDevice_ID_021}"
>
> The last position is requested but the driver is in ASCII mode.  
>
> **Inputs:**
>
> - The mock serial device is connected.
>
> **Expected Output:**
>
> An exception is raised.
>
### Clear Data Buffer

#### Positive Tests

> [!test-card] "Empty Buffer [](){#TestDevice_ID_022}"
>
> Request the Fastrak object empty the data buffer.
>
> **Inputs:**
>
> - A mocked serial device is connected.
> - The buffer is:
>           - filled
>           - unfilled
>
> **Expected Output:**
>
> Empty buffer is reported.  
>

#### Negative Tests

> [!test-card] "A device is not connected[](){#TestDevice_ID_023}"
>
> The buffer is requested to be emptied but the serial device is not connected.  
>
> **Inputs:**
>
> - The serial device is not connected.
>
> **Expected Output:**
>
> A disconnected exception is raised.
>

> [!test-card] "The device is streaming[](){#TestDevice_ID_024}"
>
> The last position is requested but the serial device is not connected.  
>
> **Inputs:**
>
> - The mock serial device is connected.
> - The device is streaming.
>
> **Expected Output:**
>
> An exception is raised.
>
