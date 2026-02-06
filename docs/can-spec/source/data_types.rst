Data Types
==========

This chapter describes all data types, structures, and enumerations defined by the CAN
driver module.

Enumerations
------------

CAN_ENDIANNESS_e
^^^^^^^^^^^^^^^^

Specifies the byte order for CAN signal encoding/decoding.

.. code-block:: c

   typedef enum {
       CAN_LITTLE_ENDIAN,  /**< Intel byte order (LSB first) */
       CAN_BIG_ENDIAN,     /**< Motorola byte order (MSB first) */
   } CAN_ENDIANNESS_e;

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Value
     - Description
   * - ``CAN_LITTLE_ENDIAN``
     - Intel byte order. Least significant byte at lowest address.
   * - ``CAN_BIG_ENDIAN``
     - Motorola byte order. Most significant byte at lowest address.
       Uses bit numbering where bit 7 of byte 0 is the MSB.

----

CAN_IDENTIFIER_TYPE_e
^^^^^^^^^^^^^^^^^^^^^

Specifies the CAN identifier type.

.. code-block:: c

   typedef enum {
       CAN_STANDARD_IDENTIFIER_11_BIT,  /**< Standard 11-bit CAN ID */
       CAN_EXTENDED_IDENTIFIER_29_BIT,  /**< Extended 29-bit CAN ID */
       CAN_INVALID_TYPE,                /**< Invalid (guard value) */
   } CAN_IDENTIFIER_TYPE_e;

.. list-table::
   :widths: 40 60
   :header-rows: 1

   * - Value
     - Description
   * - ``CAN_STANDARD_IDENTIFIER_11_BIT``
     - CAN 2.0A standard frame with 11-bit identifier (0x000–0x7FF)
   * - ``CAN_EXTENDED_IDENTIFIER_29_BIT``
     - CAN 2.0B extended frame with 29-bit identifier (0x00000000–0x1FFFFFFF)
   * - ``CAN_INVALID_TYPE``
     - Guard value — used for parameter validation

----

Structures
----------

CAN_NODE_s
^^^^^^^^^^

CAN hardware node descriptor.

.. code-block:: c

   typedef struct {
       canBASE_t *canNodeRegister;
   } CAN_NODE_s;

.. list-table::
   :widths: 25 20 55
   :header-rows: 1

   * - Field
     - Type
     - Description
   * - ``canNodeRegister``
     - ``canBASE_t *``
     - Pointer to the CAN controller register base (``canREG1`` or ``canREG2``)

**Predefined Instances:**

.. code-block:: c

   CAN_NODE_s can_node1          = { .canNodeRegister = canREG1 };
   CAN_NODE_s can_node2Isolated  = { .canNodeRegister = canREG2 };

   #define CAN_NODE_1  (&can_node1)
   #define CAN_NODE_2  (&can_node2Isolated)

----

CAN_MESSAGE_PROPERTIES_s
^^^^^^^^^^^^^^^^^^^^^^^^^

Describes the properties of a single CAN message.

.. code-block:: c

   typedef struct {
       uint32_t id;
       CAN_IDENTIFIER_TYPE_e idType;
       uint8_t dlc;
       CAN_ENDIANNESS_e endianness;
   } CAN_MESSAGE_PROPERTIES_s;

.. list-table::
   :widths: 20 30 50
   :header-rows: 1

   * - Field
     - Type
     - Description
   * - ``id``
     - ``uint32_t``
     - CAN message identifier (11-bit or 29-bit)
   * - ``idType``
     - ``CAN_IDENTIFIER_TYPE_e``
     - Standard or extended identifier
   * - ``dlc``
     - ``uint8_t``
     - Data Length Code (0–8 bytes)
   * - ``endianness``
     - ``CAN_ENDIANNESS_e``
     - Signal byte order within this message

----

CAN_SIGNAL_TYPE_s
^^^^^^^^^^^^^^^^^

Defines a single signal within a CAN message, including its position and
physical-to-raw conversion parameters.

.. code-block:: c

   typedef struct {
       uint8_t bitStart;
       uint8_t bitLength;
       float_t factor;
       float_t offset;
       float_t min;
       float_t max;
   } CAN_SIGNAL_TYPE_s;

.. list-table::
   :widths: 15 15 70
   :header-rows: 1

   * - Field
     - Type
     - Description
   * - ``bitStart``
     - ``uint8_t``
     - Start bit position in the 64-bit CAN message (0–63)
   * - ``bitLength``
     - ``uint8_t``
     - Signal width in bits (1–64)
   * - ``factor``
     - ``float_t``
     - Scaling factor: ``physical = raw * factor - offset``
   * - ``offset``
     - ``float_t``
     - DC offset: ``physical = raw * factor - offset``
   * - ``min``
     - ``float_t``
     - Minimum allowed physical value (used for clamping on TX)
   * - ``max``
     - ``float_t``
     - Maximum allowed physical value (used for clamping on TX)

**Conversion Formulas:**

.. code-block:: text

   TX (physical → raw):  raw = (clamped_physical + offset) / factor
   RX (raw → physical):  physical = raw * factor - offset

----

CAN_BUFFER_ELEMENT_s
^^^^^^^^^^^^^^^^^^^^

Element stored in the RX receive queue — represents one received CAN frame.

.. code-block:: c

   typedef struct {
       CAN_NODE_s *canNode;
       uint32_t id;
       CAN_IDENTIFIER_TYPE_e idType;
       uint8_t data[CAN_MAX_DLC];
   } CAN_BUFFER_ELEMENT_s;

.. list-table::
   :widths: 15 25 60
   :header-rows: 1

   * - Field
     - Type
     - Description
   * - ``canNode``
     - ``CAN_NODE_s *``
     - CAN node the message was received on
   * - ``id``
     - ``uint32_t``
     - Received message ID
   * - ``idType``
     - ``CAN_IDENTIFIER_TYPE_e``
     - Standard or extended
   * - ``data``
     - ``uint8_t[8]``
     - Message payload (8 bytes)

----

CAN_TX_MESSAGE_TIMING_s
^^^^^^^^^^^^^^^^^^^^^^^^

Timing parameters for cyclic TX messages.

.. code-block:: c

   typedef struct {
       uint32_t period;
       uint32_t phase;
   } CAN_TX_MESSAGE_TIMING_s;

.. list-table::
   :widths: 15 15 70
   :header-rows: 1

   * - Field
     - Type
     - Description
   * - ``period``
     - ``uint32_t``
     - Cycle time in milliseconds. Must be a non-zero multiple of ``CAN_TICK_ms`` (10 ms).
   * - ``phase``
     - ``uint32_t``
     - Phase offset in milliseconds. Defines the first transmission time after periodic
       enable. Must be less than ``period`` and a multiple of ``CAN_TICK_ms``.

----

CAN_RX_MESSAGE_TIMING_s
^^^^^^^^^^^^^^^^^^^^^^^^

Timing parameters for RX messages (informational).

.. code-block:: c

   typedef struct {
       uint32_t period;
   } CAN_RX_MESSAGE_TIMING_s;

.. list-table::
   :widths: 15 15 70
   :header-rows: 1

   * - Field
     - Type
     - Description
   * - ``period``
     - ``uint32_t``
     - Expected receive cycle time in milliseconds. Used for timing validation only.

----

CAN_TX_MESSAGE_TYPE_s
^^^^^^^^^^^^^^^^^^^^^

Complete TX message configuration entry — one per configured cyclic message.

.. code-block:: c

   typedef struct {
       CAN_NODE_s *canNode;
       CAN_MESSAGE_PROPERTIES_s message;
       CAN_TX_MESSAGE_TIMING_s timing;
       CAN_TxCallbackFunction_f callbackFunction;
       uint8_t *pMuxId;
   } CAN_TX_MESSAGE_TYPE_s;

.. list-table::
   :widths: 20 30 50
   :header-rows: 1

   * - Field
     - Type
     - Description
   * - ``canNode``
     - ``CAN_NODE_s *``
     - CAN node to transmit on
   * - ``message``
     - ``CAN_MESSAGE_PROPERTIES_s``
     - Message ID, type, DLC, and endianness
   * - ``timing``
     - ``CAN_TX_MESSAGE_TIMING_s``
     - Period and phase
   * - ``callbackFunction``
     - ``CAN_TxCallbackFunction_f``
     - Callback to generate message payload
   * - ``pMuxId``
     - ``uint8_t *``
     - Pointer to multiplexer state variable (``NULL`` if not multiplexed)

----

CAN_RX_MESSAGE_TYPE_s
^^^^^^^^^^^^^^^^^^^^^

Complete RX message configuration entry — one per configured receive message.

.. code-block:: c

   typedef struct {
       CAN_NODE_s *canNode;
       CAN_MESSAGE_PROPERTIES_s message;
       CAN_RX_MESSAGE_TIMING_s timing;
       CAN_RxCallbackFunction_f callbackFunction;
   } CAN_RX_MESSAGE_TYPE_s;

.. list-table::
   :widths: 20 30 50
   :header-rows: 1

   * - Field
     - Type
     - Description
   * - ``canNode``
     - ``CAN_NODE_s *``
     - Expected CAN node for reception
   * - ``message``
     - ``CAN_MESSAGE_PROPERTIES_s``
     - Message ID, type, DLC, and endianness
   * - ``timing``
     - ``CAN_RX_MESSAGE_TIMING_s``
     - Expected period
   * - ``callbackFunction``
     - ``CAN_RxCallbackFunction_f``
     - Callback invoked when message is received

----

CAN_SHIM_s
^^^^^^^^^^

Database access shim — passed to all TX and RX callbacks to provide access to
BMS data tables.

.. code-block:: c

   typedef struct {
       OS_QUEUE *pQueueImd;
       DATA_BLOCK_CELL_VOLTAGE_s      *pTableCellVoltage;
       DATA_BLOCK_CELL_TEMPERATURE_s  *pTableCellTemperature;
       DATA_BLOCK_CURRENT_SENSOR_s    *pTableCurrentSensor;
       DATA_BLOCK_ERROR_STATE_s       *pTableErrorState;
       DATA_BLOCK_INSULATION_MONITORING_s *pTableInsulation;
       DATA_BLOCK_MIN_MAX_s           *pTableMinMax;
       DATA_BLOCK_MOL_FLAG_s          *pTableMol;
       DATA_BLOCK_MSL_FLAG_s          *pTableMsl;
       DATA_BLOCK_OPEN_WIRE_s         *pTableOpenWire;
       DATA_BLOCK_PACK_VALUES_s       *pTablePackValues;
       DATA_BLOCK_RSL_FLAG_s          *pTableRsl;
       DATA_BLOCK_SOC_s               *pTableSoc;
       DATA_BLOCK_SOE_s               *pTableSoe;
       DATA_BLOCK_SOF_s               *pTableSof;
       DATA_BLOCK_SOH_s               *pTableSoh;
       DATA_BLOCK_STATE_REQUEST_s     *pTableStateRequest;
       DATA_BLOCK_AEROSOL_SENSOR_s    *pTableAerosolSensor;
   } CAN_SHIM_s;

This structure provides centralized access to all database tables needed by CAN
callbacks. It is initialized once as a ``const`` instance and passed by pointer to
every callback invocation.

----

CAN_STATE_s
^^^^^^^^^^^^

Internal module state.

.. code-block:: c

   typedef struct {
       bool periodicEnable;
       bool currentSensorPresent[BS_NR_OF_STRINGS];
       bool currentSensorCCPresent[BS_NR_OF_STRINGS];
       bool currentSensorECPresent[BS_NR_OF_STRINGS];
   } CAN_STATE_s;

.. list-table::
   :widths: 30 20 50
   :header-rows: 1

   * - Field
     - Type
     - Description
   * - ``periodicEnable``
     - ``bool``
     - Whether periodic TX is active
   * - ``currentSensorPresent``
     - ``bool[]``
     - Per-string current sensor presence
   * - ``currentSensorCCPresent``
     - ``bool[]``
     - Per-string Coulomb Counting message presence
   * - ``currentSensorECPresent``
     - ``bool[]``
     - Per-string Energy Counting message presence

----

Function Pointer Types
----------------------

CAN_TxCallbackFunction_f
^^^^^^^^^^^^^^^^^^^^^^^^^

TX callback function signature. Called by the periodic transmitter to generate message
payload data.

.. code-block:: c

   typedef uint32_t (*CAN_TxCallbackFunction_f)(
       CAN_MESSAGE_PROPERTIES_s message,
       uint8_t *canData,
       uint8_t *pMuxId,
       const CAN_SHIM_s *const kpkCanShim
   );

**Parameters:**

- ``message`` — Message properties (ID, DLC, endianness)
- ``canData`` — Output: 8-byte buffer to fill with CAN payload
- ``pMuxId`` — Pointer to multiplexer state variable
- ``kpkCanShim`` — Const pointer to database access shim

**Returns:** ``0`` on success, non-zero on error.

----

CAN_RxCallbackFunction_f
^^^^^^^^^^^^^^^^^^^^^^^^^

RX callback function signature. Called when a matching CAN message is received.

.. code-block:: c

   typedef uint32_t (*CAN_RxCallbackFunction_f)(
       CAN_MESSAGE_PROPERTIES_s message,
       const uint8_t *const kpkCanData,
       const CAN_SHIM_s *const kpkCanShim
   );

**Parameters:**

- ``message`` — Message properties (ID, DLC, endianness)
- ``kpkCanData`` — Const pointer to received 8-byte payload
- ``kpkCanShim`` — Const pointer to database access shim

**Returns:** ``0`` on success, non-zero on error.
