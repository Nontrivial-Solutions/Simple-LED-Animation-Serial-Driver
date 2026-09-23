---
title: Simple Arduino Controlled LED Serial Driver
authors:
  - joe_starr
---

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![White Logo image](https://brainmade.org/white-logo.svg){width=10%}](https://brainmade.org)

![hero](./infra/assets/logo.svg)

/// caption
Arduino Mega from `amperka/hardware-drawings` [@amperka_hardware_drawings_2016]
///

## Note to Reader

### What Am I?

This repository contains an Arduino sketch which uses the FastLED library to control a collection
(strip) of NEOPIXEL LED. The repository also contains a Python serial driver for commanding the
Arduino. The python side is primarily designed around controlling the LED array based on feedback
from a [Polhemus Fastrak](https://polhemus.com/all-trackers/fastrak).

Simple installation by pip. You should probably be using uv projects: `uv add SLASD`

### About the Documentation

The following document describes the "rules" and expectation for development. The
["API Reference"](./reference/fastrakSerialDriver/) page contains the technical context descriptions
found in the source files. The ["Use Cases"](./content/usecase/usecase) page contains a collection
of use cases and a use case diagram for the tool. The ["Decisions"](./content/madr/) page contains a
collection of [architectural decision records](https://adr.github.io/madr/) [@Kopp2018] giving
context on why this tool is the way it is.

### Issues

If you discover an issue with this repository or have a question, please feel free to open an issue.
I've included templates for the following issues:

- 🖋️ Spelling and Grammar: Found some language that is incorrect?
- 🤷 Clarity: Found a section that just makes no sense?
- ❓ Question: Do you have a general question?
- 🐞 Bug: Found an error in the code?
- 🚀 Enhancement: Have a suggestion for improving the toolchain?

[:fontawesome-solid-paper-plane: Open Issue!](https://github.com/Nontrivial-Solutions/psychopy-6dof/issues/new/choose){ .md-button }

## 📃 Cite Me

## ⚖️ License

Documentation:
[![License: CC BY-SA 4.0](https://licensebuttons.net/l/by-sa/4.0/80x15.png)](https://creativecommons.org/licenses/by-sa/4.0/)

Code:
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Planning and Administration

### Tasks

Tasks are tracked as GitHub issues.

### Version Control

The toolchain shall be kept under Git versioning. Development shall take place on branches with
`main` on GitHub as a source of truth. GitHub pull requests shall serve as the arbiter for inclusion
on main with the following quality gates:

- Running and passing the unit test suite.
- Running and passing linting and style enforcers.
- Successful generation of documentation.

#### Release Tagging

The project shall be tagged when a new feature or bug fix is merged into main. The tag shall follow
[semantic versioning](https://semver.org) for labels.

```text
vMAJOR.MINOR.PATCH
```

### Project Structure

Files and directories shall be lower case, where capital is not required by a tool, and contain no
`' '`.

```text
📁 .
├── 📁 .github
│   ├── 📁 ISSUE_TEMPLATE
│   ├── 📁 PULL_REQUEST_TEMPLATE
│   ├── 📁 workflows
│   └── 📝 pull_request_template.md
├── 📁 .vscode
│   └── ⚙️ launch.json
├── 📁 docs
│   ├── 📁 contentt
│   │   ├── 📁 madr
│   │   ├── 📁 units
│   │   └── 📁 usecase
│   ├── 📁 infra
│   └── 📖 README.md
├── 📁 arduino_src 
│   └── 🇨 arduino_src.ino
├── 📁 slasd 
│   └── 🐍 __init__.py
├── ⚙️ .editorconfig
├── 🙈 .gitignore
├── 🛠️ .pre-commit-config.yaml
├── ⚙️ .rumdl.toml
├── ❄️ flake.lock
├── ❄️ flake.nix
├── 🛠️ Justfile
├── 📜 LICENSE
├── 📄 mkdocs.yml
├── 🐍 pyproject.toml
└── 🔒 uv.lock
```

### Directories of Interest

- docs: This directory contains the high level documentation for the tool.
- arduino_src: This directory contains the source code of the Arduino side of the tool.
- slasd: This directory contains the source code of the python side of the tool.
- .github: This directory contains the GitHub infrastructure.  
- .vscode: This directory contains the debugger configuration.  

### Define a Unit

A unit shall be a Python module.

### Quality

The tool and its units shall fail-safe, that is the tool and its units can fail, but the failure
must be detectable. A segfault is okay, an off by one error that computes the wrong value is not.

#### Unit Testing

No unit testing in the project only integration testing. See
[ADR00002][./content/madr/00002_testing.md].

#### Integration Testing

The plugin shall have manual integration testing.

### Requirements

#### Use Cases

Requirements are described as a collection of use cases and actors. There are two collections of the
artifacts one for the [client](./content/arduino_src/usecase/) and one for the
[server](./content/python_driver/usecase/usecase/). These are in turn collected into the following
use case diagrams:

##### Client

```mermaid
flowchart LR
  aS["👤  Server"]

  SS(["Set State"])
  RC(["Receive Command"])

  aS --> RC

  RC -. include .->SS
```

##### Server

```mermaid
flowchart LR
  aU["👤 User"]

  SC(["Send Command"])

  aU --> SC
```

##### Architectural Decisions

Architectural decisions [MADR](<https://github.com/adr/madr>) [@Kopp2018] serve as the primary
documentation for architectural decisions.

The following is the order of operations for the proposal of a MADR:

1. Create a branch for a proposal with the name:

    ```text
    proposal-{{short title}}
    ```

1. Create a pull request with this template.
1. In the branch create a Markdown file based on the
    [MADR Template](https://github.com/adr/madr/blob/4.0.0/template/adr-template.md). Name the
    Markdown file:

    ```text
    {{issue# padded to five digits}}-{{title}}
    ```

1. When a decision is made change the status to:
    - "accepted" and pull the branch into main branch
    - "rejected" and pull the branch into main branch

#### Nonfunctional Requirements

##### Colors

Diagrams included in documentation for features (use case and unit descriptions) are expected to use
the [COLORS](https://clrs.cc) color palette.

##### Technologies

###### Languages and Frameworks

- git
- Python
- mermaid.js
- prek
- tombi
- rumdl
- ruff
- uv
- MADR[@Kopp2018]

###### Documentation of Implementation

###### Code Style Guide

Python code shall be formatted with ruff using the included style settings. Markdown files shall be
formatted with ruff using the included style settings. TOML files shall be formatted with tombi
using the included style settings.

## Design and Documentation

### System

#### Block Diagram

```mermaid
flowchart LR
    device["BaseLedAnimator"]
    cwr@{ shape: processes, label: "{{Collection}}<br>Device specific animators" }
    commands@{ shape: processes, label: "{{Collection}}<br>Available Commands" }

    device --> cwr
    device --> commands 
```

#### Class Diagram

```mermaid
classDiagram
    class LedAnimationDevice {
        + init( COMport, baud, timeout, ledCount) 
        + connect() 
        + compNSndState( **kwargs) 
        - sendState( data) 
        - computeState( **kwargs) 
    }

    class FastrakAnimationDevice {
        - computeState( **kwargs) 
    }

    class FastrakParams {
        + FastrakPostion posData
        + int angleToLight
        + int colorR
        + int colorG
        + int colorB
    }


    class SetLedState {
        + init(self, data) 
    }
    
    class SerialCommand {
        <<interface>>
        - str commandId
        - bytearray payload
        + send(ser) 
    }

    SetLedState ..|> SerialCommand

    FastrakAnimationDevice --|> LedAnimationDevice

    FastrakParams --* FastrakAnimationDevice 
    SetLedState --* LedAnimationDevice 

```

#### Unit Designs

Unit designs (and test description) for the client and server units (public members and methods) is
found under their respective documentation sections.
