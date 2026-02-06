# foxBMS 2 — C Coding Guidelines

Apply these rules whenever writing, editing, or reviewing C source (`.c`) and header (`.h`) files in this repository. The rules are derived from `docs/developer-manual/style-guide/guidelines_c.rst`, the `.clang-format` configuration, the file templates in `conf/tpl/`, and the Axivion static-analysis rules.

---

## 1. General file rules (GENERAL:001–006)

- Filenames: lowercase alphanumeric, underscores, dashes, dots only (`^[a-z0-9_\-.]*$`).
- Source filenames MUST be unique across the entire repository.
- C/H files MUST use **ASCII** encoding (not UTF-8).
- Files MUST end with exactly one newline (POSIX 3.206).
- No trailing whitespace.
- Indentation: **4 spaces**, never tabs.

## 2. Filenames (C:001)

- C sources: `.c`, headers: `.h`, assembler: `.asm`.
- Configuration files end with `_cfg.c` / `_cfg.h`.
- Example: `driver.c`, `driver.h`, `driver_cfg.c`, `driver_cfg.h`.

## 3. License header (C:002)

Every `.c` and `.h` file MUST start with the BSD-3-Clause license block exactly as in `conf/tpl/c.c` (lines 1–40). Do not modify the license text.

## 4. File-level Doxygen (C:004)

Immediately after the license block, add a Doxygen comment with these tags (whitespace-aligned):

```c
/**
 * @file    <filename>
 * @author  foxBMS Team
 * @date    YYYY-MM-DD (date of creation)
 * @updated YYYY-MM-DD (date of last update)
 * @version v1.7.0
 * @ingroup <UPPERCASE_GROUP>
 * @prefix  <PREFIX>
 *
 * @brief   <one-line summary>
 * @details <detailed description>
 */
```

- `@prefix`: 2–5 uppercase alphanumeric characters starting with a letter.
- `@ingroup` and `@prefix` use uppercase alphanumeric + underscores.
- `@date` / `@updated`: ISO 8601 date followed by `(date of creation)` or `(date of last update)`.
- Blank line after `@prefix`, after `@brief`, and after `@details`.
- Doxygen comment lines SHOULD stay within **80 characters**.

## 5. Include guard (C:005)

All `.h` files MUST use `#ifndef`-style include guards (never `#pragma once`):

```c
#ifndef FOXBMS__<UPPERCASE_FILENAME>_H_
#define FOXBMS__<UPPERCASE_FILENAME>_H_

/* ... content ... */

#endif /* FOXBMS__<UPPERCASE_FILENAME>_H_ */
```

- Format: `FOXBMS__` + uppercase filename (dots/dashes become underscores) + `_H_`.
- No blank line between `#ifndef` and `#define`; one blank line after `#define`.

## 6. Section markers (C:006)

### Source files (`.c`)

```c
/*========== Includes =======================================================*/
/*========== Macros and Definitions =========================================*/
/*========== Static Constant and Variable Definitions =======================*/
/*========== Extern Constant and Variable Definitions =======================*/
/*========== Static Function Prototypes =====================================*/
/*========== Static Function Implementations ================================*/
/*========== Extern Function Implementations ================================*/
/*========== Externalized Static Function Implementations (Unit Test) =======*/
#ifdef UNITY_UNIT_TEST
#endif
```

### Header files (`.h`)

```c
/*========== Includes =======================================================*/
/*========== Macros and Definitions =========================================*/
/*========== Extern Constant and Variable Declarations ======================*/
/*========== Extern Function Prototypes =====================================*/
/*========== Externalized Static Functions Prototypes (Unit Test) ===========*/
#ifdef UNITY_UNIT_TEST
#endif
```

All sections MUST appear in the order shown above, even if empty.

## 7. Includes (C:007)

- Use **include-what-you-use** — only include what is needed, no forward declarations.
- **Source files**: first include the corresponding header, then a blank line, then remaining includes sorted by priority.
- **Header files**: first `general.h` (if needed), then the corresponding `_cfg.h` (if it exists), then a blank line, then remaining includes sorted.
- Sorting priority (lower number = earlier):
  1. `general.h`
  2. `unity.h` (unit tests only)
  3. Mock headers (unit tests only)
  4. `*_cfg.h`
  5. HAL headers (`HL_*`, `ti_*`)
  6. FreeRTOS headers (starting with `FreeRTOS.h`)
  7. All other headers

## 8. Line length (C:003)

- Code lines: **120 characters** max (exceptions: URLs, raw string literals).
- Doxygen comment lines: **80 characters** max.

## 9. Formatting (C:031)

- **1TBS** (One True Brace Style) — opening brace on the same line.
- Enforced by `.clang-format` at the repository root (based on LLVM, column limit 120, 4-space indent).
- Pointer asterisk adjacent to the variable name: `uint8_t *pData` (PointerAlignment: Right).
- `BinPackArguments: false`, `BinPackParameters: false` — one argument per line when they don't fit on one line.

## 10. Scoping (C:008)

- Declare everything in the **narrowest scope** possible.
- File-private functions, variables, macros: use `static`.
- Public API: use `extern` explicitly on both prototype and definition.

## 11. Function names (C:009)

- `PREFIX_VerbNoun` — **Pascal Case** after the uppercase module prefix.
- Verb-noun pattern preferred: `SOA_CheckVoltages`, `ALGO_RunCyclic`.
- The prefix matches the file's `@prefix` Doxygen tag.

## 12. Function scopes (C:010)

- Public functions: declare with `extern` in the header, define with `extern` in the source.
- Private functions: declare with `static` in the source (in the Static Function Prototypes section).

## 13. Function Doxygen (C:011)

- Doxygen goes **above the prototype**, not above the implementation.
- Required tags: `@brief`, `@details`.
- `@return` required if return type is not `void`.
- `@param[in]`, `@param[out]`, `@param[in,out]` for pointer parameters.
- Plain `@param` (no direction suffix) for pass-by-value parameters.
- All parameter arguments MUST be whitespace-aligned.

## 14. Return statements (C:012)

- Do NOT wrap the return expression in parentheses unless needed for clarity in complex expressions.

## 15. Function parameter checking (C:015)

- Check input values at the start of the function.
- Pointer parameters MUST be checked against `NULL_PTR`: `FAS_ASSERT(pData != NULL_PTR);`
- Use `FAS_ASSERT()` for assertions.

## 16. Variable names (C:016)

- **camelCase** starting lowercase.
- File-scope / static variables MUST start with the **lowercase module prefix**: `abc_cellVoltage`.
- Physical-unit suffix using SI symbols: `_mA`, `_mV`, `_K`, `_ms`, `_degC`, `_perc`.
- All static and global variables MUST have a Doxygen comment.

## 17. Constant names (C:017)

- Module prefix + leading `k` + camelCase: `abc_kDaysInAWeek`.

## 18. Pointer names (C:018)

- Pointer: prefix `p` — `pData`.
- Function pointer: prefix `fp` — `fpCallback`. Function pointer types MUST be typedef'd with suffix `_f`.
- Const pointer: `kp`; pointer to const: `pk`; const pointer to const: `kpk`.
- Asterisk adjacent to the variable name: `uint8_t *pData`.

## 19. Variable initialization (C:019)

- Initialize all variables at declaration.
- One variable per line (no multi-declarations).
- Use correct literal suffixes: `uint8/16/32_t` → `u`, `uint64_t` → `uLL`, `int64_t` → `LL`, `float_t` → `f`.
- Pointers: initialize with `NULL_PTR` if no other valid value.
- Hex digits MUST be uppercase (C:020): `0xABu`.
- Floating-point: always digits on both sides of the radix: `1.0f` not `1.f` (C:021).

## 20. Structs (C:022)

```c
/** Brief description of the struct */
typedef struct {
    uint16_t member1; /*!< description of member1 */
    uint16_t member2; /*!< description of member2 */
} ABC_EXAMPLE_s;
```

- Name: `PREFIX_DESCRIPTION_s` (all uppercase, underscore-separated, `_s` suffix).
- Anonymous structs forbidden — define the tag as the name without `_s`.
- Trailing comma after last member.

## 21. Enums (C:023)

```c
/** Brief description of the enum */
typedef enum {
    ABC_FIRST_VALUE,  /*!< description */
    ABC_SECOND_VALUE, /*!< description */
    ABC_EXAMPLE_E_MAX /*!< max guard — no trailing comma */
} ABC_EXAMPLE_e;
```

- Name: `PREFIX_DESCRIPTION_e` (all uppercase, `_e` suffix).
- Members: all uppercase with module prefix.
- Do NOT assign explicit values.
- Last member: replace `_e` with `_E_MAX` (no trailing comma on this entry).

## 22. Typedefs (C:024)

- All uppercase with underscores.
- General typedefs end with `_t`; structs with `_s`; enums with `_e`; function pointers with `_f`.

## 23. Macros (C:025)

- ALL_CAPS with module prefix: `ABC_MY_CONSTANT`.
- Value macros MUST wrap the value in parentheses: `#define ABC_TIMEOUT_ms (100u)`.
- Physical-unit suffix on the name: `_ms`, `_mV`, `_A`, `_F`, etc.
- Function-like macros are NOT recommended.

## 24. Conditionals (C:026)

- `if` / `else` on separate lines.
- No spaces inside parentheses; space between keyword and `(`.
- Multi-clause conditions: each clause in its own parentheses, logical operator at end of line.

## 25. Switch statements (C:027)

- Every case MUST end with `break` (no fall-through unless empty fall-through, which must be annotated).
- Case blocks MUST NOT use braces.
- `default` case is mandatory; if it should never execute, treat it as an error (`FAS_ASSERT(FAS_TRAP)`).
- Empty line between `break;` and next `case`.

## 26. Loops (C:028)

- Braces required for all loops, even single-statement bodies.
- Empty loop bodies: use `{ }` with an explanatory comment.
- Special counter variables for battery-system loops:
  - `BS_NR_OF_STRINGS` → counter `s`
  - `BS_NR_OF_MODULES_PER_STRING` → counter `m`
  - `BS_NR_OF_CELL_BLOCKS_PER_MODULE` → counter `cb`
  - `BS_NR_OF_TEMP_SENSORS_PER_MODULE` → counter `ts`

## 27. Comments (C:029)

- Only ANSI-C comments: `/* */`. No `//` comments.
- Comments MUST NOT be nested.

## 28. Forbidden functions (Axivion rules)

The following standard library functions are **forbidden**:

- `stdlib.h`: `malloc`, `free`, `calloc`, `realloc` (no dynamic memory allocation).
- `stdio.h`: any `*printf*` function.
- `string.h`: any `str*` function that is not length-bounded (use `strn*` variants).

## 29. Types

- Use `<stdint.h>` fixed-width types: `uint8_t`, `uint16_t`, `uint32_t`, `int16_t`, etc.
- Use `float_t` (not bare `float`). Prefer `float` over `double` (hardware FPU support).
- Use `NULL_PTR` (defined as `((void *)(0u))`) instead of `NULL`.
- Use `STD_OK` / `STD_NOT_OK` from `STD_RETURN_TYPE_e` for return values.

## 30. Error handling

- Use `FAS_ASSERT(condition)` for runtime assertions.
- Use `FAS_ASSERT(FAS_TRAP)` to unconditionally trap (e.g., unreachable default cases).
- Check all pointer parameters against `NULL_PTR` at function entry.

## 31. Unit testing

- The `UNITY_UNIT_TEST` section at the end of each file externalizes static functions for testing.
- Use `UNIT_TEST_WEAK_IMPL` for weak implementations replaceable in tests.
- Unit test functions must start with `test` (Ceedling requirement).
