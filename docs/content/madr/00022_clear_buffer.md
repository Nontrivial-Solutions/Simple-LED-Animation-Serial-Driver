---
title: 00022 Clear Buffer 
authors:
  - joe_starr
status: accepted
date: 2026-08-12
---

## Context and Problem Statement

When running in Psychopy an "experiment" reuses the exact object between routines. There is no clean
way to clear the data buffer between runs. This ADR decides how to clear the data buffer.

## Decision Outcome

Add a clear buffer interface that blocks.

> [!note]
> 
> No other options were considered.

## Decision Drivers  

- Must be threadsafe.

## Considered Options

### Add a Clear Buffer Interface That Blocks

The clear buffer Interface will block until a thread can be killed, and a buffer cleared.

- Good, because it gives a threadsafe option.
