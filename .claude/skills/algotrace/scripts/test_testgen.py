import io
import subprocess
import sys
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("testgen.py")


def run(*args):
    out = subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)
    assert out.returncode == 0, out.stderr
    return out.stdout.strip().splitlines()


class TestArray(unittest.TestCase):
    def test_length(self):
        arr = eval(run("array", "--n", "12")[0])
        self.assertEqual(len(arr), 12)

    def test_bounds(self):
        arr = eval(run("array", "--n", "50", "--lo", "-5", "--hi", "5")[0])
        self.assertTrue(all(-5 <= x <= 5 for x in arr))

    def test_sorted_flag(self):
        arr = eval(run("array", "--n", "30", "--sorted")[0])
        self.assertEqual(arr, sorted(arr))

    def test_unique_flag(self):
        arr = eval(run("array", "--n", "20", "--unique", "--lo", "0", "--hi", "100")[0])
        self.assertEqual(len(arr), len(set(arr)))

    def test_edges_include_empty_and_overflow(self):
        lines = run("array", "--edges")
        cases = [eval(l) for l in lines]
        self.assertIn([], cases)
        self.assertIn([2**31 - 1, 2**31 - 1], cases)


class TestIntervals(unittest.TestCase):
    def test_sorted_and_valid(self):
        first = eval(run("intervals", "--n", "10")[0])
        self.assertEqual(first, sorted(first))
        self.assertTrue(all(a <= b for a, b in first))


class TestTree(unittest.TestCase):
    def test_level_order_shape(self):
        out = run("tree", "--n", "10")
        tree = eval(out[0])
        self.assertLessEqual(sum(1 for v in tree if v is not None), 10)
        self.assertIsNone(tree[-1] if not tree else None) if not tree else self.assertIsNotNone(tree[-1])


class TestGraph(unittest.TestCase):
    def test_edge_count_and_no_self_loops(self):
        out = run("graph", "--n", "5", "--m", "6")
        edges = eval(out[1])
        self.assertLessEqual(len(edges), 6)
        self.assertTrue(all(u != v for u, v in edges))
        self.assertEqual(len(edges), len(set(edges)))


if __name__ == "__main__":
    unittest.main()
