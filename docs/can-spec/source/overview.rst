Overview
========

Introduction
------------

The CAN (Controller Area Network) driver module provides the communication interface between
the Battery Management System (BMS) and external devices over CAN bus. The module is built on
top of the DCAN hardware controller present on the TMS570/RM48 Hercules microcontroller family
and abstracts hardware-level details into a clean, callback-based API.

The CAN driver handles:

- Periodic and asynchronous message transmission
- Interrupt-driven message reception with queue-based processing
- Signal packing/unpacking with endianness and scaling support
- Multiplexed message handling for variable-content data
- Comprehensive error detection and diagnostic reporting

Features
--------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Feature
     - Description
   * - Protocol
     - CAN 2.0A (11-bit) and CAN 2.0B (29-bit extended) identifiers
   * - Bitrate
     - Up to 1 Mbit/s
   * - Mailboxes
     - 64 hardware message mailboxes (32 TX, 32 RX)
   * - TX Scheduling
     - Deterministic period + phase offset scheduling
   * - RX Processing
     - Interrupt-safe queue-based reception
   * - Endianness
     - Transparent big-endian and little-endian handling
   * - Signal Scaling
     - Automatic factor/offset conversion
   * - Multiplexing
     - Native support for multiplexed CAN messages
   * - Diagnostics
     - CAN timing validation, queue overflow detection
   * - CAN Nodes
     - Dual CAN nodes (CAN1 standard, CAN2 isolated)

Applicable Documents
--------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Reference
     - Title
   * - CAN 2.0B
     - Bosch CAN Specification Version 2.0, Part B
   * - SPNU499C
     - TI Hercules TMS570LS31x/21x Technical Reference Manual — DCAN Chapter
   * - ISO 11898-1
     - Road vehicles — Controller area network (CAN) — Part 1: Data link layer and physical signalling

Terminology
-----------

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Term
     - Definition
   * - BMS
     - Battery Management System
   * - CAN
     - Controller Area Network
   * - DCAN
     - Dual-clock Controller Area Network (TI Hercules IP)
   * - DLC
     - Data Length Code — number of data bytes in a CAN frame (0–8)
   * - IVT
     - Isabellenhutte current/voltage/temperature sensor
   * - IMD
     - Insulation Monitoring Device
   * - Mux
     - Multiplexer — mechanism to send variable content in the same message ID
   * - PEX
     - Port Expander — used for CAN transceiver control
   * - MOL
     - Maximum Operating Limit
   * - MSL
     - Maximum Safety Limit
   * - RSL
     - Recommended Safety Limit
   * - SOC
     - State of Charge
   * - SOE
     - State of Energy
   * - SOF
     - State of Function
   * - SOH
     - State of Health
   * - AFE
     - Analog Front End
