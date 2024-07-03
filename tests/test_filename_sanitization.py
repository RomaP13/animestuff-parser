import unittest

from utils.url_utils import sanitize_filename


class TestSanitizeFilename(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up class variables and read test cases from the input file."""
        filename = "tests/data/filenames_test_cases.txt"
        cls.filenames = []

        try:
            with open(filename, "r") as file:
                for line in file:
                    input_value, expected_value = line.strip().split(" => ")
                    cls.filenames.append((input_value, expected_value))
        except IOError as e:
            raise Exception(f"Error reading a file '{file}': {e}")

    def test_sanitize_filename(self):
        """
        Test the sanitize_filename function.

        This test iterates over each filename test case and verifies
        that the filename is sanitized correctly.

        Raises:
            AssertionError: If the sanitized filename
            does not match the expected value.
        """
        for input_value, expected_value in self.filenames:
            sanitized = sanitize_filename(input_value)
            msg = f"Expected '{expected_value}', but got '{sanitized}'"

            self.assertEqual(sanitized, expected_value, msg)


if __name__ == "__main__":
    unittest.main()
