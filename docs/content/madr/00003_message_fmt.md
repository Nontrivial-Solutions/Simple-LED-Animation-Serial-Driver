---
title: 00003 Decide on the Serial Message Format
authors:
  - joe_starr
status: accepted
date: 2026-10-12
---

## Context and Problem Statement

Serial messages need to pass between the PC and a hardware device (Arduino). The messages will
travel over a serial connection as a byte stream.

## Decision Outcome

A collection of commands with form similar to the Fastrak with payload of a C strings.

Additionally, every message will receive some sort of `Ack`.

> [!note]
>
> I did the "bad thing" on this ADR. I made choices before making the ADR. Versions 0.x.x and 1.x.x
> of the software have poorly designed messaging systems. This ADR really documents the ideas that
> changed between 0.x.x, 1.x.x, and 2.x.x.

## Decision Drivers  

- Must be easy to understand the flow.
- Must be easy to debug.
- Must be fast to transmit.
- Must be fast to detect possible errors.

## Considered Options

### Format

- A command with a full LED array byte stream
- A collection of commands with form similar to the Fastrak. Payload is bytes.
- A collection of commands with form similar to the Fastrak. Payload is C strings.

#### A Command with a Full LED Array Byte Stream

- Bad, because it's hard to understand the flow.  
- Bad, because it's hard to debug.  
- Good, because it's fast for a full LED page.
- Good, because it's easy to include and compute message integrity check.

#### A Collection of Commands with Form Similar to the Fastrak. Payload Is Bytes

- Good, because it's easy to understand the flow.  
- Good, because it's easy to debug.  
- Bad, because it's slow for a full LED page.
- Bad, because it's hard to include and compute message integrity check.

#### A Collection of Commands with Form Similar to the Fastrak. Payload Is C Strings

- Good, because it's easy to understand the flow.  
- Good, because it's easy to debug.  
- Bad, because it's slow for a full LED page.
- Bad, because it's hard to include and compute message integrity check.

### Response Format

- Acknowledge every message.
- Acknowledge some messages.
- Don't acknowledge messages.

#### Acknowledge Every Message

- Good, because it ensures messages aren't dropped.
- Bad, because it is slow.  

#### Acknowledge Some Messages

- Bad, because it ensures only some messages aren't dropped.
- Bad, because it makes the shape of messages less consistent.  
- Bad, because it is slow.  

#### Don't Acknowledge Messages

- Bad, because it ensures only no message integrity.
- Good, because it is fast.  
