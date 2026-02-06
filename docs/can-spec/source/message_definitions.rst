Message Definitions
===================

This chapter defines all CAN messages transmitted and received by the BMS.

Cyclic Transmit Messages
------------------------

The following messages are transmitted periodically by the BMS. All use 8-byte DLC and
big-endian byte order unless otherwise noted.

.. list-table:: Cyclic TX Message Summary
   :widths: 10 30 12 12 12 24
   :header-rows: 1

   * - ID
     - Name
     - Period
     - Phase
     - DLC
     - Callback
   * - 0x220
     - BMS State
     - 100 ms
     - 0 ms
     - 8
     - ``CANTX_BmsState``
   * - 0x221
     - BMS State Details
     - 1000 ms
     - 100 ms
     - 8
     - ``CANTX_BmsStateDetails``
   * - 0x250
     - Cell Voltages
     - 100 ms
     - 10 ms
     - 8
     - ``CANTX_CellVoltages``
   * - 0x260
     - Cell Temperatures
     - 200 ms
     - 20 ms
     - 8
     - ``CANTX_CellTemperatures``
   * - 0x232
     - Pack Limits
     - 100 ms
     - 30 ms
     - 8
     - ``CANTX_PackLimits``
   * - 0x231
     - Pack Min/Max Values
     - 100 ms
     - 40 ms
     - 8
     - ``CANTX_PackMinimumMaximumValues``
   * - 0x235
     - Pack State Estimation
     - 1000 ms
     - 50 ms
     - 8
     - ``CANTX_PackStateEstimation``
   * - 0x233
     - Pack Values P0
     - 100 ms
     - 60 ms
     - 8
     - ``CANTX_PackValuesP0``
   * - 0x234
     - Pack Values P1
     - 100 ms
     - 60 ms
     - 8
     - ``CANTX_PackValuesP1``
   * - 0x240
     - String State
     - 100 ms
     - 70 ms
     - 8
     - ``CANTX_StringState``
   * - 0x241
     - String Min/Max Values
     - 100 ms
     - 80 ms
     - 8
     - ``CANTX_StringMinimumMaximumValues``
   * - 0x242
     - String State Estimation
     - 1000 ms
     - 90 ms
     - 8
     - ``CANTX_StringStateEstimation``
   * - 0x243
     - String Values P0
     - 100 ms
     - 70 ms
     - 8
     - ``CANTX_StringValuesP0``
   * - 0x244
     - String Values P1
     - 100 ms
     - 80 ms
     - 8
     - ``CANTX_StringValuesP1``

.. note::

   Messages marked with multiplexed callbacks (Cell Voltages, Cell Temperatures,
   String State, String Values, String Min/Max, String State Estimation) use an
   internal multiplexer counter to send different data subsets on each cycle.

TX Message Detail: BMS State (0x220)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Reports the overall BMS operating state and key status flags.

.. list-table::
   :widths: 15 20 15 50
   :header-rows: 1

   * - Bit Start
     - Signal Name
     - Length
     - Description
   * - 7
     - BMS State
     - 4 bits
     - Current BMS state machine state
   * - 3
     - Error Flag
     - 1 bit
     - General error indicator
   * - 11
     - Contactor State
     - 4 bits
     - Combined contactor status

TX Message Detail: Cell Voltages (0x250)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Multiplexed message transmitting up to 4 cell voltage values per frame.

.. list-table::
   :widths: 15 20 15 50
   :header-rows: 1

   * - Bit Start
     - Signal Name
     - Length
     - Description
   * - 7
     - Mux ID
     - 8 bits
     - Multiplexer index (selects which cells)
   * - 15
     - Cell Voltage 0
     - 13 bits
     - Voltage of cell (mux*4 + 0) in mV
   * - 28
     - Cell Voltage 1
     - 13 bits
     - Voltage of cell (mux*4 + 1) in mV
   * - 41
     - Cell Voltage 2
     - 13 bits
     - Voltage of cell (mux*4 + 2) in mV
   * - 54
     - Cell Voltage 3
     - 13 bits
     - Voltage of cell (mux*4 + 3) in mV

TX Message Detail: Cell Temperatures (0x260)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Multiplexed message transmitting up to 6 cell temperature values per frame.

.. list-table::
   :widths: 15 20 15 50
   :header-rows: 1

   * - Bit Start
     - Signal Name
     - Length
     - Description
   * - 7
     - Mux ID
     - 8 bits
     - Multiplexer index (selects which sensors)
   * - 15
     - Temperature 0
     - 8 bits
     - Temperature reading (mux*6 + 0) in deg C + offset
   * - 23
     - Temperature 1
     - 8 bits
     - Temperature reading (mux*6 + 1)
   * - 31
     - Temperature 2
     - 8 bits
     - Temperature reading (mux*6 + 2)
   * - 39
     - Temperature 3
     - 8 bits
     - Temperature reading (mux*6 + 3)
   * - 47
     - Temperature 4
     - 8 bits
     - Temperature reading (mux*6 + 4)
   * - 55
     - Temperature 5
     - 8 bits
     - Temperature reading (mux*6 + 5)

Asynchronous Transmit Messages
-------------------------------

These messages are sent on-demand rather than periodically, typically triggered by
specific events or requests.

.. list-table:: Async TX Message Summary
   :widths: 15 35 50
   :header-rows: 1

   * - Message
     - Callback
     - Trigger Condition
   * - IMD Request
     - ``CANTX_ImdRequest``
     - On-demand request to Insulation Monitoring Device
   * - Debug Response
     - ``CANTX_DebugResponse``
     - Response to debug query received on RX
   * - Crash Dump
     - ``CANTX_CrashDump``
     - System crash or fatal error detected
   * - Build Configuration
     - ``CANTX_DebugBuildConfiguration``
     - Requested via debug interface
   * - Unsupported Mux
     - ``CANTX_DebugUnsupportedMultiplexerValues``
     - Invalid mux value received in debug message

Receive Messages
----------------

The following messages are expected from external devices on the CAN bus.

.. list-table:: RX Message Summary
   :widths: 8 30 8 8 8 20 18
   :header-rows: 1

   * - ID
     - Name
     - Node
     - DLC
     - Endian
     - Callback
     - Source Device
   * - 0x37
     - IMD Info
     - CAN1
     - 6
     - Little
     - ``CANRX_ImdInfo``
     - IMD
   * - 0x23
     - IMD Response
     - CAN1
     - 5
     - Little
     - ``CANRX_ImdResponse``
     - IMD
   * - 0x210
     - BMS State Request
     - CAN1
     - 8
     - Big
     - ``CANRX_BmsStateRequest``
     - Supervisory
   * - 0x521
     - IVT Current
     - CAN1
     - 6
     - Big
     - ``CANRX_CurrentSensor``
     - IVT (String 0)
   * - 0x522
     - IVT Voltage 1
     - CAN1
     - 6
     - Big
     - ``CANRX_CurrentSensor``
     - IVT (String 0)
   * - 0x523
     - IVT Voltage 2
     - CAN1
     - 6
     - Big
     - ``CANRX_CurrentSensor``
     - IVT (String 0)
   * - 0x524
     - IVT Voltage 3
     - CAN1
     - 6
     - Big
     - ``CANRX_CurrentSensor``
     - IVT (String 0)
   * - 0x525
     - IVT Temperature
     - CAN1
     - 6
     - Big
     - ``CANRX_CurrentSensor``
     - IVT (String 0)
   * - 0x526
     - IVT Power
     - CAN1
     - 6
     - Big
     - ``CANRX_CurrentSensor``
     - IVT (String 0)
   * - 0x527
     - IVT Current Counter
     - CAN1
     - 6
     - Big
     - ``CANRX_CurrentSensor``
     - IVT (String 0)
   * - 0x528
     - IVT Energy Counter
     - CAN1
     - 6
     - Big
     - ``CANRX_CurrentSensor``
     - IVT (String 0)
   * - 0x300
     - Debug Message
     - CAN1
     - 8
     - Big
     - ``CANRX_Debug``
     - Debug tool
   * - 0x3C4
     - Aerosol Sensor
     - CAN1
     - 8
     - Big
     - ``CANRX_AerosolSensor``
     - Aerosol sensor
   * - 0x280
     - AFE Cell Temperatures
     - CAN1
     - 8
     - Big
     - ``CANRX_CellTemperatures``
     - AFE
   * - 0x270
     - AFE Cell Voltages
     - CAN1
     - 8
     - Big
     - ``CANRX_CellVoltages``
     - AFE

RX Message Detail: Current Sensor (0x521–0x528)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Isabellenhutte IVT current sensor sends a series of messages on CAN IDs 0x521
through 0x528. All share the same callback (``CANRX_CurrentSensor``) which differentiates
based on message ID:

.. list-table::
   :widths: 12 25 63
   :header-rows: 1

   * - ID
     - Measurement
     - Description
   * - 0x521
     - Current
     - Battery string current measurement (mA)
   * - 0x522
     - Voltage 1
     - First voltage measurement point (mV)
   * - 0x523
     - Voltage 2
     - Second voltage measurement point (mV)
   * - 0x524
     - Voltage 3
     - Third voltage measurement point (mV)
   * - 0x525
     - Temperature
     - Sensor temperature measurement (0.1 °C)
   * - 0x526
     - Power
     - Computed power measurement (mW)
   * - 0x527
     - Current Counter
     - Coulomb counting (As)
   * - 0x528
     - Energy Counter
     - Energy counting (Wh)

The current sensor callback updates the ``DATA_BLOCK_CURRENT_SENSOR_s`` database table
and sets the corresponding presence flags (``currentSensorPresent``,
``currentSensorCCPresent``, ``currentSensorECPresent``) in the module state.

RX Message Detail: BMS State Request (0x210)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Received from the supervisory controller to request BMS state transitions.

.. list-table::
   :widths: 15 25 15 45
   :header-rows: 1

   * - Bit Start
     - Signal Name
     - Length
     - Description
   * - 7
     - State Request
     - 8 bits
     - Requested BMS state (mapped to ``DATA_BLOCK_STATE_REQUEST_s``)
   * - 15
     - Previous State Request
     - 8 bits
     - Echo of previous state request for validation

RX Message Detail: Debug Message (0x300)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

General-purpose debug interface message. Supports multiplexed commands for:

- Software reset request
- Timestamp synchronization
- Build configuration query
- Diagnostic data retrieval

The multiplexer value in the first byte determines the specific debug command.
