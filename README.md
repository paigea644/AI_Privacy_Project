# Psychiatric Note Privacy Gateway and Summarizer

## Overview

This project will create a privacy gateway for a psychiatrist who wants assistance summarizing an already-written psychiatric note.

The gateway will keep selected patient identifiers local by replacing them with placeholders before sending the note to an AI or mock provider. It will then validate the provider’s response and restore only authorized values.

The completed system will support:

- Patient names
- Medical record numbers
- Dates of birth

Only synthetic, completely fictional information will be used. This project is an educational prototype and is not intended for clinical use.

## Current Status

The project is currently in **M1: Requirements and Design**. The complete privacy gateway has not yet been implemented.

The M1 Tech Spike has been completed successfully.

## M1 Tech Spike

The Tech Spike confirms that Python can read and echo plain-text input.

- **Python version:** `Python 3.14.7`
- **Source file:** `src/tech_spike.py`

Example input:

```text
Patient Jordan Lee reported increased anxiety.
```

Observed output:

```text
Enter a synthetic psychiatric note: Patient Jordan Lee reported increased anxiety.
Received note:
Patient Jordan Lee reported increased anxiety.
```

## Documentation

- `docs/DESIGN.md`: Requirements, language choice, architecture, prompt, and design decisions
- `docs/EVALUATION.md`: Planned acceptance cases
- `docs/USER_GUIDE.md`: Planned usage and privacy warnings
- `docs/ASSISTANCE.md`: Important assistance and verification