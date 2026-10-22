# Evaluation Plan

## 1. Purpose

This evaluation will determine whether the Psychiatric Note Privacy Gateway protects supported sensitive values while still producing a useful summary.

All tests will use synthetic, meaning completely fictional, patient information created for this project. No real patient information will be used.

The acceptance cases originally planned during M1 have now been implemented as automated M2 tests.

## 2. Test Environment

The tests use Python’s built-in `unittest` framework and require no external packages, API key, or network connection.

The test suite is run from the main project directory with:

```powershell
python -m unittest discover -s tests -v
```

Five automated tests were executed.

Observed result:

```text
Ran 5 tests

OK
```

## 3. Executed Acceptance Cases

### Case 1: Ordinary Input

**Purpose:** Verify that the gateway detects and masks a supported patient name and medical record number.

**Input:**

```text
Patient Jordan Lee, MRN-482731, reported anxiety.
```

**Expected masked text:**

```text
Patient [[r1:NAME:1]], [[r1:MRN:1]], reported anxiety.
```

**Checks performed:**

- The request returned a `success` status.
- `Jordan Lee` did not appear in `masked_text`.
- `MRN-482731` did not appear in `masked_text`.
- Neither original value appeared in `provider_response`.
- Both values appeared in `final_output` after successful validation.

**Observed result:** Passed

The original name and MRN were protected from the mock provider and restored locally in the final output.

---

### Case 2: Repeated Sensitive Value

**Purpose:** Verify that repeated occurrences of the same sensitive value use the same placeholder.

**Input:**

```text
Jordan Lee reported anxiety. Jordan Lee will return next week.
```

**Expected masked text:**

```text
[[r2:NAME:1]] reported anxiety. [[r2:NAME:1]] will return next week.
```

**Checks performed:**

- The request returned a `success` status.
- `[[r2:NAME:1]]` appeared twice.
- `[[r2:NAME:2]]` was not created.

**Observed result:** Passed

Both occurrences of `Jordan Lee` used the same placeholder.

---

### Case 3: No Sensitive Data

**Purpose:** Verify that a note without a supported name or MRN is handled correctly.

**Input:**

```text
The patient reported anxiety and will return next week.
```

**Expected masked text:**

The masked text should be identical to the original text because no supported sensitive values are present.

**Checks performed:**

- The request returned a `success` status.
- The masked text matched the original input.
- No placeholder syntax appeared in the masked text.
- The absence of sensitive data was not treated as an error.

**Observed result:** Passed

The gateway processed the request without creating or restoring placeholders.

---

### Case 4: Invalid Placeholder Response

**Purpose:** Verify that the gateway rejects a placeholder that does not belong to the current request.

**Input:**

```text
Jordan Lee reported anxiety.
```

The test uses:

```json
{
  "mock_mode": "invalid_placeholder"
}
```

The mock provider adds this foreign-request placeholder:

```text
[[r4-foreign:NAME:1]]
```

**Expected result:**

The gateway should return a controlled error, restore no sensitive values, and omit `final_output`.

**Observed output:**

```json
{
  "status": "error",
  "request_id": "r4",
  "error_code": "INVALID_PLACEHOLDER",
  "message": "Placeholder belongs to another request: [[r4-foreign:NAME:1]]"
}
```

**Checks performed:**

- The result had an `error` status.
- The error code was `INVALID_PLACEHOLDER`.
- No `final_output` field was returned.
- No partially restored response was displayed.
- No unmasked fallback request was sent.

**Observed result:** Passed

---

### Case 5: Different Names in One Request

**Purpose:** Verify that different sensitive values in the same category receive different placeholders.

**Input:**

```text
Jordan Lee listed Avery Brooks as an emergency contact.
```

**Expected masked text:**

```text
[[r5:NAME:1]] listed [[r5:NAME:2]] as an emergency contact.
```

**Checks performed:**

- The request returned a `success` status.
- `[[r5:NAME:1]]` appeared in the masked text.
- `[[r5:NAME:2]]` appeared in the masked text.
- `Jordan Lee` appeared in the final restored output.
- `Avery Brooks` appeared in the final restored output.

**Observed result:** Passed

The two names were assigned separate placeholders and restored correctly.

## 4. Evaluation Summary

All five automated M2 tests passed.

The results demonstrate that the prototype can:

- Detect names from the local synthetic term list
- Detect MRNs matching the documented structured pattern
- Mask supported values before provider processing
- Preserve repeated values with one placeholder
- Distinguish different values in the same request
- Handle notes containing no supported sensitive data
- Reject foreign-request placeholders
- Prevent partial restoration after validation failure
- Restore valid placeholders locally

The ordinary-input test confirmed that the original name and MRN did not appear in either the masked text or mock-provider response.

## 5. Summary Usefulness

The offline mock provider produces a predictable response using the headings:

- Presenting Concern
- Symptoms
- Medication
- Treatment Plan
- Follow-Up

It preserves masked placeholders and copies relevant sentences based on fixed keywords.

The response is sufficient for demonstrating the M2 privacy pipeline, but it has limitations:

- It may place the same sentence under more than one heading.
- It does not understand meaning like a real language model.
- It may return `Not provided` when its keyword rules do not recognize a sentence.
- A successful privacy result does not guarantee a high-quality summary.

Prompt usefulness and comparison between two prompt versions are deferred until M3.

## 6. Future Measurements

During M3, the evaluation will expand to record:

- **True positives:** Sensitive-value occurrences correctly detected
- **False positives:** Non-sensitive text incorrectly detected
- **False negatives:** Sensitive-value occurrences not detected
- **Outbound leaks:** Protected-value occurrences remaining in the provider request
- **Invalid tokens:** Invalid or unauthorized placeholders found
- **Restoration results:** Placeholders successfully restored or rejected
- **Precision and recall:** Calculated when their denominators are nonzero

M3 will also add tests for the remaining category, policy behavior, overlapping matches, provider failures, cross-request isolation, and prompt comparison.

