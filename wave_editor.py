import wave_helper
import math
import sys
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


def reverse_audio(audio_data):
    """
    function that reverses the list of the audio
    :param audio_data: list of list
    :return: reversed list
    """
    audio_data.reverse()
    print("The audio was reversed successfully")
    return audio_data


def accelerating_audio_speed(audio_data):
    """
    This function accelerates the audio speed
    :param audio_data: a list of lists with integers
    :return: the updated list
    """
    new_list = []
    for i in range(len(audio_data)):
        if i % 2 == 0:
            new_list.append(audio_data[i])
    print("The audio was accelerated successfully")
    return new_list


def slowdown_audio_speed(audio_data):
    """
    This function slows down the audio speed
    :param audio_data: a list of lists with integers
    :return: the updated list
    """
    new_list = []
    if len(audio_data) <= 1:
        return audio_data
    new_list.append(audio_data[0])
    for i in range(1, len(audio_data)):
        average_list = [int((audio_data[i - 1][0] + audio_data[i][0]) / 2),
                        int((audio_data[i - 1][1] + audio_data[i][1]) / 2)]
        new_list.append(average_list)
        new_list.append(audio_data[i])
    print("The audio was slowed down successfully")
    return new_list


def turn_volume_up(audio_data):
    """
    This function the audio volume up
    :param audio_data: a list of lists with integers
    :return: the updated list
    """
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
    print("The audio volume raised successfully")
    return audio_data


def turn_volume_down(audio_data):
    """
    This function the audio volume down
    :param audio_data: a list of lists with integers
    :return: the updated list
    """
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
    print("The audio volume was turned down successfully")
    return audio_data


def low_pass_filter(audio_data_list):
    """
    This function does a low pass filter audio
    :param audio_data_list: a list of lists with integers
    :return: the updated list
    """
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
            average_index_one = int((audio_data_list[i - 1][1] + audio_data_list[i][1] +
                                     audio_data_list[i + 1][1]) / 3)
            audio_data[i][0] = average_index_zero
            audio_data[i][1] = average_index_one
        # updating the last member
        average_index_zero = int(
            (audio_data_list[len(audio_data_list) - 1][0] +
             audio_data_list[len(audio_data_list) - 2][0]) / 2)
        average_index_one = int(
            (audio_data_list[len(audio_data_list) - 1][1] +
             audio_data_list[len(audio_data_list) - 2][1]) / 2)
        audio_data[len(audio_data_list) - 1][0] = average_index_zero
        audio_data[len(audio_data_list) - 1][1] = average_index_one
    print("The audio low passed successfully")
    return audio_data


def save_changes_and_exit(frame_rate, audio_data, wave_filename):
    """
    This functions saves the updated wav file
    """
    wave_helper.save_wave(frame_rate, audio_data, wave_filename)
    print("The new changes were successfully saved")


def decision_to_change_the_file(frame_rate=None, audio_data=None):
    """
    This function handles the decision to make changes to a wav file
    """
    if frame_rate is None and audio_data is None:
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
    """
    This function saves the changed file to the given new file name
    """
    new_file_name = input("Enter a name for the new wav file: ")
    save_changes_and_exit(frame_rate, audio_data, new_file_name)


def main():
    """
    Thats is the main function that runs the whole program
    """
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

                val = melody_composing(instructions_file)
                if val is None:
                    continue
                frame_rate, audio_data = val
                decision_to_change_the_file(frame_rate, audio_data)
            elif decision == 3:
                break
            else:
                print("Invalid input")

        except ValueError:
            print("Invalid input")


def read_melody_file(filename):
    """
    This function loads the content of the file
    :param filename: the name of the file
    :return: The content of the file (string)
    """

    if not os.path.exists(filename):
        return None

    with open(filename, 'r') as file:
        melody = file.read().splitlines()
        melody = ' '.join(melody)
    return melody


def melody_composing(filename):
    instructions = read_melody_file(filename)  # the instructions of the composition
    if not instructions:
        print('invalid file')
        return None

    notes_list = note_time_list(instructions)
    if not notes_list:
        print('invalid notes')
        return None

    wav_list = make_a_wav(notes_list)
    return WAV_FILE_SAMPLE_RATE, wav_list


def note_time_list(melody):
    """
    this function make a list of a note and a time (like 16 or 8)
    :param melody: The string with the instructions for the melody
    :return: The list
    """

    instructions = melody.split(' ')
    instructions = [value for value in instructions if value != '']

    pairs = list()  # A list of lists[[Note, Number],....]
    pair = list()  # A single list

    if len(instructions) % 2:  # --> The list must be has an even length
        return None

    for i in range(len(instructions)):

        value = instructions[i]

        if not i % 2:
            if value not in NOTE_TO_FREQ_MAPPING.keys() \
                    or len(value) != 1:  # ----> it means we got incorrect instructions
                return None

            pair.append(value)

        else:
            if not value.isdigit() \
                    or int(value) <= 0:  # ----> it means we got incorrect instructions
                return None

            pair.append(int(value))
            pairs.append(pair)
            pair = list()

    return pairs


def calculate_length_of_sample(frequency, index):
    samples_per_cycle = WAV_FILE_SAMPLE_RATE / frequency
    length_of_index = int(MAX_VOLUME * math.sin(2 * math.pi * (index / samples_per_cycle)))

    return [length_of_index, length_of_index]


def make_a_wav(pairs):
    """
    This function gets a list - [Note(string), Number(string)] and returns a wav list
    :param pairs: A list of lists [[Note, Number],....]
    :return: Wav list

    ['F', 16], ['G', 8], ['Q', 32], ['G', 1] -- > [[0, 0], [26629, 26629], [-31033, -31033], [9536, 9536], …]
    """
    melody_lst = list()  # The wav list
    for pair in pairs:

        frequency = NOTE_TO_FREQ_MAPPING[pair[0]]
        current_length = pair[1] * int((1 / 16) * WAV_FILE_SAMPLE_RATE)

        for index in range(current_length):
            if frequency != 0:
                melody_lst.append(calculate_length_of_sample(frequency, index))
            else:
                melody_lst.append([0, 0])

    return melody_lst


if __name__ == '__main__':
    main()
