---
title: 00001 File Structure
authors:
  - joe_starr
status: accepted
date: 2026-06-18
---

## Context and Problem Statement

The serial commands need to be outlined and stored in a usable way. This ADR chooses how the
commands will be stored.  

## Decision Outcome

The following units:

- Support
- Commands with no response
- Commands with Response

## Decision Drivers  

- Must be easy to understand
- Must be easy to import
- Must be easy to maintain

## Considered Options

- A unit for each command
- A unit for each flavor of command (with/without response) with supporting content inline
- A unit for each flavor of command (with/without response) with supporting content in a separate
    unit

### A Unit for Each Command

Maintain a separate unit for each serial command

- Good, because it matches documentation for the Fastrak
- Bad, because it's very verbose
- Bad, because it is hard to import

### A Unit for Each Flavor of Command (with/Without Response) with Supporting Content Inline

Maintain a unit for the two types of command (with/Without Response). Any supporting content (enum,
dataclasses, etc.) is stored with the command.

- Good, because it is simple
- Good, because it is easy to import
- Bad, because it will create very long files.  

<!-- rumdl-disable MD013 -->
### A Unit for Each Flavor of Command (with/Without Response) with Supporting Content in a Separate Unit
<!-- rumdl-enable MD013 -->

Maintain a unit for the two types of command (with/Without Response). Any supporting content (enum,
dataclasses, etc.) is stored within a support unit.

- Good, because it is simple
- Good, because it is easy to import
- Good, because it is easy to maintain and extend
