# User Guide

## 1. Current Project Status

The Psychiatric Note Privacy Gateway is currently in the M1 requirements and design stage. The complete gateway has not yet been implemented.

A small Python Tech Spike has been completed to confirm that the selected runtime can read and echo plain-text input. This guide will be updated during later milestones as gateway features are implemented.

## 2. Intended User and Task

The intended user is a psychiatrist who wants assistance summarizing an already-written psychiatric note while preventing selected identifiers from being sent to an external provider.

The planned program will produce a structured summary containing:

- Presenting concern
- Symptoms
- Medication information
- Treatment plan
- Follow-up instructions

This project is an educational prototype and is not intended for real clinical use.

## 3. Planned Workflow

The user will provide one fictional psychiatric note as plain text.

The gateway will:

1. Detect supported sensitive values locally.
2. Replace protected values with placeholders.
3. Send only the masked note to the provider.
4. Validate placeholders in the provider response.
5. Restore authorized values locally.
6. Display the final summary or a controlled error.

## 4. Input and Output

### Planned Input

The program will accept one fictional psychiatric note as plain text.

Example:

> Patient Jordan Lee, MRN-482731, reported increased anxiety and difficulty sleeping for the past two weeks. The patient is taking sertraline as prescribed. The plan is to continue the current medication and return in two weeks.

The program will not initially accept:

- Audio recordings
- Handwritten or scanned notes
- Multiple patient notes in one request
- Multi-turn conversations
- Real patient records

### Planned Output

The summary will use the following headings:

- Presenting Concern
- Symptoms
- Medication
- Treatment Plan
- Follow-Up

Example:

> **Presenting Concern:** Jordan Lee reports increased anxiety and difficulty sleeping.
>
> **Symptoms:** Anxiety and difficulty sleeping for the past two weeks.
>
> **Medication:** The patient is taking sertraline as prescribed.
>
> **Treatment Plan:** Continue the current medication.
>
> **Follow-Up:** Return in two weeks.

If information for a heading is missing, the output should state `Not provided`.

## 5. Planned Sensitive-Data Support

The completed gateway will support:

- Patient names
- Medical record numbers
- Dates of birth

The M2 prototype will initially support:

- Patient names detected with a local fictional term list
- Medical record numbers detected with a regular-expression pattern

Date-of-birth detection is planned for M3.

## 6. Privacy and Safety Warnings

- Use only synthetic, completely fictional information.
- Do not enter real patient records or identifying information.
- Do not use the program to diagnose conditions or make treatment decisions.
- Do not assume that the gateway detects every possible sensitive value.
- Do not send an unmasked note as a fallback if the provider fails.
- Treat validation errors as failed requests rather than attempting unsafe restoration.
 

## 7. Planned Error Behavior

The working gateway will return a controlled error if the provider response contains a malformed, unknown, or unauthorized placeholder.

If validation fails, the program will not:

- Restore any sensitive values
- Display a partially restored response
- Resend the original unmasked note

