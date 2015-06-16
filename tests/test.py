import sys
import os
import unittest

from deflake import Deflake


class DeflakeTestCase(unittest.TestCase):
    THIS_DIR = os.path.dirname(os.path.realpath(__file__))

    def _results_are_same_and_pass(self, results):
        return all(results[0] == result and result == "PASS" for result in results)

    def test_default_no_fail(self):
        flake = Deflake("ls", quiet=True)
        results = flake.run()
        self.assertEqual(len(results), 10,
            "Program should have run 10 times but ran %s" % len(results))
        self.assertTrue(self._results_are_same_and_pass(results))

    def test_max_runs_no_fail(self):
        flake = Deflake("ls", max_runs=21, quiet=True)
        results = flake.run()
        self.assertEqual(len(results), 21, 
            "Program should have run 21 times but ran %s" % len(results))
        self.assertTrue(self._results_are_same_and_pass(results))

    @unittest.skipIf("3.4" in sys.version, "poolsize generates too many processes for Python 3.4")
    def test_mp(self):
        flake = Deflake("ls", pool_size=4, quiet=True)
        results = flake.run()
        len_results = len(results)
        self.assertEqual(len_results, 10, 
            "Program should have run 10 times, but ran %s" % len_results)
        self.assertTrue(self._results_are_same_and_pass(results))

    def test_fail(self):
        flake = Deflake(os.path.join(self.THIS_DIR, "flaky.sh"), quiet=True)
        results = flake.run()
        self.assertEqual(len(results), 8)
        self.assertEqual(results[-2], "FAIL (run 7)")
        self.assertEqual(results[-1], "forced error\n")

    def test_counter_token(self):
        flake = Deflake("touch file#count#.txt", max_runs=2, quiet=True)
        results = flake.run()
        self.assertTrue(os.path.exists('file1.txt') and os.path.exists('file2.txt'))

    @classmethod
    def tearDownClass(cls):
        counter = open(os.path.join(cls.THIS_DIR, ".counter"), "w")
        counter.write("0")
        counter.close()
        os.remove('file1.txt')
        os.remove('file2.txt')


if __name__ == "__main__":
    unittest.main()
