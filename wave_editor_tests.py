import unittest
from .wave_editor import *
from .compositor import compose_wav_file
from .wave_helper import load_wave
import os


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return None


class WaveEditorCase(unittest.TestCase):
    def test_reverse_audio(self):
        self.assertEqual(reverse_audio([[1, 2], [2, 3], [3, 4], [4, 5]]), [[4, 5], [3, 4], [2, 3], [1, 2]])
        self.assertEqual(reverse_audio([]), [])

    def test_accelerating_audio_speed(self):
        self.assertEqual(accelerating_audio_speed([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]]), [[1, 1], [3, 3], [5, 5]])
        self.assertEqual(accelerating_audio_speed([[1, 1]]), [[1, 1]])
    def test_first_sample_file(self):
        samples_dir = os.path.dirname(find('sample1.txt', os.getcwd()))
        composed_list = compose_wav_file(rf'{samples_dir}\sample1.txt')
        loaded_wave = load_wave(rf'{samples_dir}\sample1.wav')
        self.assertEqual(composed_list, loaded_wave)

    def test_slowdown_audio_speed(self):
        self.assertEqual(slowdown_audio_speed([[10, 10], [20, 30], [30, 50], [40, 60]]), [[10,10], [15, 20], [20,30], [25, 40], [30,50], [35, 55], [40, 60]])

    def test_second_sample_file(self):
        samples_dir = os.path.dirname(find('sample1.txt', os.getcwd()))
        composed_list = compose_wav_file(rf'{samples_dir}\sample2.txt')
        loaded_wave = load_wave(rf'{samples_dir}\sample2.wav')
        self.assertEqual(composed_list, loaded_wave)


if __name__ == '__main__':
    unittest.main()
