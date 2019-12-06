import math
import os

WAV_FILE_SAMPLE_RATE = 2000
MAX_VOLUME = 32767
NOTE_TO_FREQ_MAPPING = {
    'A': 440,
    'B': 494,
    'C': 523,
    'D': 587,
    'E': 659,
    'F': 698,
    'G': 784,
    'Q': 0
}


def calculate_wave_length_for_index_i(max_vol, i, sample_rate, frequency):
    samples_per_cycle = sample_rate / frequency
    return int(max_vol * math.sin(math.pi * 2 * i / samples_per_cycle))


def read_file_contents(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()
        lines = ' '.join(lines)
    return lines


def parse_file_contents(lines):
    values = lines.split(' ')
    values = [value for value in values if value != '']
    if len(values) % 2:
        return None
    current_pair = []
    pair_list = []
    for i in range(len(values)):
        if i % 2 == 0:
            if values[i] not in NOTE_TO_FREQ_MAPPING.keys():
                return None
            current_pair.append(values[i])
        else:
            value_as_int = int(values[i])
            if value_as_int < 0 or value_as_int > 16:
                return None
            current_pair.append(value_as_int)
            pair_list.append(current_pair)
            current_pair = []
    return pair_list


def convert_pairs_to_wav_list(pair_list):
    final_wav = []
    for pair in pair_list:
        current_note_length = pair[1] * int(1 / 16 * WAV_FILE_SAMPLE_RATE)
        current_note = pair[0]
        for i in range(current_note_length):
            index_val = calculate_wave_length_for_index_i(MAX_VOLUME, i, WAV_FILE_SAMPLE_RATE,
                                                          NOTE_TO_FREQ_MAPPING[current_note])
            final_wav.append([index_val, index_val])
    return final_wav


def compose_wav_file(instruction_file_path):
    file_contents = read_file_contents(instruction_file_path)
    if not file_contents:
        return None
    pair_list = parse_file_contents(file_contents)
    if not pair_list:
        return None
    return WAV_FILE_SAMPLE_RATE, convert_pairs_to_wav_list(pair_list)
