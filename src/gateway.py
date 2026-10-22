import re
from pathlib import Path


# Locate names.txt relative to this Python file.
NAMES_FILE = Path(__file__).parent.parent / "data" / "names.txt"

# Supported MRN format: MRN- followed by exactly six digits.
MRN_PATTERN = re.compile(r"\bMRN-\d{6}\b")

# Complete format required for a valid placeholder.
PLACEHOLDER_PATTERN = re.compile(
    r"\[\[([A-Za-z0-9_-]+):(NAME|MRN):([1-9]\d*)\]\]"
)

# Finds any text attempting to use the reserved [[...]] syntax.
RESERVED_TOKEN_PATTERN = re.compile(r"\[\[.*?\]\]")

def load_names():
    """Load the fictional names from the local term-list file."""

    with open(NAMES_FILE, "r", encoding="utf-8") as file:
        names = []

        for line in file:
            name = line.strip()

            if name:
                names.append(name)

    return names

def detect_sensitive_data(text, names):
    """Find supported names and medical record numbers in the text."""

    detections = []

    # Detect every occurrence of each name in the local term list.
    for name in names:
        name_pattern = re.compile(rf"\b{re.escape(name)}\b")

        for match in name_pattern.finditer(text):
            detections.append(
                {
                    "category": "NAME",
                    "value": match.group(),
                    "start": match.start(),
                    "end": match.end()
                }
            )

    # Detect every supported medical record number.
    for match in MRN_PATTERN.finditer(text):
        detections.append(
            {
                "category": "MRN",
                "value": match.group(),
                "start": match.start(),
                "end": match.end()
            }
        )

    # Put detections in the same order in which they appear in the note.
    detections.sort(key=lambda detection: detection["start"])

    return detections

def mask_sensitive_data(text, detections, request_id):
    """Replace detected values and create a local placeholder mapping."""

    masked_parts = []
    placeholder_mapping = {}
    value_placeholders = {}
    category_counts = {}

    last_end = 0

    for detection in detections:
        category = detection["category"]
        value = detection["value"]
        start = detection["start"]
        end = detection["end"]

        # Overlap handling will be completed during M3.
        if start < last_end:
            raise ValueError("Overlapping detections are not supported in M2.")

        # Copy the non-sensitive text before this detection.
        masked_parts.append(text[last_end:start])

        # Category and value together identify a unique sensitive value.
        value_key = (category, value)

        if value_key not in value_placeholders:
            category_counts[category] = category_counts.get(category, 0) + 1

            number = category_counts[category]
            placeholder = f"[[{request_id}:{category}:{number}]]"

            value_placeholders[value_key] = placeholder
            placeholder_mapping[placeholder] = value
        else:
            placeholder = value_placeholders[value_key]

        # Insert the placeholder instead of the original value.
        masked_parts.append(placeholder)

        # Remember where the detected value ended.
        last_end = end

    # Copy any text remaining after the final detection.
    masked_parts.append(text[last_end:])

    masked_text = "".join(masked_parts)

    return masked_text, placeholder_mapping

def mock_provider(masked_text, request_id, mode="normal"):
    """Create a deterministic structured summary from the masked note."""

    # Divide the note into sentences.
    sentences = re.split(r"(?<=[.!?])\s+", masked_text.strip())

    def find_sentence(keywords):
        """Return the first sentence containing one of the keywords."""

        for sentence in sentences:
            lowercase_sentence = sentence.lower()

            for keyword in keywords:
                if keyword in lowercase_sentence:
                    return sentence

        return "Not provided."

    presenting_concern = sentences[0] if sentences else "Not provided."

    symptoms = find_sentence(
        ["reported", "anxiety", "depression", "sleep", "mood", "panic"]
    )

    medication = find_sentence(
        ["medication", "taking", "prescribed"]
    )

    treatment_plan = find_sentence(
        ["plan", "continue", "treatment"]
    )

    follow_up = find_sentence(
        ["follow-up", "return", "appointment"]
    )

    summary = (
        f"Presenting Concern: {presenting_concern}\n"
        f"Symptoms: {symptoms}\n"
        f"Medication: {medication}\n"
        f"Treatment Plan: {treatment_plan}\n"
        f"Follow-Up: {follow_up}"
    )

    if mode == "invalid_placeholder":
        summary += (
            f"\nInvalid Test: "
            f"[[{request_id}-foreign:NAME:1]]"
        )

    return summary

def validate_provider_response(response, request_id, placeholder_mapping):
    """Validate all reserved placeholders before restoration."""

    reserved_tokens = RESERVED_TOKEN_PATTERN.findall(response)

    for token in reserved_tokens:
        match = PLACEHOLDER_PATTERN.fullmatch(token)

        # The token uses [[...]] but does not follow the required format.
        if match is None:
            return False, f"Malformed placeholder: {token}"

        token_request_id = match.group(1)

        # The placeholder belongs to a different request.
        if token_request_id != request_id:
            return False, f"Placeholder belongs to another request: {token}"

        # The placeholder is well-formed but was not created for this request.
        if token not in placeholder_mapping:
            return False, f"Unknown placeholder: {token}"

    # Detect unmatched or incomplete reserved syntax.
    response_without_tokens = RESERVED_TOKEN_PATTERN.sub("", response)

    if "[[" in response_without_tokens or "]]" in response_without_tokens:
        return False, "Malformed reserved placeholder syntax."

    return True, None

#Loops through local mapping and replaces each placeholder w original value
def restore_sensitive_data(response, placeholder_mapping):
    """Restore valid placeholders using the local mapping."""

    restored_response = response

    for placeholder, original_value in placeholder_mapping.items():
        restored_response = restored_response.replace(
            placeholder,
            original_value
        )

    return restored_response

def create_error(request_id, error_code, message):
    """Create a controlled JSON-compatible error result."""

    return {
        "status": "error",
        "request_id": request_id,
        "error_code": error_code,
        "message": message
    }


def process_request(request):
    """Run one request through the complete privacy gateway."""

    if not isinstance(request, dict):
        return create_error(
            None,
            "INVALID_INPUT",
            "The input must be a JSON object."
        )

    request_id = request.get("request_id")
    text = request.get("text")
    mock_mode = request.get("mock_mode", "normal")

    if not isinstance(request_id, str) or not request_id:
        return create_error(
            None,
            "INVALID_INPUT",
            "request_id must be a non-empty string."
        )

    if re.fullmatch(r"[A-Za-z0-9_-]+", request_id) is None:
        return create_error(
            request_id,
            "INVALID_INPUT",
            "request_id may contain only letters, numbers, underscores, and hyphens."
        )

    if not isinstance(text, str) or not text.strip():
        return create_error(
            request_id,
            "INVALID_INPUT",
            "text must be a non-empty string."
        )

    if mock_mode not in ["normal", "invalid_placeholder"]:
        return create_error(
            request_id,
            "INVALID_MOCK_MODE",
            "mock_mode must be normal or invalid_placeholder."
        )

    names = load_names()

    detections = detect_sensitive_data(text, names)

    masked_text, placeholder_mapping = mask_sensitive_data(
        text,
        detections,
        request_id
    )

    provider_response = mock_provider(
        masked_text,
        request_id,
        mock_mode
    )

    is_valid, validation_error = validate_provider_response(
        provider_response,
        request_id,
        placeholder_mapping
    )

    if not is_valid:
        return create_error(
            request_id,
            "INVALID_PLACEHOLDER",
            validation_error
        )

    final_output = restore_sensitive_data(
        provider_response,
        placeholder_mapping
    )

    return {
        "status": "success",
        "request_id": request_id,
        "masked_text": masked_text,
        "provider_response": provider_response,
        "final_output": final_output
    }