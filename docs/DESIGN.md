# Psychiatric Note Privacy Gateway and Summarizer

## 1. User, Task, and Motivation

### Intended User

The intended user is a psychiatrist who wants assistance summarizing notes from a patient encounter.

### AI-Assisted Task

The program will convert one fictional psychiatric session note into a structured summary containing the presenting concern, symptoms, medication information, treatment plan, and follow-up instructions.

### Motivation

Psychiatric notes may contain identifiers that are unnecessary for summarization. This project explores whether patient identifiers can remain on the local machine while a masked version of the note is processed by an AI or mock provider.

The gateway will detect sensitive values, replace them with placeholders, validate the provider’s response, and restore only placeholders authorized for the current request.

## 2. Sensitive-Data Categories

The completed gateway will support three sensitive-data categories:

- **Patient name:** Detected through exact matching with a local fictional term list.
- **Medical record number:** Detected through a regular-expression pattern. The MRN pattern supports prefix `MRN-` followed by exactly six digits, such as `MRN-482731`.
- **Date of birth:** Detected through a regular-expression pattern.

Symptoms, medications, treatment plans, and follow-up instructions will remain visible because the provider needs this clinical content to produce a useful summary.

Only fictional information created for this project will be used.

## 3. Success Criteria

The project will be successful if:

- Supported identifiers are detected and do not appear in the outbound request.
- Detected values are replaced with request-specific placeholders.
- Repeated values use the same placeholder within one request.
- The provider returns a useful structured summary.
- Only valid placeholders belonging to the current request are restored.
- Invalid placeholders produce a controlled error without an unmasked fallback.

## 4. Non-Goals

This project will not:

- Process real patient records.
- Diagnose psychiatric conditions or recommend treatment.
- Replace a clinician’s judgment.
- Transcribe audio or extract text from images.
- Support multiple patients or multi-turn conversations.
- Provide a graphical interface.
- Guarantee compliance with all medical privacy regulations.

This is an educational prototype and is not intended for clinical use.


## 5. M2 Scope and Implementation

Milestone 2 implements one complete, single-request pipeline:

`JSON Input → Detection → Masking → Offline Mock Provider → Validation → Restoration → JSON Output`

The prototype supports two sensitive-data categories:

- Patient names detected through exact matching with a local synthetic term list
- Medical record numbers detected with the pattern `\bMRN-\d{6}\b`

For each request, the gateway:

1. Reads a synthetic note from a JSON file.
2. Detects supported names and medical record numbers.
3. Replaces detected values with request-specific placeholders.
4. Creates a local placeholder mapping.
5. Sends only the masked note to the deterministic offline mock provider.
6. Validates every reserved placeholder in the provider response.
7. Restores authorized values after the complete response passes validation.
8. Returns a successful JSON result or a controlled JSON error.

Repeated occurrences of the same value use the same placeholder. Different values receive different placeholders.

Date-of-birth detection remains planned for M3.

### Detection and Masking

Each detection records its category, original value, starting position, and ending position.

Detected values are replaced using this format:

`[[request-id:CATEGORY:number]]`

Examples include:

- `[[r1:NAME:1]]`
- `[[r1:NAME:2]]`
- `[[r1:MRN:1]]`

Repeated occurrences of the same value use the same placeholder. Different values receive different placeholders.

For example:

```text
Jordan Lee, MRN-482731, reported anxiety. Jordan Lee will return in two weeks.
```

becomes:

```text
[[r1:NAME:1]], [[r1:MRN:1]], reported anxiety. [[r1:NAME:1]] will return in two weeks.
```

The local mapping for this request would contain:

```python
{
    "[[r1:NAME:1]]": "Jordan Lee",
    "[[r1:MRN:1]]": "MRN-482731"
}
```

The mapping remains local. It is not sent to the mock provider or included in the JSON output.

Date-of-birth detection, `MASK` and `REMOVE` policy behavior, overlap handling, and full cross-request isolation are deferred until M3.

## 6. Language and Runtime Choice

### Selected Language: Python

Python was selected because the project primarily involves text processing, regular expressions, dictionaries, JSON, and automated testing.

### Alternative Language: Java

Java could implement the same gateway and offers stronger compile-time type checking. However, it generally requires more setup and supporting code for a small text-processing prototype.

### Trade-Off Comparison

- **String processing:** Python provides concise string and regular-expression operations. Java supports the same operations but usually requires more code.

- **Type system:** Python’s dynamic typing supports rapid development, while Java’s static typing can catch more errors during compilation.

- **JSON support:** Python includes JSON support in its standard library. Java commonly uses an additional library such as Jackson or Gson.

- **Development speed:** Python requires less setup and boilerplate for a small command-line application. Java’s additional structure may be more useful in a larger system.

Python was selected because its text-processing features and development speed match this project. Input validation and automated tests help reduce the risks of dynamic typing.

## 7. System Design

### Data Flow

The user provides one plain-text note. The gateway detects and masks sensitive values locally, sends only the masked note to the provider, validates the returned placeholders, restores authorized values locally, and displays the final summary.

`Original note → Detection → Masking → Provider → Validation → Restoration → Final summary`

### Privacy Boundary

The following must remain local:

- The original note
- Original sensitive values
- The local term list
- The placeholder mapping
- Validation and restoration operations

The future external provider may receive:

- The summarization prompt
- The masked note
- Request-specific placeholders
- Clinical content needed for summarization

The M2 mock provider receives only the masked note. It uses fixed keyword rules to create a predictable structured response without calling an external service.

Before restoration, every placeholder must be correctly formatted, belong to the current request, and exist in that request’s mapping.

### Implemented Components

- **`src/main.py`:** Reads one JSON request file, calls the gateway pipeline, and prints one JSON result.
- **`process_request()`:** Coordinates the complete request pipeline.
- **`load_names()`:** Loads the local synthetic term list from `data/names.txt`.
- **`detect_sensitive_data()`:** Detects exact names and structured MRNs.
- **`mask_sensitive_data()`:** Creates placeholders and the request-local mapping.
- **`mock_provider()`:** Produces a deterministic structured summary without using a network or real AI API.
- **`validate_provider_response()`:** Rejects malformed, unknown, and foreign-request placeholders.
- **`restore_sensitive_data()`:** Restores authorized values after successful validation.
- **`create_error()`:** Produces consistent JSON-compatible error results.

The placeholder mapping exists only within the processing of the current request. It is not included in the provider input or returned in the JSON output.

## 8. Placeholder Design

The M2 prototype uses this placeholder format:

`[[request-id:CATEGORY:number]]`

For example:

`[[r1:NAME:1]]`

The original note:

`Jordan Lee, MRN-482731, reported increased anxiety. Jordan Lee also reported difficulty sleeping.`

would become:

`[[r1:NAME:1]], [[r1:MRN:1]], reported increased anxiety. [[r1:NAME:1]] also reported difficulty sleeping.`

Repeated occurrences of the same value use the same placeholder. A placeholder will be restored only if it is correctly formatted, belongs to the current request, and exists in the local mapping.

## 9. Initial Provider Prompt

### Prompt Version 1

> Summarize the following fictional psychiatric note using the headings Presenting Concern, Symptoms, Medication, Treatment Plan, and Follow-Up. Include only information found in the note. Do not diagnose the patient, recommend new treatment, or invent missing information. Preserve every placeholder exactly as written. If information for a heading is missing, write “Not provided.”

The masked note will be appended as:

`Note: {masked_note}`

This prompt is intended to create a predictable summary while preserving the placeholders required by the gateway.

The M2 mock provider does not interpret this prompt like a real AI model. Instead, it uses deterministic keyword rules to organize the masked note under the same headings. This allows the masking, validation, and restoration pipeline to be tested without a network connection or API.

## 10. Key Design Decisions

- The program reads synthetic note text from a JSON request file.
- Only fictional information created for testing is used.
- Placeholder mappings remain local to the current request.
- The deterministic offline mock provider makes testing reproducible without an API or network connection.
- The complete provider response is validated before any values are restored.
- JSON file handling is separated into `src/main.py`, while gateway behavior is implemented in `src/gateway.py`.
- The optional `invalid_placeholder` mock mode exists only to test controlled-error behavior.

## 11. M1 Tech Spike

A small Python Tech Spike was completed to confirm that the selected runtime could read and echo plain-text input.

- **Runtime:** Python 3.14.7 (64-bit)
- **Source file:** `src/tech_spike.py`
- **Exact command:** `& C:\Users\paige\AppData\Local\Python\pythoncore-3.14-64\python.exe c:/Users/paige/AI_Privacy_Gateway/AI_Privacy_Project/src/tech_spike.py`
- **Input:** `Patient Jordan Lee reported increased anxiety.`

**Observed output:**

```text
Enter a synthetic psychiatric note: Patient Jordan Lee reported increased anxiety.
Received note:
Patient Jordan Lee reported increased anxiety.
```

The output matched the entered text, confirming that the Python runtime and basic command-line input/output worked correctly. 