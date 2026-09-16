---
title: 00003 Unit Designs
authors:
  - joe_starr
status: accepted
date: 2026-06-18
---

## Context and Problem Statement

Based on [ADR 00001](./00001_file_structure.md) we know the driver will consist of a number of
units, some for serial commands and one for the driver. These units require documentation. This ADR
decides the strategy for documenting units.

## Decision Outcome

A Mixed Full and Code Unit Documentation. Following this decision the units will be documented at
the following levels:

- Commands: Code
- Support: Code
- Fastrak Driver: Full

## Decision Drivers  

- Must be fast to complete
- Must be understandable
- Must assist readers in understanding
- Must be easy to maintain

## Additional Information

We will define as follows:

>[!definition] "Full Unit Documentation"
>
> A complete collection of the following:
>
> - A class diagram
> - A description for each data member
> - Documentation for each data method
>     - A description for the method
>     - A state machine for the method
>     - (Optional) A collection of submachines
>     - (Optional) A sequence diagram
> - Unit test cards for each public method
> - Code context documentation

>[!definition] "Public Unit Documentation"
>
> A complete collection of the following:
>
> - A class diagram
> - A description for each public data member
> - Documentation for each public data method
>     - A description for the method
>     - A state machine for the method
>     - (Optional) A collection of submachines
>     - (Optional) A sequence diagram
> - Unit test cards for each public method
> - Code context documentation
>

>[!definition] "Code Context Documentation"
>
> Inline source code comments for the unit and each of its methods and members.

## Considered Options

- A full unit documentation for each unit
- A public unit documentation for each unit
- A mixed full and public unit documentation
- A mixed full and code unit documentation

### A Full Unit Documentation for Each Unit

- Good, because it gives full context for all units
- Bad, because it is hard and time-consuming to maintain
- Bad, because it is time-consuming to complete

### A Public Unit Documentation for Each Unit

- Good, because it gives interface context for all units
- Bad, because it is hard and time-consuming to maintain
- Bad, because it is time-consuming to complete

### A Mixed Full and Public Unit Documentation

Some components are documented at the `full` level and some at the `public` level.

- Good, because it gives interface context for all units where deemed important
- Bad, because it is time-consuming to maintain since many units aren't used.
- Bad, because it is time-consuming to complete since many units aren't used.

### A Mixed Full and Code Unit Documentation

Some components are documented at the `full` level and some at the `code` level.

- Good, because it gives interface context for all units where deemed important
- Good, because it is efficient to maintain since many units aren't used.
- Good, because it is efficient to complete since many units aren't used.
