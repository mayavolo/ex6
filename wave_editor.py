import wave_helper
import math
import os
from copy import deepcopy

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
MIN_VOLUME = -32768


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
        print("Reading instructions file failed")
        return None
    pair_list = parse_file_contents(file_contents)
    if not pair_list:
        print("Parsing instructions file failed")
        return None
    return WAV_FILE_SAMPLE_RATE, convert_pairs_to_wav_list(pair_list)


def reverse_audio(audio_data):
    """
    function that reverses the list of the audio
    :param audio_data: list of list
    :return: reversed list
    """
    audio_data.reverse()
    return audio_data


def accelerating_audio_speed(audio_data):
    new_list = []
    for i in range(len(audio_data)):
        if i % 2 == 0:
            new_list.append(audio_data[i])
    return new_list


def slowdown_audio_speed(audio_data):
    new_list = []
    if len(audio_data) == 1:
        return audio_data
    new_list.append(audio_data[0])
    for i in range(1, len(audio_data)):
        average_list = [int((audio_data[i - 1][0] + audio_data[i][0]) / 2),
                        int((audio_data[i - 1][1] + audio_data[i][1]) / 2)]
        new_list.append(average_list)
        new_list.append(audio_data[i])
    return new_list


def turn_volume_up(audio_data):
    if len(audio_data) == 0:
        return audio_data

    for i in range(len(audio_data)):
        sound_one = int(audio_data[i][0] * 1.2)
        second_sound = int(audio_data[i][1] * 1.2)
        # updating one component of the sound
        if sound_one >= MAX_VOLUME:
            audio_data[i][0] = MAX_VOLUME
        elif sound_one <= MIN_VOLUME:
            audio_data[i][0] = MIN_VOLUME
        else:
            audio_data[i][0] = sound_one

        # updating the second component of the sound
        if second_sound >= MAX_VOLUME:
            audio_data[i][1] = MAX_VOLUME
        elif second_sound <= MIN_VOLUME:
            audio_data[i][1] = MIN_VOLUME
        else:
            audio_data[i][1] = second_sound
    return audio_data


def turn_volume_down(audio_data):
    if len(audio_data) == 0:
        return audio_data

    for i in range(len(audio_data)):
        sound_one = int(audio_data[i][0] / 1.2)
        second_sound = int(audio_data[i][1] / 1.2)
        # updating one component of the sound
        if sound_one >= MAX_VOLUME:
            audio_data[i][0] = MAX_VOLUME
        elif sound_one <= MIN_VOLUME:
            audio_data[i][0] = MIN_VOLUME
        else:
            audio_data[i][0] = sound_one

        # updating the second component of the sound
        if second_sound >= MAX_VOLUME:
            audio_data[i][1] = MAX_VOLUME
        elif second_sound <= MIN_VOLUME:
            audio_data[i][1] = MIN_VOLUME
        else:
            audio_data[i][1] = second_sound
    return audio_data


def low_pass_filter(audio_data_list):
    # average for the first member
    audio_data = deepcopy(audio_data_list)
    average_index_zero = int((audio_data_list[0][0] + audio_data_list[1][0]) / 2)
    average_index_one = int((audio_data_list[0][1] + audio_data_list[1][1]) / 2)
    if len(audio_data) == 2:
        audio_data[0][0] = average_index_zero
        audio_data[0][1] = average_index_one
        audio_data[1][0] = average_index_zero
        audio_data[1][1] = average_index_one
        return audio_data
    else:
        # updating the first member
        audio_data[0][0] = average_index_zero
        audio_data[0][1] = average_index_one
        for i in range(1, len(audio_data_list) - 1):
            average_index_zero = int(
                (audio_data_list[i - 1][0] + audio_data_list[i][0] + audio_data_list[i + 1][0]) / 3)
            average_index_one = int((audio_data_list[i - 1][1] + audio_data_list[i][1] + audio_data_list[i + 1][1]) / 3)
            audio_data[i][0] = average_index_zero
            audio_data[i][1] = average_index_one
        # updating the last member
        average_index_zero = int(
            (audio_data_list[len(audio_data_list) - 1][0] + audio_data_list[len(audio_data_list) - 2][0]) / 2)
        average_index_one = int(
            (audio_data_list[len(audio_data_list) - 1][1] + audio_data_list[len(audio_data_list) - 2][1]) / 2)
        audio_data[len(audio_data_list) - 1][0] = average_index_zero
        audio_data[len(audio_data_list) - 1][1] = average_index_one
    return audio_data


# low_pass_filter([[1, 1], [7, 7], [20, 20], [9, 9], [-12, -12]])


def save_changes_and_exit(frame_rate, audio_data, wave_filename):
    wave_helper.save_wave(frame_rate, audio_data, wave_filename)


def decision_to_change_the_file():
    file_name = input("Enter the name of the audio file:")
    file_content = wave_helper.load_wave(file_name)
    if file_content == (-1):
        print("could not load the wav file")
        return
    frame_rate, audio_data = file_content

    new_audio_data_list = audio_data
    while True:
        print("To reverse the audio press 1")
        print("To accelerate the audio speed press 2")
        print("To slowdown the audio speed press 3")
        print("To turn up the audio volume press 4")
        print("To turn down the audio volume press 5")
        print("To use the low pass filter press 6")
        print("To exit press 7")

        decision = int(input(""))
        if decision == 1:
            new_audio_data_list = reverse_audio(audio_data)
        elif decision == 2:
            new_audio_data_list = accelerating_audio_speed(audio_data)
        elif decision == 3:
            new_audio_data_list = slowdown_audio_speed(audio_data)
        elif decision == 4:
            new_audio_data_list = turn_volume_up(audio_data)
        elif decision == 5:
            new_audio_data_list = turn_volume_down(audio_data)
        elif decision == 6:
            new_audio_data_list = low_pass_filter(audio_data)
        elif decision == 7:
            completion_menu(frame_rate, new_audio_data_list)
            break
        else:
            print("Invalid choice")


def completion_menu(frame_rate, audio_data):
    new_file_name = input("Enter a name for the new wav file: ")
    save_changes_and_exit(frame_rate, audio_data, new_file_name)


def main():
    while True:
        print("------------------Welcome to a wave editor----------------------\n")
        print("For changing the file press 1")
        print("For Making your own wav file press 2")
        print("To exit press 3")
        print("----------------------------------------------------------------")
        try:
            decision = int(input("YOUR CHOICE: "))

            if decision == 1:
                decision_to_change_the_file()
            elif decision == 2:
                instructions_file = input("Enter the instructions file name: ")

                val = compose_wav_file(instructions_file)
                if val is None:
                    continue
                frame_rate, audio_data = val
                completion_menu(frame_rate, audio_data)
            elif decision == 3:
                break
            else:
                print("Invalid input")

        except ValueError:
            print("Invalid input")

if __name__ == '__main__':
    main()
