import unittest
from .wave_editor import *


class WaveEditorCase(unittest.TestCase):
    def test_reverse_audio(self):
        self.assertEqual(reverse_audio([[1, 2], [2, 3], [3, 4], [4, 5]]), [[4, 5], [3, 4], [2, 3], [1, 2]])
        self.assertEqual(reverse_audio([]), [])

    def test_accelerating_audio_speed(self):
        self.assertEqual(accelerating_audio_speed([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]]), [[1, 1], [3, 3], [5, 5]])
        self.assertEqual(accelerating_audio_speed([[1, 1]]), [[1, 1]])

    def test_slowdown_audio_speed(self):
        self.assertEqual(slowdown_audio_speed([[10, 10], [20, 30], [30, 50], [40, 60]]), [[10,10], [15, 20], [20,30], [25, 40], [30,50], [35, 55], [40, 60]])

if __name__ == '__main__':
    unittest.main()
