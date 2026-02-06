.. meta::
   :description: CAN Interface Specification for Battery Management System
   :keywords: CAN, BMS, DCAN, interface, specification

====================================================
CAN Interface Specification
====================================================

.. raw:: html

   <div style="margin-bottom: 2em;">
   <p class="cover-subtitle">Battery Management System &mdash; CAN Driver Module Reference</p>
   <table class="doc-info-table">
   <tr><td>Document Number</td><td>INVI-CAN-REF-001C</td></tr>
   <tr><td>Release</td><td>1.0.0</td></tr>
   <tr><td>Date</td><td>February 2026</td></tr>
   <tr><td>Status</td><td>Released</td></tr>
   </table>
   </div>

This document describes the Controller Area Network (CAN) driver interface for the foxBMS 2
Battery Management System. It provides a complete specification of the CAN module
architecture, API functions, data types, message definitions, and configuration options.

The CAN driver supports the CAN 2.0B protocol specification with bitrates up to 1 Mbit/s
and is designed for automotive and industrial battery management applications operating in
electrically noisy environments.

.. toctree::
   :maxdepth: 3
   :caption: Contents
   :numbered:

   overview
   architecture
   initialization
   api_reference
   data_types
   message_definitions
   signal_handling
   error_handling
   configuration
   appendix
