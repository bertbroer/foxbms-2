Initialization
==============

Initialization Sequence
-----------------------

The CAN module must be initialized before any messages can be transmitted or received.
The initialization is performed by calling ``CAN_Initialize()``, which executes the
following sequence:

.. code-block:: text

   CAN_Initialize()
       │
       ├─► canInit()
       │       Hardware-level CAN controller initialization (HAL)
       │
       ├─► CAN_ConfigureRxMailboxesForExtendedIdentifiers()
       │       Configure mailboxes 42, 61–64 on CAN1 and CAN2
       │       for 29-bit extended identifier reception
       │
       ├─► CAN_InitializeTransceiver()
       │       Enable CAN transceivers via Port Expander (PEX)
       │       Set enable and standby pins for CAN1 and CAN2
       │
       ├─► CAN_CalculateCounterResetValue()
       │       Compute LCM of all TX message periods for counter wraparound
       │
       ├─► CAN_ValidateConfiguredTxMessagePeriod()
       │       Assert all periods are non-zero multiples of CAN_TICK_ms
       │
       ├─► CAN_ValidateConfiguredTxMessagePhase()
       │       Assert all phases are less than their period
       │       and are multiples of CAN_TICK_ms
       │
       └─► CAN_CheckDatabaseNullPointer()
               Validate all CAN_SHIM database pointers are non-NULL

HAL Initialization
------------------

The ``canInit()`` function is provided by the TI HALCoGen Hardware Abstraction Layer and
performs the following hardware-level setup:

- Configure CAN controller clock source and prescaler
- Set bit timing parameters (TSEG1, TSEG2, SJW, BRP)
- Initialize all 64 message mailboxes to default state
- Enable CAN controller interrupts
- Transition controller from Init mode to Normal mode

Extended Identifier Mailbox Configuration
-----------------------------------------

By default, mailboxes are configured for standard 11-bit identifiers. The function
``CAN_ConfigureRxMailboxesForExtendedIdentifiers()`` reconfigures specific mailboxes
to accept 29-bit extended identifiers:

**Configured Mailboxes:**

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Mailbox
     - CAN Node
     - Configuration
   * - 42
     - CAN1, CAN2
     - Extended identifier RX
   * - 61
     - CAN1, CAN2
     - Extended identifier RX
   * - 62
     - CAN1, CAN2
     - Extended identifier RX
   * - 63
     - CAN1, CAN2
     - Extended identifier RX
   * - 64
     - CAN1, CAN2
     - Extended identifier RX

**Register Configuration:**

For each mailbox, the following IF1/IF2 registers are programmed:

.. code-block:: c

   /* Wait for IF1 interface to be free */
   while ((node->IF1STAT & 0x80) == 0x80) { }

   /* Set control register: accept extended identifiers */
   node->IF1CMD  = 0xF8;   /* Transfer control, arb, mask, data */
   node->IF1MSK  = 0xC0000000; /* Mask: match on extended ID bit */
   node->IF1ARB  = 0x80000000; /* Arb: valid, extended, RX direction */
   node->IF1MCTL = 0x00001488; /* DLC=8, use acceptance mask, RX IE */
   node->IF1NO   = mailbox_number;

Transceiver Initialization
--------------------------

CAN transceivers are controlled through a Port Expander (PEX) connected via SPI.
The following pins are configured during initialization:

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Signal
     - PEX Pin
     - State
     - Effect
   * - CAN1 Enable
     - ``PEX_PORT_0_PIN_0``
     - High
     - Activate CAN1 transceiver
   * - CAN1 Standby
     - ``PEX_PORT_0_PIN_1``
     - High
     - Normal operation mode
   * - CAN2 Enable
     - ``PEX_PORT_0_PIN_2``
     - High
     - Activate CAN2 transceiver
   * - CAN2 Standby
     - ``PEX_PORT_0_PIN_3``
     - High
     - Normal operation mode

Enabling Periodic Communication
--------------------------------

After initialization, periodic CAN transmission is disabled by default to prevent
sending uninitialized data. It must be explicitly enabled:

.. code-block:: c

   /* Enable periodic CAN message transmission */
   CAN_EnablePeriodic(true);

   /* Disable periodic CAN message transmission */
   CAN_EnablePeriodic(false);

.. warning::

   Do not enable periodic transmission until all database tables have been populated
   with valid data. Transmitting uninitialized data may cause incorrect behavior in
   connected devices.

Configuration Validation
------------------------

The initialization routine performs the following compile-time and run-time checks:

**Period Validation:**

- Every TX message period must be > 0
- Every TX message period must be an exact multiple of ``CAN_TICK_ms`` (10 ms)
- Violation triggers ``FAS_ASSERT(FAS_TRAP)``

**Phase Validation:**

- Every TX message phase must be < its period
- Every TX message phase must be an exact multiple of ``CAN_TICK_ms`` (10 ms)
- Violation triggers ``FAS_ASSERT(FAS_TRAP)``

**Database Pointer Validation:**

- All pointers in the ``CAN_SHIM_s`` structure are checked for NULL
- Any NULL pointer triggers ``FAS_ASSERT(FAS_TRAP)``
