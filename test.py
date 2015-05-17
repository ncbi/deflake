import unittest

from deflake import DeFlake


class DeflakeTestCase(unittest.TestCase):
    def test_default_no_fail(self):
        flake = DeFlake("ls")
        results = flake.run()
        self.assertEqual(len(results), 10)
        self.assertTrue(all(results[0] == result and result == "PASS" for result in results))

    def test_max_runs_no_fail(self):
        flake = DeFlake("ls", max_runs=21)
        results = flake.run()
        self.assertEqual(len(results), 21)
        self.assertTrue(all(results[0] == result and result == "PASS" for result in results))

    def test_mp(self):
        flake = DeFlake("ls", pool_size=4)
        results = flake.run()
        self.assertEqual(len(results), 10, "Program should have run 10 times, but ran %s" % len(results))
        self.assertTrue(all(results[0] == result and result == "PASS" for result in results))


if __name__ == "__main__":
    unittest.main()
