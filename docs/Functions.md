# Direct Access to Conversion Functions
If you know what you're doing, you can skip past the mumbo jumbo of the main convert_time() function and instead go directly to the conversion functions themselves. Both input and output conversions are functions you can access directly.

## Input Functions

### Convert ticks to seconds

```from BPMtoFPS import ticks_to_seconds```
```ticks_to_seconds(input_value, bpm, ticks_per_beat)```

Parameters:
- input_value (int): The value to convert
- bpm (int): The beats per minute of the piece of music
- ticks_per_beat (int): The number of ticks per quarter note (default is 480)

Arithmetic:
```seconds = input_value / ticks_per_beat / bpm * 60 seconds per minute```

Returns: Total number of seconds as float

### Convert beats to seconds

```from BPMtoFPS import beats_to_seconds```
```beats_to_seconds(input_value, bpm)```

Parameters:
- input_value (int): The value to convert 
- bpm (int): The beats per minute of the piece of music

Arithmetic:
```seconds = input_value / bpm * 60 seconds per minute```

Returns: Total number of seconds as float

### Convert measures to seconds

```from BPMtoFPS import measures_to_seconds```
```measures_to_seconds(input_value, bpm, notes_per_measure)```

Parameters:
- input_value (int): The value to convert
- bpm (int): The beats per minute of the piece of music
- notes_per_measure (int): The number of quarter notes per measure

Arithmetic:
```seconds = input_value * notes_per_measure / bpm * 60 seconds per minute```

Returns: Total number of seconds as float

### Convert timecode to seconds

```from BPMtoFPS import timecode_to_seconds```
```timecode_to_seconds(input_value)```

Parameters:
- input_value (int): The value to convert

Arithmetic:
```seconds = minutes of timecode * 60 seconds per minute + seconds of timecode```

Returns: Total number of seconds as float

## Output Functions

### Convert sections to frames

```from BPMtoFPS import seconds_to_frames```
```seconds_to_frames(seconds, fps, frac=fraction)```

Parameters:
- seconds (int): The number of seconds
- fps (int): The number of frames per second in a video project
- frac (float): The threshold for rounding

Arithmetic:
```frames = (seconds * fps) rounded depending on decimal vs. fraction```

Returns: Total number of frames

### Convert seconds to timecode

```from BPMtoFPS import seconds_to_timecode```
```seconds_to_timecode(seconds, fps, frac=fraction)```

Parameters:
- seconds (int): The number of seconds
- fps (int): The number of frames per second in a video project
- frac (float): The threshold for rounding

Arithmetic:
```timecode = string(total frames + ":" + total frames - seconds * fps)```

Returns: Timecode as string

## Other Functions

### Convert frames to seconds

```from BPMtoFPS import video_frames_to_seconds```
```video_frames_to_seconds(input_value, fps)```

Parameters:
- input_value (int): The value to convert
- fps (int): The number of frames per second in a video project

Arithmetic:
```seconds = input_value / fps```

Returns: Total number of seconds as float