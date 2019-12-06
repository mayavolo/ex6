import unittest
from .wave_editor import *


class WaveEditorCase(unittest.TestCase):
    def test_reverse_audio(self):
        self.assertEqual(reverse_audio([[1, 2], [2, 3], [3, 4], [4, 5]]), [[4, 5], [3, 4], [2, 3], [1, 2]])


if __name__ == '__main__':
    unittest.main()
