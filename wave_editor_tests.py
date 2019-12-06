import unittest
from wave_editor import *
from wave_helper import load_wave
import os


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return None


class WaveEditorCase(unittest.TestCase):
    def test_reverse_audio(self):
        self.assertEqual([[4, 5], [3, 4], [2, 3], [1, 2]], reverse_audio([[1, 2], [2, 3], [3, 4], [4, 5]]))
        self.assertEqual([], reverse_audio([]))

    def test_accelerating_audio_speed(self):
        self.assertEqual([[1, 1], [3, 3], [5, 5]], accelerating_audio_speed([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]]))
        self.assertEqual([[1, 1]], accelerating_audio_speed([[1, 1]]))

    def test_first_sample_file(self):
        samples_dir = os.path.dirname(find('sample1.txt', os.getcwd()))
        composed_list = compose_wav_file(rf'{samples_dir}\sample1.txt')
        loaded_wave = load_wave(rf'{samples_dir}\sample1.wav')
        self.assertEqual(composed_list, loaded_wave)

    def test_slowdown_audio_speed(self):
        self.assertEqual([[10, 10], [15, 20], [20, 30], [25, 40], [30, 50], [35, 55], [40, 60]],
                         slowdown_audio_speed([[10, 10], [20, 30], [30, 50], [40, 60]]))

    def test_second_sample_file(self):
        samples_dir = os.path.dirname(find('sample1.txt', os.getcwd()))
        composed_list = compose_wav_file(rf'{samples_dir}\sample2.txt')
        loaded_wave = load_wave(rf'{samples_dir}\sample2.wav')
        self.assertEqual(composed_list, loaded_wave)

    def test_turn_volume_up(self):
        self.assertEqual([[-32768, -120], [-66, -66], [0, 0], [4, -2420], [32767, 12002]],
                         turn_volume_up([[-32760, -100], [-55, -55], [0, 0], [4, -2017], [32767, 10002]]))

    def test_turn_volume_down(self):
        self.assertEqual([[-27300, -83], [-45, -45], [0, 0], [3, -1680], [27305, 8335]],
                         turn_volume_down([[-32760, -100], [-55, -55], [0, 0], [4, -2017], [32767, 10002]]))

    def test_low_pass_filter(self):
        list_to_filter = [[1, 1], [7, 7], [20, 20], [9, 9], [-12, -12]]
        self.assertEqual([[4, 4], [9, 9], [12, 12], [5, 5], [-1, -1]],
                         low_pass_filter(list_to_filter))


if __name__ == '__main__':
    unittest.main()
