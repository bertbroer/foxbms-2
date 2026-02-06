Appendix
========

Source File Reference
---------------------

The following table lists all source files that comprise the CAN driver module.

Core Driver
^^^^^^^^^^^

.. list-table::
   :widths: 45 55
   :header-rows: 1

   * - File
     - Description
   * - ``src/app/driver/can/can.c``
     - Main CAN driver implementation
   * - ``src/app/driver/can/can.h``
     - Main CAN driver header (public API)

Helper Functions
^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 45 55
   :header-rows: 1

   * - File
     - Description
   * - ``src/app/driver/can/cbs/can_helper.c``
     - Signal packing/unpacking and conversion functions
   * - ``src/app/driver/can/cbs/can_helper.h``
     - Helper function declarations

Configuration
^^^^^^^^^^^^^

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - File
     - Description
   * - ``src/app/driver/config/can_cfg.c``
     - Node instances, SHIM, database tables
   * - ``src/app/driver/config/can_cfg.h``
     - Types, macros, constants
   * - ``src/app/driver/config/can_cfg_tx_cyclic.c``
     - TX message table definition
   * - ``src/app/driver/config/can_cfg_rx.c``
     - RX message table definition
   * - ``src/app/driver/config/can_cfg_tx-cyclic-message-definitions.h``
     - TX message ID/timing macros
   * - ``src/app/driver/config/can_cfg_rx-message-definitions.h``
     - RX message ID/timing macros

RX Callback Handlers
^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 55 45
   :header-rows: 1

   * - File
     - Description
   * - ``cbs/rx/can_cbs_rx_bms-state-request.c``
     - BMS state request handler
   * - ``cbs/rx/can_cbs_rx_current-sensor.c``
     - IVT current sensor handler (0x521–0x528)
   * - ``cbs/rx/can_cbs_rx_imd-info.c``
     - IMD info message handler
   * - ``cbs/rx/can_cbs_rx_imd-response.c``
     - IMD response message handler
   * - ``cbs/rx/can_cbs_rx_debug.c``
     - Debug message handler
   * - ``cbs/rx/can_cbs_rx_aerosol-sensor.c``
     - Aerosol sensor message handler
   * - ``cbs/rx/can_cbs_rx_cell-temperatures.c``
     - AFE cell temperatures handler
   * - ``cbs/rx/can_cbs_rx_cell-voltages.c``
     - AFE cell voltages handler

TX Cyclic Callback Handlers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 60 40
   :header-rows: 1

   * - File
     - Description
   * - ``cbs/tx-cyclic/can_cbs_tx_bms-state.c``
     - BMS state (0x220)
   * - ``cbs/tx-cyclic/can_cbs_tx_bms-state-details.c``
     - BMS state details (0x221)
   * - ``cbs/tx-cyclic/can_cbs_tx_cell-voltages.c``
     - Cell voltages (0x250)
   * - ``cbs/tx-cyclic/can_cbs_tx_cell-temperatures.c``
     - Cell temperatures (0x260)
   * - ``cbs/tx-cyclic/can_cbs_tx_pack-limits.c``
     - Pack limits (0x232)
   * - ``cbs/tx-cyclic/can_cbs_tx_pack-minimum-maximum-values.c``
     - Pack min/max (0x231)
   * - ``cbs/tx-cyclic/can_cbs_tx_pack-state-estimation.c``
     - Pack SOC/SOE/SOH (0x235)
   * - ``cbs/tx-cyclic/can_cbs_tx_pack-values-p0.c``
     - Pack values part 0 (0x233)
   * - ``cbs/tx-cyclic/can_cbs_tx_pack-values-p1.c``
     - Pack values part 1 (0x234)
   * - ``cbs/tx-cyclic/can_cbs_tx_string-state.c``
     - String state (0x240)
   * - ``cbs/tx-cyclic/can_cbs_tx_string-values-p0.c``
     - String values part 0 (0x243)
   * - ``cbs/tx-cyclic/can_cbs_tx_string-values-p1.c``
     - String values part 1 (0x244)
   * - ``cbs/tx-cyclic/can_cbs_tx_string-minimum-maximum-values.c``
     - String min/max (0x241)
   * - ``cbs/tx-cyclic/can_cbs_tx_string-state-estimation.c``
     - String SOC/SOE/SOH (0x242)

TX Async Callback Handlers
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :widths: 60 40
   :header-rows: 1

   * - File
     - Description
   * - ``cbs/tx-async/can_cbs_tx_imd-request.c``
     - IMD request
   * - ``cbs/tx-async/can_cbs_tx_crash-dump.c``
     - Crash dump
   * - ``cbs/tx-async/can_cbs_tx_debug-response.c``
     - Debug response
   * - ``cbs/tx-async/can_cbs_tx_debug-build-configuration.c``
     - Build configuration
   * - ``cbs/tx-async/can_cbs_tx_debug-unsupported-multiplexer-values.c``
     - Unsupported mux values

CAN Message ID Summary
----------------------

Quick reference of all CAN message identifiers used by the BMS.

TX Messages
^^^^^^^^^^^

.. list-table::
   :widths: 12 35 15 15 23
   :header-rows: 1

   * - ID (hex)
     - Name
     - Period
     - DLC
     - Multiplexed
   * - 0x220
     - BMS State
     - 100 ms
     - 8
     - No
   * - 0x221
     - BMS State Details
     - 1000 ms
     - 8
     - No
   * - 0x231
     - Pack Min/Max Values
     - 100 ms
     - 8
     - No
   * - 0x232
     - Pack Limits
     - 100 ms
     - 8
     - No
   * - 0x233
     - Pack Values P0
     - 100 ms
     - 8
     - No
   * - 0x234
     - Pack Values P1
     - 100 ms
     - 8
     - No
   * - 0x235
     - Pack State Estimation
     - 1000 ms
     - 8
     - No
   * - 0x240
     - String State
     - 100 ms
     - 8
     - Yes
   * - 0x241
     - String Min/Max Values
     - 100 ms
     - 8
     - Yes
   * - 0x242
     - String State Estimation
     - 1000 ms
     - 8
     - Yes
   * - 0x243
     - String Values P0
     - 100 ms
     - 8
     - Yes
   * - 0x244
     - String Values P1
     - 100 ms
     - 8
     - Yes
   * - 0x250
     - Cell Voltages
     - 100 ms
     - 8
     - Yes
   * - 0x260
     - Cell Temperatures
     - 200 ms
     - 8
     - Yes

RX Messages
^^^^^^^^^^^

.. list-table::
   :widths: 12 35 15 15 23
   :header-rows: 1

   * - ID (hex)
     - Name
     - DLC
     - Endian
     - Source
   * - 0x23
     - IMD Response
     - 5
     - Little
     - IMD
   * - 0x37
     - IMD Info
     - 6
     - Little
     - IMD
   * - 0x210
     - BMS State Request
     - 8
     - Big
     - Supervisory
   * - 0x270
     - AFE Cell Voltages
     - 8
     - Big
     - AFE
   * - 0x280
     - AFE Cell Temperatures
     - 8
     - Big
     - AFE
   * - 0x300
     - Debug Message
     - 8
     - Big
     - Debug tool
   * - 0x3C4
     - Aerosol Sensor
     - 8
     - Big
     - Aerosol sensor
   * - 0x521–0x528
     - IVT Sensor (8 msgs)
     - 6
     - Big
     - IVT

Revision History
----------------

.. list-table::
   :widths: 15 15 20 50
   :header-rows: 1

   * - Revision
     - Date
     - Author
     - Changes
   * - 1.0.0
     - Feb 2026
     - Invi Tech
     - Initial release — complete CAN interface specification
