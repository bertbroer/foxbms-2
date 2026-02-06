Architecture
============

Module Block Diagram
--------------------

The CAN driver module follows a layered architecture that separates hardware abstraction,
core driver logic, configuration, and application-level callback handlers.

.. code-block:: text

   ┌─────────────────────────────────────────────────────────────────────┐
   │                        Application Layer                           │
   │   ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐    │
   │   │  TX Cyclic    │  │  TX Async     │  │  RX Callbacks        │    │
   │   │  Callbacks    │  │  Callbacks    │  │                      │    │
   │   │  (14 msgs)    │  │  (5 msgs)     │  │  (15 msgs)           │    │
   │   └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘    │
   │          │                 │                      │                │
   │   ┌──────┴─────────────────┴──────────────────────┴───────────┐    │
   │   │                    CAN Helper Functions                    │    │
   │   │          Signal packing / unpacking / conversion           │    │
   │   └──────────────────────────┬────────────────────────────────┘    │
   ├──────────────────────────────┼────────────────────────────────────┤
   │                        Core Driver Layer                          │
   │   ┌──────────────────────────┴────────────────────────────────┐    │
   │   │                     CAN Driver (can.c)                     │    │
   │   │  ┌────────────┐ ┌────────────┐ ┌───────────┐ ┌────────┐  │    │
   │   │  │ Initialize  │ │ Periodic   │ │ RX Buffer │ │ Timing │  │    │
   │   │  │             │ │ Transmit   │ │ Reader    │ │ Check  │  │    │
   │   │  └────────────┘ └─────┬──────┘ └─────┬─────┘ └────────┘  │    │
   │   └────────────────────────┼──────────────┼───────────────────┘    │
   │                            │              │                        │
   │   ┌────────────────────────┼──────────────┼───────────────────┐    │
   │   │              Configuration (can_cfg.c/h)                   │    │
   │   │  ┌─────────────┐ ┌────┴───────┐ ┌────┴──────┐            │    │
   │   │  │ Node Config  │ │ TX Message │ │ RX Message│            │    │
   │   │  │ CAN1, CAN2   │ │ Tables     │ │ Tables    │            │    │
   │   │  └─────────────┘ └────────────┘ └───────────┘            │    │
   │   └───────────────────────────────────────────────────────────┘    │
   ├───────────────────────────────────────────────────────────────────┤
   │                       Hardware Abstraction                        │
   │   ┌───────────────────────────────────────────────────────────┐    │
   │   │              HAL (HL_can.h) + DCAN Registers               │    │
   │   │  ┌──────────┐  ┌──────────┐  ┌───────────┐  ┌─────────┐  │    │
   │   │  │ canInit() │  │canGetData│  │IF1/IF2 Reg│  │Mailboxes│  │    │
   │   │  └──────────┘  └──────────┘  └───────────┘  └─────────┘  │    │
   │   └───────────────────────────────────────────────────────────┘    │
   │   ┌───────────────────────────────────────────────────────────┐    │
   │   │           CAN Transceiver (via Port Expander)              │    │
   │   └───────────────────────────────────────────────────────────┘    │
   └─────────────────────────────────────────────────────────────────────┘

Hardware Mailbox Layout
-----------------------

The DCAN controller provides 64 message mailboxes partitioned as follows:

.. list-table:: Mailbox Allocation
   :widths: 25 25 50
   :header-rows: 1

   * - Mailbox Range
     - Direction
     - Purpose
   * - 1 – 32
     - TX
     - Message transmission (searched round-robin for free box)
   * - 33 – 60
     - RX
     - Standard 11-bit identifier reception
   * - 61 – 64
     - RX
     - Extended 29-bit identifier reception

.. note::

   Mailbox 42 is also reconfigured at initialization for extended identifier support on
   certain CAN nodes.

CAN Node Configuration
----------------------

The system provides two CAN bus interfaces:

.. list-table::
   :widths: 15 20 25 40
   :header-rows: 1

   * - Node
     - Symbol
     - Register Base
     - Description
   * - CAN1
     - ``CAN_NODE_1``
     - ``canREG1``
     - Primary CAN bus — carries BMS state, sensor data, debug
   * - CAN2
     - ``CAN_NODE_2``
     - ``canREG2``
     - Isolated CAN bus — galvanically isolated interface

Default node assignments for message categories:

.. code-block:: c

   #define CAN_NODE_DEBUG_MESSAGE        (CAN_NODE_1)
   #define CAN_NODE_IMD                  (CAN_NODE_1)
   #define CAN_NODE_CURRENT_SENSOR       (CAN_NODE_1)

Data Flow
---------

Transmission Path
^^^^^^^^^^^^^^^^^

.. code-block:: text

   Database Tables ──► TX Callback ──► CAN Helper (pack) ──► CAN_DataSend()
        │                                                         │
        │                                                    ┌────┴────┐
        │                                                    │ Mailbox │
        │                                                    │  free?  │
        │                                                    └─┬────┬──┘
        │                                                  Yes │    │ No
        │                                                      ▼    ▼
        │                                                   HW TX  Queue
        │                                                          │
        └──────────────────────────────────────── Retry on next ◄──┘
                                                  periodic call

Reception Path
^^^^^^^^^^^^^^

.. code-block:: text

   DCAN HW Interrupt ──► canMessageNotification()
                              │
                              ▼
                         CAN_RxInterrupt()
                              │
                              ▼
                    Read payload from IF2 registers
                              │
                              ▼
                    ftsk_canRxQueue (FreeRTOS queue)
                              │
                              ▼ (task context)
                    CAN_ReadRxBuffer()
                              │
                              ▼
                    Match message ID ──► RX Callback
                              │
                              ▼
                    CAN Helper (unpack) ──► Database Tables

Queue Architecture
------------------

The driver uses two FreeRTOS queues to decouple interrupt and task contexts:

.. list-table::
   :widths: 25 25 50
   :header-rows: 1

   * - Queue
     - Direction
     - Purpose
   * - ``ftsk_canRxQueue``
     - ISR → Task
     - Buffers received CAN frames for deferred processing
   * - ``ftsk_canTxUnsentMessagesQueue``
     - Task → Task
     - Stores TX messages that could not be sent (all mailboxes busy)
