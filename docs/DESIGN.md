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
- **Medical record number:** Detected through a regular-expression pattern.
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

## 5. M2 Scope

M2 will implement one complete pipeline:

`Input → Detection → Masking → Offline Mock Provider → Validation → Restoration → Output`

The M2 prototype will:

- Read one fictional plain-text psychiatric note.
- Detect patient names using a local term list.
- Detect medical record numbers using a regular expression.
- Replace detected values with request-specific placeholders.
- Store the placeholder mapping locally.
- Send the masked note to a deterministic offline mock provider.
- Validate the response before restoring authorized values.
- Return either a structured summary or a controlled error.

Date-of-birth detection and complete `MASK` and `REMOVE` policy behavior will be added during M3.

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

Python was selected because its text-processing features and development speed best match this project. Type hints, validation, and automated tests will be used to reduce the risks of dynamic typing.

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

The provider may receive:

- The summarization prompt
- The masked note
- Request-specific placeholders
- Clinical content needed for summarization

Before restoration, every placeholder must be correctly formatted, belong to the current request, and exist in that request’s mapping.

### Component Responsibilities

- **Input handler:** Reads one plain-text note.
- **Detector:** Locates supported sensitive values.
- **Masking and mapping components:** Create placeholders and store their local mappings.
- **Prompt builder:** Combines the prompt with the masked note.
- **Mock provider:** Produces a predictable offline summary.
- **Response validator:** Rejects invalid or unauthorized placeholders.
- **Restoration component:** Restores authorized values.
- **Output handler:** Displays the summary or controlled error.

## 8. Placeholder Design

Placeholders will use this format:

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

## 10. Key Design Decisions

- The program will use a command-line interface and plain-text input.
- Only fictional information created for testing will be used.
- Placeholder mappings will remain local and separate for each request.
- A deterministic offline mock provider will make testing reproducible without requiring an API.

## 11. M1 Tech Spike

A small Python Tech Spike was completed to confirm that the selected runtime could read and echo plain-text input.

- **Runtime:** Python [INSERT EXACT VERSION]
- **Source file:** `src/tech_spike.py`
- **Exact command:** `[INSERT EXACT COMMAND USED]`
- **Input:** `Patient Jordan Lee reported increased anxiety.`

**Observed output:**

```text
Enter a synthetic psychiatric note: Patient Jordan Lee reported increased anxiety.
Received note:
Patient Jordan Lee reported increased anxiety.
```

The output matched the entered text, confirming that the Python runtime and basic command-line input/output worked correctly.