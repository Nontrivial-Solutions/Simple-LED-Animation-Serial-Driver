---
title: 00002 Driver Configuration  
authors:
  - joe_starr
status: accepted
date: 2026-06-18
---

## Context and Problem Statement

The driver will need to explicitly set the state of a connected Fastrak device and maintain a copy
of that state locally. Which and how many knobs are presented to the user/calling tool are many and
varied. This ADR decides what options are supported.

## Decision Outcome

Expose nothing more than serial options. This will allow for the system to be implemented quickly
with the tradeoff of flexibility and error detection.

## Decision Drivers  

- Must be flexible for calling systems.  
- Must be easy to implement
- Must be easy to test
- Must be easy to maintain
- Must be simple to detect errors

## Considered Options

- Expose every available option
- Expose a subset of the options
- Expose nothing more than serial options (baudrate, etc.)

### Expose Every Available Option

Expose every configuration option available for the Fastrak.

- Good, because it allows the most flexibility
- Good, because it allows the most opportunity to detect an error on the Fastrak
- Bad, because it's very verbose
- Bad, because it is hard to implement
- Bad, because it is hard to maintain
- Bad, because it is very hard to test

### Expose a Subset of the Options

Expose a subset of the option available for the Fastrak.

- Good, because it allows significant flexibility
- Good, because it allows tailoring of error detection  
- Bad, because it's verbose
- Bad, because it is difficult to implement
- Bad, because it is labor intense to maintain
- Bad, because it is time-consuming to test

### Expose Nothing More than Serial Options (Baudrate, Etc.)

Expose no configuration for the Fastrak only for the serial connection.

- Bad, because it allows no flexibility at runtime
- Bad, because it allows only error detection considered at build time
- Good, because it's simple and fast to implement
- Good, because it is easy maintain
- Good, because it is easy to test
