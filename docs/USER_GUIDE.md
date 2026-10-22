# User Guide

## 1. Current Project Status

The Psychiatric Note Privacy Gateway is currently in **M2: Working Prototype**.

The prototype implements this complete pipeline:

`JSON Input → Detection → Masking → Offline Mock Provider → Validation → Restoration → JSON Output`

The program runs locally and does not require an API key, network connection, or external Python packages.

## 2. Intended User and Task

The intended user is a psychiatrist who wants assistance summarizing an already-written psychiatric note while preventing selected identifiers from being sent to an external provider.

The planned program will produce a structured summary containing:

- Presenting concern
- Symptoms
- Medication information
- Treatment plan
- Follow-up instructions

This project is an educational prototype and is not intended for real clinical use.

## 3. Requirements

The program requires:

- Python 3
- A terminal or PowerShell
- The project repository
- A valid JSON input file

No additional packages need to be installed.

## 4. Supported Sensitive Data

The M2 prototype supports:

- **Patient names:** Detected through exact matching with the local synthetic term list in `data/names.txt`
- **Medical record numbers:** Detected when they use the format `MRN-######`

An example of a supported MRN is:

```text
MRN-482731
```

Name matching is case-sensitive. A name must appear in `data/names.txt` exactly as it appears in the note.

Date-of-birth detection is planned for M3.

## 5. Input Format

The program reads one JSON request file.

A normal request contains:

- `request_id`: A unique identifier for the request
- `text`: The synthetic psychiatric note

Example:

```json
{
  "request_id": "r1",
  "text": "Patient Jordan Lee, MRN-482731, reported anxiety. Jordan Lee will return in two weeks."
}
```

The optional `mock_mode` field is used only for controlled-error testing:

```json
{
  "request_id": "r4",
  "text": "Jordan Lee reported anxiety.",
  "mock_mode": "invalid_placeholder"
}
```
## 6. Running a Successful Request

Open a terminal in the main project directory and run:

```powershell
python src/main.py examples/request.json
```

The program should return JSON containing:

- `status`
- `request_id`
- `masked_text`
- `provider_response`
- `final_output`

Example masked text:

```text
Patient [[r1:NAME:1]], [[r1:MRN:1]], reported anxiety. [[r1:NAME:1]] will return in two weeks.
```

The original name and MRN should not appear in `masked_text` or `provider_response`. They should appear only in `final_output` after validation succeeds.

## 7. Running the Invalid-Placeholder Example

Run:

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

The program does not return `final_output` or restore sensitive values when validation fails.

## 8. Running the Automated Tests

Run the complete M2 test suite with:

```powershell
python -m unittest discover -s tests -v
```

Expected result:

```text
Ran 5 tests

OK
```

The tests cover:

- A note containing a name and MRN
- A repeated name
- A note containing no supported sensitive values
- An invalid foreign-request placeholder
- Two different names in one request

## 9. Output Format

### Successful Output

A successful result uses:

```json
{
  "status": "success",
  "request_id": "r1",
  "masked_text": "Text containing placeholders",
  "provider_response": "The masked mock-provider response",
  "final_output": "The response with authorized values restored"
}
```

### Error Output

A controlled error uses:

```json
{
  "status": "error",
  "request_id": "r4",
  "error_code": "ERROR_CODE",
  "message": "Description of the error"
}
```

The local placeholder mapping is never included in the JSON output.

## 10. Controlled Errors

The program returns a controlled error when:

- No JSON file path is provided
- The requested file does not exist
- The file does not contain valid JSON
- `request_id` is missing or invalid
- `text` is missing or empty
- `mock_mode` contains an unsupported value
- The mock-provider response contains a malformed, unknown, or foreign placeholder

If placeholder validation fails, the program will not:

- Restore sensitive values
- Return partially restored output
- Resend the original unmasked note

## 11. Privacy and Safety Warnings

- Use only synthetic, completely fictional information.
- Do not enter real patient records or identifying information.
- Do not use the program to diagnose conditions or make treatment decisions.
- Do not assume that the gateway detects every possible sensitive value.
- Names not contained in `data/names.txt` will not be detected.
- MRNs using an unsupported format will not be detected.
- Treat validation errors as failed requests rather than attempting unsafe restoration.

## 12. Troubleshooting

### Python is not recognized

Confirm that Python is installed. Depending on the computer, the command may be `python`, `py`, or a complete path to the Python executable.

### The program reports `FILE_NOT_FOUND`

Confirm that the terminal is open in the main project directory and that the JSON file exists inside `examples`.

### The program reports `INVALID_JSON`

Confirm that:

- All keys and string values use straight double quotation marks
- There is no comma after the final field
- The file does not contain Markdown backticks
- There are no backslashes before underscores
- The file was saved before running the program

The JSON can be checked with:

```powershell
python -m json.tool examples/request.json
```

### A name is not masked

Confirm that:

- The name appears in `data/names.txt`
- The spelling and capitalization match exactly
- The complete name appears in the note

### An MRN is not masked

Confirm that the value uses uppercase `MRN-` followed by exactly six digits:

```text
MRN-482731
```

### The invalid-placeholder example returns an error

This is expected. That example deliberately creates an unauthorized placeholder to prove that the gateway rejects the response without restoring sensitive values.

