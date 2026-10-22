# Psychiatric Note Privacy Gateway and Summarizer

## Overview

This project will create a privacy gateway for a psychiatrist who wants assistance summarizing an already-written psychiatric note.

The gateway will keep selected patient identifiers local by replacing them with placeholders before sending the note to an AI or mock provider. It will then validate the provider’s response and restore only authorized values.

The M2 prototype supports:

- Patient names from a local synthetic term list
- Medical record numbers in the format `MRN-######`
- Repeated and different sensitive values
- Controlled errors for invalid placeholders
- JSON input and output
- Automated tests

Only synthetic, completely fictional information will be used. This project is an educational prototype and is not intended for clinical use.

## Current Status

**M2: Working Prototype** is complete.

The program implements the following pipeline:

`JSON Input → Detection → Masking → Offline Mock Provider → Validation → Restoration → JSON Output`

## Run a Successful Request

From the main project directory, run:

```powershell
python src/main.py examples/request.json
```

If `python` is not available as a command, use the installed Python executable.

The expected result has:

```json
{
  "status": "success",
  "request_id": "r1",
  "masked_text": "Text containing placeholders",
  "provider_response": "A structured response containing placeholders",
  "final_output": "A structured response with authorized values restored"
}
```

The original name and MRN must not appear in `masked_text` or `provider_response`. They should appear only in `final_output`.

## Run the Invalid-Placeholder Example

```powershell
python src/main.py examples/invalid_placeholder.json
```

Expected result:

```json
{
  "status": "error",
  "request_id": "r4",
  "error_code": "INVALID_PLACEHOLDER",
  "message": "Placeholder belongs to another request: [[r4-foreign:NAME:1]]"
}
```

No values are restored when validation fails.

## Run the Automated Tests

```powershell
python -m unittest discover -s tests -v
```

Expected result:

```text
Ran 5 tests

OK
```

The tests cover:

- Ordinary input containing a name and MRN
- A repeated name
- Input with no supported sensitive data
- An invalid foreign-request placeholder
- Two different names in one request

## JSON Input Format

A normal request contains:

```json
{
  "request_id": "r1",
  "text": "Patient Jordan Lee, MRN-482731, reported anxiety. Jordan Lee will return in two weeks."
}
```

The optional `mock_mode` field is used only to simulate an invalid provider response during testing.

## M1 Tech Spike

The M1 Tech Spike confirmed that Python could read and echo plain-text input.

- **Runtime:** Python 3.14.7
- **Source file:** `src/tech_spike.py`
- **Exact command:** `& C:\Users\paige\AppData\Local\Python\pythoncore-3.14-64\python.exe c:/Users/paige/AI_Privacy_Gateway/AI_Privacy_Project/src/tech_spike.py`
- **Input:** `Hello`

Observed output:

```text
Enter a synthetic psychiatric note: Hello
Received note:
Hello
```

## Documentation

- `docs/DESIGN.md`: Requirements, language choice, architecture, prompt, and design decisions
- `docs/EVALUATION.md`: Planned acceptance cases
- `docs/USER_GUIDE.md`: Planned usage and privacy warnings
- `docs/ASSISTANCE.md`: Important assistance and verification
