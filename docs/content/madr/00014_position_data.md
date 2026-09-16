---
title: 00014 Current Position 
authors:
  - joe_starr
status: accepted
date: 2026-08-07
---

## Context and Problem Statement

During integration with the Psychopy side of the chain it was discovered that the current position
must be reported on demand. This MADR decides how that will be handled.

## Decision Outcome

Position is cached during streaming and requested on demand from the Fastrak.

## Decision Drivers  

- Must be fast so to not impact Psychopy timing.
- Must give accurate data.

## Considered Options

### Position Is Requested on Demand from the Fastrak

When a position is needed a single dataframe is requested from the Fastrak.

- Good, because it gives the most accurate positional data.  
- Bad, because it is slow when streaming.  

### Position Is Cached

The result of the last manual request or streaming result is cached by the system.

- Good, because it gives the accurate positional data during streaming.  
- Good, because it is fast during streaming.  
- Bad, because unless manually polling when not streaming the data will be inaccurate.  

### Position Is Cached During Streaming and Requested on Demand from the Fastrak

The position of the Fastrak is cached during streaming and requested when not streaming.

- Good, because it gives the accurate positional data during streaming.  
- Good, because it gives the accurate positional data while not streaming.  
- Good, because it is fast during streaming.  
- Good, because it is fast when not streaming.  
