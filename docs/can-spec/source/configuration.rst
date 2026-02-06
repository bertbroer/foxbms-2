Configuration
=============

This chapter describes all compile-time configuration options, macros, and constants
used by the CAN driver module.

Configuration Files
-------------------

.. list-table::
   :widths: 35 65
   :header-rows: 1

   * - File
     - Purpose
   * - ``can_cfg.h``
     - Type definitions, macros, and constants
   * - ``can_cfg.c``
     - CAN node instances, SHIM structure, and database table instances
   * - ``can_cfg_tx_cyclic.c``
     - Cyclic TX message table (array of ``CAN_TX_MESSAGE_TYPE_s``)
   * - ``can_cfg_rx.c``
     - RX message table (array of ``CAN_RX_MESSAGE_TYPE_s``)
   * - ``can_cfg_tx-cyclic-message-definitions.h``
     - TX message ID and timing constant definitions
   * - ``can_cfg_rx-message-definitions.h``
     - RX message ID and timing constant definitions

Hardware Constants
------------------

.. list-table::
   :widths: 40 15 45
   :header-rows: 1

   * - Macro
     - Value
     - Description
   * - ``CAN_TOTAL_NUMBER_OF_MESSAGE_BOXES``
     - 64
     - Total mailboxes in the DCAN controller
   * - ``CAN_NR_OF_TX_MESSAGE_BOX``
     - 32
     - Number of TX mailboxes (1–32)
   * - ``CAN_TICK_ms``
     - 10
     - Main function call period in milliseconds
   * - ``CAN_MAX_11BIT_ID``
     - 2048
     - Maximum value for standard 11-bit identifiers
   * - ``CAN_MAX_DLC``
     - 8
     - Maximum Data Length Code
   * - ``CAN_DEFAULT_DLC``
     - 8
     - Default DLC for messages
   * - ``CAN_FOXBMS_MESSAGES_DEFAULT_DLC``
     - 8
     - Default DLC for foxBMS-specific messages

Extended Identifier Mailbox Configuration
-----------------------------------------

.. list-table::
   :widths: 45 15 40
   :header-rows: 1

   * - Macro
     - Value
     - Description
   * - ``CAN_LOWEST_MAILBOX_FOR_EXTENDED_IDENTIFIERS``
     - 61
     - First mailbox for extended IDs
   * - ``CAN_HIGHEST_MAILBOX_FOR_EXTENDED_IDENTIFIERS``
     - 64
     - Last mailbox for extended IDs

Timing Configuration
--------------------

.. list-table::
   :widths: 40 15 45
   :header-rows: 1

   * - Macro
     - Value
     - Description
   * - ``CAN_TIMING_LOWER_LIMIT_COUNTS``
     - 95
     - Lower timing validation threshold (counts)
   * - ``CAN_TIMING_UPPER_LIMIT_COUNTS``
     - 105
     - Upper timing validation threshold (counts)

Byte Position Constants
-----------------------

Convenience macros for accessing specific bytes in the CAN data array:

.. code-block:: c

   #define CAN_BYTE_0_POSITION  (0u)
   #define CAN_BYTE_1_POSITION  (1u)
   #define CAN_BYTE_2_POSITION  (2u)
   #define CAN_BYTE_3_POSITION  (3u)
   #define CAN_BYTE_4_POSITION  (4u)
   #define CAN_BYTE_5_POSITION  (5u)
   #define CAN_BYTE_6_POSITION  (6u)
   #define CAN_BYTE_7_POSITION  (7u)

Signal Constants
----------------

.. list-table::
   :widths: 40 15 45
   :header-rows: 1

   * - Macro
     - Value
     - Description
   * - ``CAN_SIGNAL_MAX_SIZE``
     - 64
     - Maximum signal width in bits
   * - ``CAN_SIGNAL_OFFSET_0``
     - 0.0f
     - Default zero offset for signals
   * - ``CAN_BIT``
     - 1
     - Single-bit signal width
   * - ``CAN_NUM_OF_VOLTAGES_IN_CAN_CELL_VOLTAGES_MSG``
     - 4
     - Voltage values per cell voltages message
   * - ``CAN_NUM_OF_TEMPERATURES_IN_CAN_CELL_TEMPERATURES_MSG``
     - 6
     - Temperature values per cell temperatures message

Transceiver Pin Assignments
----------------------------

CAN transceiver control pins on the Port Expander:

.. list-table::
   :widths: 30 30 40
   :header-rows: 1

   * - Macro
     - Value
     - Description
   * - ``CAN1_ENABLE_PIN``
     - ``PEX_PORT_0_PIN_0``
     - CAN1 transceiver enable
   * - ``CAN1_STANDBY_PIN``
     - ``PEX_PORT_0_PIN_1``
     - CAN1 transceiver standby control
   * - ``CAN2_ENABLE_PIN``
     - ``PEX_PORT_0_PIN_2``
     - CAN2 transceiver enable
   * - ``CAN2_STANDBY_PIN``
     - ``PEX_PORT_0_PIN_3``
     - CAN2 transceiver standby control

CAN Node Assignments
--------------------

Default CAN node assignments for message categories:

.. code-block:: c

   #define CAN_NODE_1                        (&can_node1)
   #define CAN_NODE_2                        (&can_node2Isolated)

   #define CAN_NODE_DEBUG_MESSAGE            (CAN_NODE_1)
   #define CAN_NODE_IMD                      (CAN_NODE_1)
   #define CAN_NODE_CURRENT_SENSOR           (CAN_NODE_1)
   #define CAN_NODE_RX_CELL_VOLTAGES         (CAN_NODE_1)
   #define CAN_NODE_RX_CELL_TEMPERATURES     (CAN_NODE_1)

Adding a New TX Message
-----------------------

To add a new cyclic TX message:

1. **Define the message ID and timing** in ``can_cfg_tx-cyclic-message-definitions.h``:

   .. code-block:: c

      #define CANTX_MY_MESSAGE_ID       (0x2A0u)
      #define CANTX_MY_MESSAGE_ID_TYPE  (CAN_STANDARD_IDENTIFIER_11_BIT)
      #define CANTX_MY_MESSAGE_PERIOD   (100u)  /* ms */
      #define CANTX_MY_MESSAGE_PHASE    (30u)   /* ms */

2. **Implement the callback** in a new file under ``cbs/tx-cyclic/``:

   .. code-block:: c

      uint32_t CANTX_MyMessage(
          CAN_MESSAGE_PROPERTIES_s message,
          uint8_t *canData,
          uint8_t *pMuxId,
          const CAN_SHIM_s *const kpkCanShim)
      {
          /* Pack signals into canData */
          return 0u;
      }

3. **Add the message entry** to the ``can_txMessages[]`` array in ``can_cfg_tx_cyclic.c``:

   .. code-block:: c

      {
          .canNode          = CAN_NODE_1,
          .message          = {CANTX_MY_MESSAGE_ID,
                               CANTX_MY_MESSAGE_ID_TYPE,
                               CAN_DEFAULT_DLC,
                               CAN_BIG_ENDIAN},
          .timing           = {CANTX_MY_MESSAGE_PERIOD,
                               CANTX_MY_MESSAGE_PHASE},
          .callbackFunction = CANTX_MyMessage,
          .pMuxId           = NULL,
      },

4. **Declare the callback** in ``can_cbs_tx_cyclic.h``.

Adding a New RX Message
-----------------------

To add a new RX message:

1. **Define the message ID** in ``can_cfg_rx-message-definitions.h``:

   .. code-block:: c

      #define CANRX_MY_SENSOR_ID       (0x350u)
      #define CANRX_MY_SENSOR_ID_TYPE  (CAN_STANDARD_IDENTIFIER_11_BIT)
      #define CANRX_MY_SENSOR_PERIOD   (100u)  /* ms, informational */

2. **Implement the callback** in a new file under ``cbs/rx/``:

   .. code-block:: c

      uint32_t CANRX_MySensor(
          CAN_MESSAGE_PROPERTIES_s message,
          const uint8_t *const kpkCanData,
          const CAN_SHIM_s *const kpkCanShim)
      {
          /* Extract signals from kpkCanData */
          return 0u;
      }

3. **Add the message entry** to the ``can_rxMessages[]`` array in ``can_cfg_rx.c``.

4. **Declare the callback** in ``can_cbs_rx.h``.
