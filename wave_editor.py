import wave_helper


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
    MAX_VOLUME = 32767
    MIN_VOLUME = -32767
    if len(audio_data) == 0:
        return audio_data

    for i in range(len(audio_data)):
        sound_one = int(audio_data[i][0] * 1.2)
        second_sound = int(audio_data[i][1] * 1.2)
        # updating one component of the sound
        if sound_one >= MAX_VOLUME:
            audio_data[i][[0]] = MAX_VOLUME
        elif sound_one <= MIN_VOLUME:
            audio_data[i][[0]] = MIN_VOLUME
        else:
            audio_data[i][[0]] = sound_one

        # updating the second component of the sound
        if second_sound >= MAX_VOLUME:
            audio_data[i][[1]] = MAX_VOLUME
        elif second_sound <= MIN_VOLUME:
            audio_data[i][[1]] = MIN_VOLUME
        else:
            audio_data[i][[1]] = second_sound
    return audio_data


def turn_volume_down(audio_data):
    MAX_VOLUME = 32767
    MIN_VOLUME = -32767
    if len(audio_data) == 0:
        return audio_data

    for i in range(len(audio_data)):
        sound_one = int(audio_data[i][0] / 1.2)
        second_sound = int(audio_data[i][1] / 1.2)
        # updating one component of the sound
        if sound_one >= MAX_VOLUME:
            audio_data[i][[0]] = MAX_VOLUME
        elif sound_one <= MIN_VOLUME:
            audio_data[i][[0]] = MIN_VOLUME
        else:
            audio_data[i][[0]] = sound_one

        # updating the second component of the sound
        if second_sound >= MAX_VOLUME:
            audio_data[i][[1]] = MAX_VOLUME
        elif second_sound <= MIN_VOLUME:
            audio_data[i][[1]] = MIN_VOLUME
        else:
            audio_data[i][[1]] = second_sound
    return audio_data


def low_pass_filter(audio_data):
    # average for the first member
    average_index_zero = int((audio_data[0][0] + audio_data[[1][0]]) / 2)
    average_index_one = int((audio_data[0][1] + audio_data[[1][1]]) / 2)
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
        for i in range(1, len(audio_data) - 1):
            average_index_zero = int((audio_data[i - 1][0] + audio_data[i][0] + audio_data[i + 1][0]) / 3)
            average_index_one = int((audio_data[i - 1][1] + audio_data[i][1] + audio_data[i + 1][1]) / 3)
            audio_data[i][0] = average_index_zero
            audio_data[i][1] = average_index_one
        average_index_zero = int((audio_data[len(audio_data) - 1][0] + audio_data[[len(audio_data) - 2][0]]) / 2)
        average_index_one = int((audio_data[len(audio_data) - 1][1] + audio_data[[len(audio_data) - 2][1]]) / 2)
        # updating the last member
        audio_data[len(audio_data) - 1][0] = average_index_zero
        audio_data[len(audio_data) - 1][1] = average_index_one
    return audio_data


def save_changes_and_exit(frame_rate, audio_data, wave_filename):
    wave_helper.save_wave(frame_rate, audio_data, wave_filename)


def decision_to_change_the_file():
    file_name = input("Enter the name of the audio file:")
    file_content = wave_helper.load_wave(file_name)
    if file_content == (-1):
        print("could not load the wav file")
        return
    frame_rate, audio_data = file_content
    print("To reverse the audio press 1")
    print("To accelerate the audio speed press 2")
    print("To slowdown the audio speed press 3")
    print("To turn up the audio volume press 4")
    print("To turn down the audio volume press 5")
    print("To use the low pass filter press 6")
    print("To exit press 7")
    new_audio_data_list = audio_data
    while True:
        decision = int(input(""))
        if decision == 1:
            new_audio_data_list = reverse_audio(audio_data)
        if decision == 2:
            new_audio_data_list = accelerating_audio_speed(audio_data)
        if decision == 3:
            new_audio_data_list = slowdown_audio_speed(audio_data)
        if decision == 4:
            new_audio_data_list = turn_volume_up(audio_data)
        if decision == 5:
            new_audio_data_list = turn_volume_down(audio_data)
        if decision == 7:
            completion_menu(frame_rate, new_audio_data_list)
            break


def compose_wav_file():
    pass


def completion_menu(frame_rate, audio_data):
    new_file_name = input("Enter a name for the new wav file: ")
    save_changes_and_exit(frame_rate, audio_data, new_file_name)


def main():
    while True:
        print("Welcome to a wave editor")
        print("For changing the file press 1")
        print("For Making your own wav file press 2")
        print("To exit press 3")
        decision = int(input(""))
        if decision == 1:
            decision_to_change_the_file()
        if decision == 2:
            frame_rate, audio_data = compose_wav_file()
            completion_menu(frame_rate, audio_data)
        if decision == 3:
            break
            #
