---
title: 00002 Decide on Testing Strategy
authors:
  - joe_starr
status: accepted
date: 2026-09-18
---

## Context and Problem Statement

Based on [ADR 00001](./00001_copy_fastrak_structure.md) we will be reusing the architecture from the
Fastrak serial driver where reasonable and omitting documentation where reasonable. Since we're also
interfacing with a hardware object (Arduino and LED) our testing situation is complicated.

This ADR decides the scope of testing for the tool.

## Decision Outcome

Due to the difficulty of unit testing components which interface with hardware we will only conduct
integration tests. Test plans will be outlined in individual Markdown files in the
`docs/content/tests` directory.

## Decision Drivers  

No drivers considered.

## Considered Options

No other options considered.
