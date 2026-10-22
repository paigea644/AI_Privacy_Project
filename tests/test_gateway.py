import unittest

from src.gateway import process_request


class GatewayTests(unittest.TestCase):

    def test_ordinary_input(self):
        request = {
            "request_id": "r1",
            "text": (
                "Patient Jordan Lee, MRN-482731, "
                "reported anxiety."
            )
        }

        result = process_request(request)

        self.assertEqual(result["status"], "success")

        self.assertNotIn(
            "Jordan Lee",
            result["masked_text"]
        )

        self.assertNotIn(
            "MRN-482731",
            result["masked_text"]
        )

        self.assertNotIn(
            "Jordan Lee",
            result["provider_response"]
        )

        self.assertNotIn(
            "MRN-482731",
            result["provider_response"]
        )

        self.assertIn(
            "Jordan Lee",
            result["final_output"]
        )

        self.assertIn(
            "MRN-482731",
            result["final_output"]
        )

    def test_repeated_name_uses_same_placeholder(self):
        request = {
            "request_id": "r2",
            "text": (
                "Jordan Lee reported anxiety. "
                "Jordan Lee will return next week."
            )
        }

        result = process_request(request)

        self.assertEqual(result["status"], "success")

        self.assertEqual(
            result["masked_text"].count("[[r2:NAME:1]]"),
            2
        )

        self.assertNotIn(
            "[[r2:NAME:2]]",
            result["masked_text"]
        )

    def test_no_sensitive_data(self):
        original_text = (
            "The patient reported anxiety and will return next week."
        )

        request = {
            "request_id": "r3",
            "text": original_text
        }

        result = process_request(request)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["masked_text"], original_text)
        self.assertNotIn("[[", result["masked_text"])

    def test_invalid_placeholder_response(self):
        request = {
            "request_id": "r4",
            "text": "Jordan Lee reported anxiety.",
            "mock_mode": "invalid_placeholder"
        }

        result = process_request(request)

        self.assertEqual(result["status"], "error")

        self.assertEqual(
            result["error_code"],
            "INVALID_PLACEHOLDER"
        )

        self.assertNotIn("final_output", result)

    def test_different_names_get_different_placeholders(self):
        request = {
            "request_id": "r5",
            "text": (
                "Jordan Lee listed Avery Brooks "
                "as an emergency contact."
            )
        }

        result = process_request(request)

        self.assertEqual(result["status"], "success")

        self.assertIn(
            "[[r5:NAME:1]]",
            result["masked_text"]
        )

        self.assertIn(
            "[[r5:NAME:2]]",
            result["masked_text"]
        )

        self.assertIn(
            "Jordan Lee",
            result["final_output"]
        )

        self.assertIn(
            "Avery Brooks",
            result["final_output"]
        )


if __name__ == "__main__":
    unittest.main()