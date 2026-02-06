Error Handling
==============

This chapter describes the error detection, diagnostic reporting, and fault handling
mechanisms implemented in the CAN driver module.

CAN Bus Timing Validation
--------------------------

The function ``CAN_CheckCanTiming()`` monitors the timing of received CAN messages
and reports deviations to the diagnostic module.

Timing Window
^^^^^^^^^^^^^

Messages are expected at a nominal rate. The timing is validated against a window:

.. list-table::
   :widths: 30 20 50
   :header-rows: 1

   * - Parameter
     - Value
     - Description
   * - ``CAN_TIMING_LOWER_LIMIT_COUNTS``
     - 95
     - Minimum acceptable timing counts
   * - ``CAN_TIMING_UPPER_LIMIT_COUNTS``
     - 105
     - Maximum acceptable timing counts
   * - Tick resolution
     - 10 ms
     - ``CAN_TICK_ms``
   * - Nominal window
     - 950–1050 ms
     - Acceptable range for 1 s nominal period

Diagnostic IDs
^^^^^^^^^^^^^^

The timing validation reports to the following diagnostic handler IDs:

.. list-table::
   :widths: 40 60
   :header-rows: 1

   * - Diagnostic ID
     - Condition
   * - ``DIAG_ID_CAN_TIMING``
     - General CAN message timing deviation
   * - ``DIAG_ID_CURRENT_SENSOR_RESPONDING``
     - Current sensor main messages absent/late
   * - ``DIAG_ID_CAN_CC_RESPONDING``
     - Coulomb counting message absent/late
   * - ``DIAG_ID_CAN_EC_RESPONDING``
     - Energy counting message absent/late

Each diagnostic event is reported via ``DIAG_Handler()`` with either ``DIAG_EVENT_OK``
(timing within window) or ``DIAG_EVENT_NOT_OK`` (timing violation).

Queue Overflow Detection
------------------------

TX Queue Overflow
^^^^^^^^^^^^^^^^^

When a CAN message cannot be transmitted because all 32 TX mailboxes are busy, the
message is placed in ``ftsk_canTxUnsentMessagesQueue``. If this queue is also full:

- The diagnostic event ``DIAG_ID_CAN_TX_QUEUE_FULL`` is raised
- The message is silently dropped

**Mitigation:** The queue is drained at the start of each periodic transmit cycle by
``CAN_SendMessagesFromQueue()``.

RX Queue Overflow
^^^^^^^^^^^^^^^^^

When the ``ftsk_canRxQueue`` is full and a new message arrives in the interrupt handler:

- The ``canIoError`` flag is set by the OS send-to-queue function
- The diagnostic event ``DIAG_ID_CAN_RX_QUEUE_FULL`` is raised
- The received message is lost

**Mitigation:** Ensure ``CAN_ReadRxBuffer()`` is called frequently enough to drain the
queue before overflow occurs. The default 10 ms task cycle is designed for this purpose.

Configuration Validation Errors
-------------------------------

The following configuration errors are detected during initialization and cause
immediate system halt via ``FAS_ASSERT(FAS_TRAP)``:

.. list-table::
   :widths: 40 60
   :header-rows: 1

   * - Validation
     - Error Condition
   * - Period validation
     - TX message period is zero
   * - Period validation
     - TX message period is not a multiple of ``CAN_TICK_ms``
   * - Phase validation
     - TX message phase >= period
   * - Phase validation
     - TX message phase is not a multiple of ``CAN_TICK_ms``
   * - Database pointer validation
     - Any ``CAN_SHIM_s`` pointer is ``NULL``

.. warning::

   Configuration validation failures trigger a non-recoverable assertion. These indicate
   programming errors in the message configuration tables and must be fixed at compile
   time.

Runtime Assertion Failures
--------------------------

The following runtime conditions trigger ``FAS_ASSERT`` in the CAN driver:

.. list-table::
   :widths: 35 35 30
   :header-rows: 1

   * - Function
     - Condition
     - Cause
   * - ``CAN_DataSend``
     - Invalid ``pNode``
     - Node pointer is not ``CAN_NODE_1`` or ``CAN_NODE_2``
   * - ``CAN_DataSend``
     - Invalid ``idType``
     - Identifier type is ``CAN_INVALID_TYPE``
   * - ``CAN_RxInterrupt``
     - Invalid node
     - ISR called for unrecognized CAN register base
   * - Helper functions
     - NULL pointer
     - Any required pointer parameter is NULL

Error Recovery
--------------

The CAN driver implements the following error recovery mechanisms:

Automatic TX Retry
^^^^^^^^^^^^^^^^^^

Messages that fail to transmit due to busy mailboxes are automatically queued and
retried on the next periodic cycle (10 ms later). This provides transparent recovery
for transient bus load conditions.

.. code-block:: text

   CAN_DataSend() fails → Queue to ftsk_canTxUnsentMessagesQueue
                                     │
                          ┌──────────┘ (next 10 ms cycle)
                          ▼
              CAN_SendMessagesFromQueue() → CAN_DataSend() retry

Current Sensor Presence Tracking
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The driver continuously monitors current sensor message reception and updates
presence flags:

- ``CAN_IsCurrentSensorPresent()`` — set ``true`` when any IVT message received
- ``CAN_IsCurrentSensorCcPresent()`` — set ``true`` when CC message (0x527) received
- ``CAN_IsCurrentSensorEcPresent()`` — set ``true`` when EC message (0x528) received

These flags are cleared when the timing validation detects message absence, enabling
the application to detect sensor disconnection.
