Signal Handling
===============

This chapter describes how CAN signals are packed into and unpacked from CAN message
frames, including endianness handling and physical-to-raw conversion.

Signal Conversion Overview
--------------------------

CAN signals are encoded as raw integer values within the 64-bit (8-byte) CAN frame.
The CAN helper functions handle the conversion between physical (engineering unit) values
and raw CAN signal values.

.. code-block:: text

   Physical Value ────► Clamp to [min,max] ────► Add offset ────► Divide by factor
        │                                                              │
        │                          TX Path                             │
        │                                                              ▼
        │                                                        Raw CAN Value
        │                                                              │
        │                          RX Path                             │
        │                                                              │
        ▼                                                              ▼
   Physical Value ◄──── Subtract offset ◄──── Multiply by factor ◄────┘

TX Signal Preparation
---------------------

CAN_TxPrepareSignalData
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: c

   void CAN_TxPrepareSignalData(
       float_t *pSignal,
       CAN_SIGNAL_TYPE_s signalProperties
   )

Prepares a physical signal value for CAN transmission.

**Algorithm:**

1. **Clamp** the signal to the configured ``[min, max]`` range
2. **Add** the offset: ``signal = signal + offset``
3. **Divide** by the factor: ``signal = signal / factor``

The result is the raw integer value ready for insertion into the CAN frame.

**Example:**

.. code-block:: c

   /* Signal: Battery voltage, range 0-65535 mV, factor 1.0, offset 0 */
   CAN_SIGNAL_TYPE_s voltageSignal = {
       .bitStart   = 15,
       .bitLength  = 16,
       .factor     = 1.0f,
       .offset     = 0.0f,
       .min        = 0.0f,
       .max        = 65535.0f,
   };

   float_t voltage = 3750.0f;  /* 3750 mV */
   CAN_TxPrepareSignalData(&voltage, voltageSignal);
   /* voltage is now 3750.0 (raw value) */

CAN_TxSetMessageDataWithSignalData
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: c

   void CAN_TxSetMessageDataWithSignalData(
       uint64_t *pMessage,
       uint64_t bitStart,
       uint8_t bitLength,
       uint64_t canSignal,
       CAN_ENDIANNESS_e endianness
   )

Inserts a raw signal value into a 64-bit message buffer at the specified bit position.

**Parameters:**

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Name
     - Type
     - Description
   * - ``pMessage``
     - ``uint64_t *``
     - Pointer to the 64-bit message buffer
   * - ``bitStart``
     - ``uint64_t``
     - Start bit position (0–63)
   * - ``bitLength``
     - ``uint8_t``
     - Signal width in bits
   * - ``canSignal``
     - ``uint64_t``
     - Raw signal value to insert
   * - ``endianness``
     - ``CAN_ENDIANNESS_e``
     - Byte order for signal placement

For big-endian signals, the start bit is converted using the internal lookup table
before insertion.

CAN_TxSetCanDataWithMessageData
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: c

   void CAN_TxSetCanDataWithMessageData(
       uint64_t message,
       uint8_t *pCanData,
       CAN_ENDIANNESS_e endianness
   )

Copies the 64-bit message buffer into the 8-byte CAN data array with appropriate
byte-order handling.

**Byte Mapping (Big-Endian):**

.. code-block:: text

   Message bits [63:56] → pCanData[0]
   Message bits [55:48] → pCanData[1]
   Message bits [47:40] → pCanData[2]
   Message bits [39:32] → pCanData[3]
   Message bits [31:24] → pCanData[4]
   Message bits [23:16] → pCanData[5]
   Message bits [15:8]  → pCanData[6]
   Message bits [7:0]   → pCanData[7]

**Byte Mapping (Little-Endian):**

.. code-block:: text

   Message bits [7:0]   → pCanData[0]
   Message bits [15:8]  → pCanData[1]
   Message bits [23:16] → pCanData[2]
   Message bits [31:24] → pCanData[3]
   Message bits [39:32] → pCanData[4]
   Message bits [47:40] → pCanData[5]
   Message bits [55:48] → pCanData[6]
   Message bits [63:56] → pCanData[7]

RX Signal Extraction
--------------------

CAN_RxGetMessageDataFromCanData
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: c

   void CAN_RxGetMessageDataFromCanData(
       uint64_t *pMessage,
       const uint8_t *const kpkCanData,
       CAN_ENDIANNESS_e endianness
   )

Converts the received 8-byte CAN data array into a 64-bit message buffer.
This is the inverse of ``CAN_TxSetCanDataWithMessageData``.

CAN_RxGetSignalDataFromMessageData
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: c

   void CAN_RxGetSignalDataFromMessageData(
       uint64_t message,
       uint64_t bitStart,
       uint8_t bitLength,
       uint64_t *pCanSignal,
       CAN_ENDIANNESS_e endianness
   )

Extracts a raw signal value from the 64-bit message buffer.

**Parameters:**

.. list-table::
   :widths: 20 20 60
   :header-rows: 1

   * - Name
     - Type
     - Description
   * - ``message``
     - ``uint64_t``
     - 64-bit message buffer
   * - ``bitStart``
     - ``uint64_t``
     - Start bit position
   * - ``bitLength``
     - ``uint8_t``
     - Signal width in bits
   * - ``pCanSignal``
     - ``uint64_t *``
     - Output: extracted raw signal value
   * - ``endianness``
     - ``CAN_ENDIANNESS_e``
     - Byte order for extraction

CAN_RxConvertRawSignalData
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: c

   void CAN_RxConvertRawSignalData(
       float_t *pSignalConverted,
       float_t signalRaw,
       CAN_SIGNAL_TYPE_s signalProperties
   )

Converts a raw CAN signal value to a physical (engineering unit) value.

**Formula:**

.. code-block:: text

   physical = (raw * factor) - offset

Endianness Handling
-------------------

Big-Endian Bit Numbering
^^^^^^^^^^^^^^^^^^^^^^^^^

CAN big-endian (Motorola) byte order uses a non-linear bit numbering scheme.
The driver uses a static 64-element lookup table to convert between big-endian and
little-endian bit positions:

.. code-block:: c

   static const uint8_t can_bigEndianTable[64] = {
        7u,  6u,  5u,  4u,  3u,  2u,  1u,  0u,
       15u, 14u, 13u, 12u, 11u, 10u,  9u,  8u,
       23u, 22u, 21u, 20u, 19u, 18u, 17u, 16u,
       31u, 30u, 29u, 28u, 27u, 26u, 25u, 24u,
       39u, 38u, 37u, 36u, 35u, 34u, 33u, 32u,
       47u, 46u, 45u, 44u, 43u, 42u, 41u, 40u,
       55u, 54u, 53u, 52u, 51u, 50u, 49u, 48u,
       63u, 62u, 61u, 60u, 59u, 58u, 57u, 56u,
   };

**Visual Bit Layout (Big-Endian):**

.. code-block:: text

   Byte 0:  bit7  bit6  bit5  bit4  bit3  bit2  bit1  bit0
   Byte 1:  bit15 bit14 bit13 bit12 bit11 bit10 bit9  bit8
   Byte 2:  bit23 bit22 bit21 bit20 bit19 bit18 bit17 bit16
   Byte 3:  bit31 bit30 bit29 bit28 bit27 bit26 bit25 bit24
   Byte 4:  bit39 bit38 bit37 bit36 bit35 bit34 bit33 bit32
   Byte 5:  bit47 bit46 bit45 bit44 bit43 bit42 bit41 bit40
   Byte 6:  bit55 bit54 bit53 bit52 bit51 bit50 bit49 bit48
   Byte 7:  bit63 bit62 bit61 bit60 bit59 bit58 bit57 bit56

Complete TX Example
-------------------

The following example demonstrates the full TX signal packing workflow:

.. code-block:: c

   uint8_t canData[CAN_MAX_DLC] = {0};
   uint64_t message = 0u;

   /* Pack battery voltage signal (16 bits, starting at bit 15, big-endian) */
   float_t voltage = 48250.0f;  /* 48.25 V in mV */
   CAN_SIGNAL_TYPE_s sig = {
       .bitStart = 15, .bitLength = 16,
       .factor = 1.0f, .offset = 0.0f,
       .min = 0.0f, .max = 65535.0f
   };

   CAN_TxPrepareSignalData(&voltage, sig);
   CAN_TxSetMessageDataWithSignalData(
       &message, sig.bitStart, sig.bitLength,
       (uint64_t)voltage, CAN_BIG_ENDIAN);

   /* Copy to CAN data array */
   CAN_TxSetCanDataWithMessageData(message, canData, CAN_BIG_ENDIAN);

   /* Transmit */
   CAN_DataSend(CAN_NODE_1, 0x233, CAN_STANDARD_IDENTIFIER_11_BIT, canData);

Complete RX Example
-------------------

The following example demonstrates the full RX signal extraction workflow:

.. code-block:: c

   /* In an RX callback function */
   uint64_t message = 0u;
   uint64_t rawSignal = 0u;

   /* Convert CAN data to message buffer */
   CAN_RxGetMessageDataFromCanData(&message, kpkCanData, CAN_BIG_ENDIAN);

   /* Extract 16-bit voltage signal starting at bit 15 */
   CAN_RxGetSignalDataFromMessageData(
       message, 15u, 16u, &rawSignal, CAN_BIG_ENDIAN);

   /* Convert raw to physical */
   float_t physicalVoltage;
   CAN_SIGNAL_TYPE_s sig = {
       .factor = 1.0f, .offset = 0.0f,
       .min = 0.0f, .max = 65535.0f
   };
   CAN_RxConvertRawSignalData(&physicalVoltage, (float_t)rawSignal, sig);

Utility Functions
-----------------

CAN_ConvertBooleanToInteger
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: c

   uint8_t CAN_ConvertBooleanToInteger(bool input)

Converts a boolean value to a CAN-compatible integer (0 or 1).

**Parameters:**

- ``input`` — Boolean value

**Returns:** ``1u`` if input is ``true``, ``0u`` if ``false``.
