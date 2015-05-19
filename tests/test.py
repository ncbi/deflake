import unittest

from deflake import Deflake


class DeflakeTestCase(unittest.TestCase):
    def _results_are_same_and_pass(self, results):
        return all(results[0] == result and result == "PASS" for result in results)

    def test_default_no_fail(self):
        flake = Deflake("ls")
        results = flake.run()
        self.assertEqual(len(results), 10,
            "Program should have run 10 times but ran %s" % len(results))
        self.assertTrue(self._results_are_same_and_pass(results))

    def test_max_runs_no_fail(self):
        flake = Deflake("ls", max_runs=21)
        results = flake.run()
        self.assertEqual(len(results), 21, 
            "Program should have run 21 times but ran %s" % len(results))
        self.assertTrue(self._results_are_same_and_pass(results))

    def test_mp(self):
        flake = Deflake("ls", pool_size=4)
        results = flake.run()
        len_results = len(results)
        self.assertEqual(len_results, 10, 
            "Program should have run 10 times, but ran %s" % len_results)
        self.assertTrue(self._results_are_same_and_pass(results))

    def test_fail(self):
        flake = Deflake("./flaky.sh")
        results = flake.run()
        self.assertEqual(len(results), 7)
        self.assertEqual(results[-1], "FAIL")

    @classmethod
    def tearDownClass(cls):
        counter = open(".counter", "w")
        counter.write("0")
        counter.close()


if __name__ == "__main__":
    unittest.main()
