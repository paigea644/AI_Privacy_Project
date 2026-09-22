# Evaluation Plan

## 1. Purpose

This evaluation will determine whether the Psychiatric Note Privacy Gateway protects supported sensitive values while still producing a useful summary.

All tests will use synthetic, meaning completely fictional, patient information created for this project. No real patient information will be used.

For M1, the following cases are planned but have not been implemented or executed. They will become automated tests during M2.

## 2. Planned Acceptance Cases

### Case 1: Ordinary Input

**Purpose:** Verify that the gateway detects and masks supported sensitive values in a typical note.

**Original input:**

> Patient Jordan Lee, MRN-482731, reported increased anxiety and difficulty sleeping for the past two weeks. The patient is taking sertraline as prescribed. The plan is to continue the current medication and return in two weeks.

**Expected masked input:**

> Patient [[r1:NAME:1]], [[r1:MRN:1]], reported increased anxiety and difficulty sleeping for the past two weeks. The patient is taking sertraline as prescribed. The plan is to continue the current medication and return in two weeks.

**Expected result:**

The provider should return a structured summary containing the relevant symptoms, medication, treatment plan, and follow-up information. The gateway should validate and restore any authorized placeholders included in the response.

Neither `Jordan Lee` nor `MRN-482731` should appear in the outbound masked request.

**Expected status:** Success

---

### Case 2: Repeated Sensitive Value

**Purpose:** Verify that repeated occurrences of the same value use the same placeholder.

**Original input:**

> Jordan Lee reported increased anxiety. Jordan Lee stated that the symptoms become worse at night. A follow-up appointment was scheduled for Jordan Lee in two weeks.

**Expected masked input:**

> [[r2:NAME:1]] reported increased anxiety. [[r2:NAME:1]] stated that the symptoms become worse at night. A follow-up appointment was scheduled for [[r2:NAME:1]] in two weeks.

**Expected result:**

All three occurrences of `Jordan Lee` should be replaced with `[[r2:NAME:1]]`. If that placeholder appears in the provider response, every occurrence should be restored as `Jordan Lee`.

**Expected status:** Success

---

### Case 3: No Sensitive Data

**Purpose:** Verify that the gateway handles a note containing no supported sensitive values.

**Original input:**

> The patient reported difficulty sleeping and increased anxiety during the past week. The patient is taking the current medication as prescribed. The plan is to discuss sleep habits and schedule a follow-up appointment in two weeks.

**Expected masked input:**

The masked input should be identical to the original input because it contains no patient name or medical record number.

**Expected result:**

The gateway should process the note without creating or restoring any placeholders. The absence of sensitive information should not be treated as an error.

**Expected status:** Success

---

### Case 4: Invalid Placeholder Response

**Purpose:** Verify that the gateway rejects a placeholder that was not created for the current request.

**Original input:**

> Patient Jordan Lee, MRN-482731, reported increased anxiety.

**Expected masked input:**

> Patient [[r4:NAME:1]], [[r4:MRN:1]], reported increased anxiety.

**Simulated invalid provider response:**

> Presenting Concern: [[r99:NAME:1]] reports increased anxiety.

**Expected result:**

The validator should reject `[[r99:NAME:1]]` because it belongs to request `r99`, not the current request, `r4`.

The program should:

- Return a controlled error.
- Avoid restoring any sensitive values.
- Avoid displaying a partially restored response.
- Never send the original unmasked note as a fallback.

**Expected status:** Controlled error

## 3. Evaluation Criteria

Each case will check whether:

- Supported sensitive values were detected.
- The correct placeholders were created.
- Protected values were absent from the outbound request.
- Repeated values used the same placeholder.
- Only valid placeholders were restored.
- The final summary preserved important clinical facts.
- Invalid responses produced controlled errors.
- No unmasked fallback request was sent.

## 4. Planned Measurements

During later milestones, the evaluation will record:

- **True positives:** Sensitive values correctly detected
- **False positives:** Non-sensitive text incorrectly detected
- **False negatives:** Sensitive values not detected
- **Outbound leaks:** Protected values remaining in the outbound request
- **Invalid tokens:** Invalid or unauthorized placeholders
- **Restoration results:** Placeholders successfully restored or rejected
- **Summary usefulness:** Whether the summary preserves required facts without inventing information

Precision and recall will be calculated when their denominators are nonzero.

## 5. Current Status

These are planned M1 acceptance cases. The complete gateway has not yet been implemented, so no test results are being claimed.

During M2, the relevant cases will be automated, executed, and updated with their observed results.