# Assistance Record

## Purpose

This document records important assistance received while developing the Psychiatric Note Privacy Gateway. For each important suggestion, it identifies the source, the decision made, and how the suggestion was checked.

## Entry 1: Project Scope and M1 Planning

- Source: ChatGPT
- Suggestion: Narrow the original psychiatry-related idea to a command-line privacy gateway that summarizes one already-written psychiatric note. ChatGPT suggested separating the gateway into detection, masking, provider, validation, and restoration responsibilities. 
- Decision: I accepted the general project structure because it created one specific user and one manageable AI-assisted task. I decided that the completed gateway will support patient names, medical record numbers, and dates of birth. To keep M2 manageable, its first prototype will focus on patient names and medical record numbers.
- Verification: I compared the suggestions with the project handbook. I confirmed that the design identifies one user, one narrow task, at least three final sensitive-data categories, exact term-list matching, a structured pattern, local placeholder mappings, and an offline mock provider. I also removed unnecessary features such as audio transcription, image processing, and a graphical interface.
- Result: The planning assistance helped me define the project’s scope, privacy boundary, components, and milestone plan. I reviewed and modified the suggestions to ensure that the final design matched the project requirements.


## Entry 2: Language Selection

- Source: ChatGPT
- Suggestion: Use Python for implementation and compare it with Java. The suggested trade-offs included string processing, type systems, JSON support, and development speed.
- Decision: I accepted Python as the planned implementation language because the project relies heavily on string processing, regular expressions, dictionaries, JSON, and automated testing.
- Verification: I checked that Python provides regular expressions through the standard `re` module and JSON support through the standard `json` module. I will verify that the required Python runtime is installed by completing the M1 Tech Spike and recording the version, command, input, and observed output.
- Result: Python remains the selected language, but the decision will be confirmed by successfully completing the Tech Spike.


## Entry 3: M2 Pipeline Implementation 

- Source: ChatGPT
- Suggestion: Build the M2 prototype in small checkpoints instead of attempting the entire gateway at once. The suggested order was term-list loading, detection, masking, mock-provider behavior, validation, restoration, JSON input and output, and automated testing.
- Decision: I accepted this approach because each part of the pipeline could be implemented and tested before moving to the next part. I used separate functions for loading names, detecting values, masking values, producing a mock response, validating placeholders, restoring values, creating errors, and processing the complete request.
- Verification: I ran the program after each checkpoint. I confirmed that the detector found a repeated name and MRN, the masker reused the same placeholder for repeated values, the mock provider received only masked text, and restoration occurred only after successful validation.
- Result: The completed prototype now runs one request through the full M2 pipeline from JSON input to JSON output.


## Entry 4: JSON Format and Controlled Errors

- Source: ChatGPT
- Suggestion: Use a small documented JSON format containing `request_id` and `text`, with an optional `mock_mode` field for controlled-error testing. Successful results contain the masked text, provider response, and final output. Error results contain an error code and message.
- Decision: I used this format because a separate shared JSON I/O Contract was not available with the M2 materials. I documented the format in the README, design document, and user guide.
- Verification: I ran `examples/request.json` and received a successful JSON result. I also ran `examples/invalid_placeholder.json` and received an `INVALID_PLACEHOLDER` error without a `final_output` field.
- Result: The program now provides consistent JSON success and error results. Invalid placeholders are rejected without restoring sensitive values.


## Entry 5: Automated Test Design

- Source: ChatGPT
- Suggestion: Convert the M1 acceptance cases into automated tests using Python’s built-in `unittest` framework. The suggested tests covered ordinary input, repeated values, no sensitive data, an invalid placeholder, and different names in one request.
- Decision: I accepted the test structure and adjusted the fixtures to match the synthetic names and MRN format supported by my implementation.
- Verification: I ran the test suite with:

  `python -m unittest discover -s tests -v`

  All five tests passed.
- Result: The automated tests confirm that the M2 prototype performs masking, repeated-value handling, different-entity handling, validation, controlled errors, and restoration as expected.