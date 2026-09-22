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
