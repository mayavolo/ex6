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
