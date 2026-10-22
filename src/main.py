import json
import sys

from gateway import process_request

def main():
    if len(sys.argv) != 2:
        result = {
            "status": "error",
            "request_id": None,
            "error_code": "INVALID_COMMAND",
            "message": "Provide the path to one JSON request file."
        }

        print(json.dumps(result, indent=2))
        return 1

    input_path = sys.argv[1]

    try:
        with open(input_path, "r", encoding="utf-8") as file:
            request = json.load(file)
    except FileNotFoundError:
        result = {
            "status": "error",
            "request_id": None,
            "error_code": "FILE_NOT_FOUND",
            "message": f"Could not find input file: {input_path}"
        }

        print(json.dumps(result, indent=2))
        return 1
    except json.JSONDecodeError:
        result = {
            "status": "error",
            "request_id": None,
            "error_code": "INVALID_JSON",
            "message": "The input file does not contain valid JSON."
        }

        print(json.dumps(result, indent=2))
        return 1

    result = process_request(request)

    print(json.dumps(result, indent=2))

    if result["status"] == "success":
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())