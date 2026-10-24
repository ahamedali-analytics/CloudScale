import importlib.util
import pathlib
import sys
import unittest

PROCESSOR_PATH = pathlib.Path(__file__).parents[1] / "backend" / "worker" / "processor.py"
spec = importlib.util.spec_from_file_location("cloudscale_processor", PROCESSOR_PATH)
processor = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = processor
spec.loader.exec_module(processor)


class ProcessRecordsTests(unittest.TestCase):
    def test_counts_records_and_fields(self):
        result = processor.process_records([{"a": 1}, {"a": 3, "b": "x"}])
        self.assertEqual(result["recordCount"], 2)
        self.assertEqual(result["fieldCount"], 2)
        self.assertEqual(result["numericSummary"]["a"]["mean"], 2)

    def test_counts_missing_values(self):
        result = processor.process_records([{"x": None}, {"x": ""}, {}])
        self.assertEqual(result["missingValuesByField"]["x"], 3)

    def test_preview_is_limited_to_five(self):
        result = processor.process_records([{"i": i} for i in range(8)])
        self.assertEqual(len(result["preview"]), 5)

    def test_rejects_non_dictionary_records(self):
        with self.assertRaises(ValueError):
            processor.process_records([{"ok": 1}, "bad"])

    def test_empty_list_is_valid_for_processor(self):
        result = processor.process_records([])
        self.assertEqual(result["recordCount"], 0)
        self.assertEqual(result["fields"], [])


if __name__ == "__main__":
    unittest.main()
