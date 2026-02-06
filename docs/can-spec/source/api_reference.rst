API Reference
=============

This chapter provides a complete reference of all public functions exposed by the CAN
driver module.

Core Functions
--------------

CAN_Initialize
^^^^^^^^^^^^^^

.. code-block:: c

   void CAN_Initialize(void)

Initializes the CAN module hardware, transceivers, and validates configuration.

**Parameters:** None

**Returns:** ``void``

**Description:**

This function must be called once during system startup before any CAN communication
can occur. It performs the full initialization sequence described in :doc:`initialization`.

**Preconditions:**

- SPI bus must be initialized (required for PEX transceiver control)
- FreeRTOS queues must be created

**Postconditions:**

- CAN1 and CAN2 controllers are active
- CAN transceivers are enabled
- RX mailboxes are configured for both standard and extended identifiers
- Periodic transmission remains disabled (must be enabled separately)

----

CAN_EnablePeriodic
^^^^^^^^^^^^^^^^^^

.. code-block:: c

   void CAN_EnablePeriodic(bool command)

Enables or disables periodic CAN message transmission.

**Parameters:**

.. list-table::
   :widths: 15 15 70
   :header-rows: 1

   * - Name
     - Type
     - Description
   * - ``command``
     - ``bool``
     - ``true`` to enable periodic TX, ``false`` to disable

**Returns:** ``void``

**Description:**

Controls the periodic transmission state machine. When disabled, the CAN main function
will not transmit any cyclic messages. This prevents sending uninitialized data before
the system is ready.

----

CAN_MainFunction
^^^^^^^^^^^^^^^^

.. code-block:: c

   void CAN_MainFunction(void)

Main CAN driver function — called periodically every 10 ms by the task scheduler.

**Parameters:** None

**Returns:** ``void``

**Description:**

This is the cyclic entry point for the CAN driver, called from the 10 ms application task.
It performs:

1. CAN bus timing validation (``CAN_CheckCanTiming()``)
2. Periodic message transmission if enabled (``CAN_PeriodicTransmit()``)

The periodic transmit function:

- Retries previously unsent messages from the TX queue
- Iterates through all configured TX messages
- For each message whose period has elapsed (accounting for phase), calls the
  associated callback to generate data and attempts transmission
- Increments the tick counter (with wraparound at the calculated LCM)

----

Transmission Functions
----------------------

CAN_DataSend
^^^^^^^^^^^^^

.. code-block:: c

   STD_RETURN_TYPE_e CAN_DataSend(
       CAN_NODE_s *pNode,
       uint32_t id,
       CAN_IDENTIFIER_TYPE_e idType,
       uint8 *pData
   )

Sends a single CAN message on the specified node.

**Parameters:**

.. list-table::
   :widths: 15 30 55
   :header-rows: 1

   * - Name
     - Type
     - Description
   * - ``pNode``
     - ``CAN_NODE_s *``
     - Pointer to CAN node (``CAN_NODE_1`` or ``CAN_NODE_2``)
   * - ``id``
     - ``uint32_t``
     - CAN message identifier
   * - ``idType``
     - ``CAN_IDENTIFIER_TYPE_e``
     - ``CAN_STANDARD_IDENTIFIER_11_BIT`` or ``CAN_EXTENDED_IDENTIFIER_29_BIT``
   * - ``pData``
     - ``uint8 *``
     - Pointer to 8-byte data payload

**Returns:**

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Value
     - Meaning
   * - ``STD_OK``
     - Message was placed in a free TX mailbox
   * - ``STD_NOT_OK``
     - No free TX mailbox was available

**Description:**

Searches through the 32 TX mailboxes (1–32) for a free slot. When found, configures
the IF1 arbitration register with the message ID and transfers the 8-byte payload.

For standard identifiers, the ID is left-shifted by 18 bits into the IF1ARB register.
For extended identifiers, the ID is placed directly.

.. note::

   If no free mailbox is found, the caller should queue the message for retry via
   ``ftsk_canTxUnsentMessagesQueue``.

----

CAN_SendMessagesFromQueue
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: c

   void CAN_SendMessagesFromQueue(void)

Retransmits previously unsent messages from the TX queue.

**Parameters:** None

**Returns:** ``void``

**Description:**

Reads all pending entries from ``ftsk_canTxUnsentMessagesQueue`` and attempts to
retransmit each one via ``CAN_DataSend()``. Called at the beginning of each
periodic transmit cycle.

----

Reception Functions
-------------------

CAN_ReadRxBuffer
^^^^^^^^^^^^^^^^

.. code-block:: c

   void CAN_ReadRxBuffer(void)

Processes all received CAN messages from the RX queue.

**Parameters:** None

**Returns:** ``void``

**Description:**

Drains the ``ftsk_canRxQueue`` and matches each received message against the configured
RX message table. When a match is found (by CAN node, message ID, and identifier type),
the associated callback function is invoked.

This function runs in task context, so callbacks have full access to the database and
other OS services (unlike interrupt context).

**Matching Logic:**

.. code-block:: c

   for each message in ftsk_canRxQueue:
       for each entry in can_rxMessages[]:
           if (entry.canNode == message.canNode &&
               entry.message.id == message.id &&
               entry.message.idType == message.idType):
               entry.callbackFunction(entry.message, message.data, &can_kShim)

----

Status Query Functions
----------------------

CAN_IsCurrentSensorPresent
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: c

   bool CAN_IsCurrentSensorPresent(uint8_t stringNumber)

Checks whether the current sensor for a given string is present on the CAN bus.

**Parameters:**

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Name
     - Type
     - Description
   * - ``stringNumber``
     - ``uint8_t``
     - Battery string index (0 to ``BS_NR_OF_STRINGS - 1``)

**Returns:** ``true`` if the current sensor is responding, ``false`` otherwise.

----

CAN_IsCurrentSensorCcPresent
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: c

   bool CAN_IsCurrentSensorCcPresent(uint8_t stringNumber)

Checks whether Coulomb Counting messages are being received from the current sensor.

**Parameters:**

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Name
     - Type
     - Description
   * - ``stringNumber``
     - ``uint8_t``
     - Battery string index (0 to ``BS_NR_OF_STRINGS - 1``)

**Returns:** ``true`` if CC messages are detected, ``false`` otherwise.

----

CAN_IsCurrentSensorEcPresent
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: c

   bool CAN_IsCurrentSensorEcPresent(uint8_t stringNumber)

Checks whether Energy Counting messages are being received from the current sensor.

**Parameters:**

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Name
     - Type
     - Description
   * - ``stringNumber``
     - ``uint8_t``
     - Battery string index (0 to ``BS_NR_OF_STRINGS - 1``)

**Returns:** ``true`` if EC messages are detected, ``false`` otherwise.
