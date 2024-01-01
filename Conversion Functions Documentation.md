#### Input Functions
`ticks_to_seconds(input_value, bpm, ticks_per_beat)`

    Convert ticks to seconds

    Parameters:
        input_value (int): The value to convert
        bpm (int): The beats per minute of the piece of music
        ticks_per_beat (int): The number of ticks per quarter note (default is 480)

    Arithmetic:
        seconds = input_value / ticks_per_beat / bpm * 60 seconds per minute

    Returns:
         Total number of seconds
`beats_to_seconds(input_value, bpm)`

    Convert beats to seconds

    Parameters:
        input_value (int): The value to convert
        bpm (int): The beats per minute of the piece of music

    Arithmetic:
        seconds = input_value / bpm * 60 seconds per minute

    Returns:
        Total number of seconds
`timecode_to_seconds(input_value)`

    Convert timecode to seconds

    Parameters:
        input_value (int): The value to convert

    Arithmetic:
        seconds = minutes of timecode * 60 seconds per minute + seconds of timecode

    Returns:
        Total number of seconds

#### Output Functions

`seconds_to_frames(seconds, fps, frac=fraction)`

    Convert sections to frames

    Parameters:
        seconds (int): The number of seconds
        fps (int): The number of frames per second in a video project
        frac (float): The threshold for rounding

    Arithmetic:
        frames = (seconds * fps) rounded depending on decimal vs. fraction

    Returns:
        Total number of frames

`seconds_to_timecode(seconds, fps, frac=fraction)`

    Convert seconds to timecode

    Parameters:
        seconds (int): The number of seconds
        fps (int): The number of frames per second in a video project
        frac (float): The threshold for rounding

    Arithmetic:
        timecode = string(total frames + ":" + total frames - seconds * fps)

    Returns:
        Timecode as string