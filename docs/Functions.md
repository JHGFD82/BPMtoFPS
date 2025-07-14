# Function Reference

This guide covers direct access to BPMtoFPS conversion functions for advanced users and specialized applications. While the main `convert_time()` function handles most use cases, these individual functions provide more control and flexibility.

## Overview

BPMtoFPS provides two categories of functions:
- **Input Converters**: Convert various time formats to seconds
- **Output Converters**: Convert seconds to video time formats

## Main Function

### convert_time()
The primary function that handles all conversions through a unified interface.

```python
from BPMtoFPS import convert_time

result = convert_time(ref_format, target_formats, input_value, 
                     bpm=None, fps=None, ticks_per_beat=480,
                     notes_per_measure=None, do_print=False)
```

**Parameters:**
- `ref_format` (str): Input format ('ticks', 'beats', 'measures', 'timecode', 'video_frames')
- `target_formats` (str or List[str]): Output format(s) ('frames', 'timecode', 'seconds')  
- `input_value` (int or str): Value to convert
- `bpm` (int, optional): Beats per minute (required for musical inputs)
- `fps` (float, optional): Frames per second (required for video outputs)
- `ticks_per_beat` (int, optional): MIDI ticks per beat (default: 480)
- `notes_per_measure` (int, optional): Quarter notes per measure (required for measures)
- `do_print` (bool, optional): Print results to console (default: False)

**Returns:** Dictionary with converted values

**Raises:**
- `ValueError`: Missing required parameters or invalid input
- `KeyError`: Unsupported format strings

**Examples:**
```python
# Single output
result = convert_time('beats', 'frames', 24, bpm=120, fps=29.97)
print(result)  # {'frames': 720}

# Multiple outputs
result = convert_time('ticks', ['frames', 'timecode'], 1920, 
                     bpm=120, fps=29.97, ticks_per_beat=480)
print(result)  # {'frames': 180, 'timecode': '6:00'}

# All outputs including seconds
result = convert_time('measures', ['frames', 'timecode', 'seconds'], 4,
                     bpm=140, notes_per_measure=4, fps=24)
```

## Input Converter Functions

These functions convert various time formats to seconds.

### ticks_to_seconds()
Convert MIDI ticks to seconds.

```python
from BPMtoFPS import ticks_to_seconds

seconds = ticks_to_seconds(input_value, bpm, ticks_per_beat)
```

**Parameters:**
- `input_value` (int): Number of ticks to convert
- `bpm` (int): Beats per minute of the musical piece
- `ticks_per_beat` (int): MIDI ticks per quarter note (typically 480)

**Returns:** Total seconds as float

**Raises:**
- `ZeroDivisionError`: If bpm or ticks_per_beat is zero
- `TypeError`: If arguments are not numbers

**Formula:** `seconds = input_value / ticks_per_beat / bpm * 60`

**Examples:**
```python
# Convert 960 ticks (2 beats) at 120 BPM
seconds = ticks_to_seconds(960, 120, 480)
print(seconds)  # 1.0

# Convert one measure (1920 ticks) at 140 BPM  
seconds = ticks_to_seconds(1920, 140, 480)
print(round(seconds, 2))  # 1.71

# Different MIDI resolution
seconds = ticks_to_seconds(720, 120, 360)  # 360 TPB resolution
print(seconds)  # 1.0
```

### beats_to_seconds()
Convert beats to seconds.

```python
from BPMtoFPS import beats_to_seconds

seconds = beats_to_seconds(input_value, bpm)
```

**Parameters:**
- `input_value` (int): Number of beats to convert
- `bpm` (int): Beats per minute of the musical piece

**Returns:** Total seconds as float

**Raises:**
- `ZeroDivisionError`: If bpm is zero
- `TypeError`: If arguments are not numbers

**Formula:** `seconds = input_value / bpm * 60`

**Examples:**
```python
# Convert 4 beats (one measure in 4/4) at 120 BPM
seconds = beats_to_seconds(4, 120)
print(seconds)  # 2.0

# Convert 24 beats at 140 BPM
seconds = beats_to_seconds(24, 140)
print(round(seconds, 2))  # 10.29

# Fast tempo
seconds = beats_to_seconds(16, 180)
print(round(seconds, 2))  # 5.33
```

### measures_to_seconds()
Convert musical measures to seconds.

```python
from BPMtoFPS import measures_to_seconds

seconds = measures_to_seconds(input_value, bpm, notes_per_measure)
```

**Parameters:**
- `input_value` (int): Number of measures to convert
- `bpm` (int): Beats per minute of the musical piece  
- `notes_per_measure` (int): Quarter notes per measure (time signature)

**Returns:** Total seconds as float

**Raises:**
- `ZeroDivisionError`: If bpm is zero
- `TypeError`: If arguments are not numbers

**Formula:** `seconds = input_value * notes_per_measure / bpm * 60`

**Examples:**
```python
# Convert 8 measures at 120 BPM in 4/4 time
seconds = measures_to_seconds(8, 120, 4)
print(seconds)  # 16.0

# Convert 2 measures at 90 BPM in 3/4 time (waltz)
seconds = measures_to_seconds(2, 90, 3)
print(seconds)  # 4.0

# Complex time signature: 7/8 time
seconds = measures_to_seconds(4, 120, 7)
print(round(seconds, 2))  # 14.0
```

### timecode_to_seconds()
Convert timecode strings to seconds.

```python
from BPMtoFPS import timecode_to_seconds

seconds = timecode_to_seconds(input_value)
```

**Parameters:**
- `input_value` (str): Timecode in "mm:ss.sss" format or seconds as string

**Returns:** Total seconds as float

**Raises:**
- `ValueError`: Invalid timecode format or unparseable string
- `TypeError`: Non-string input

**Supported Formats:**
- `"mm:ss.sss"` - Minutes:seconds.milliseconds  
- `"ss.sss"` - Direct seconds input as string

**Examples:**
```python
# Convert timecode format
seconds = timecode_to_seconds("1:30.5")
print(seconds)  # 90.5

# Convert direct seconds as string
seconds = timecode_to_seconds("45.25")  
print(seconds)  # 45.25

# More complex timecode
seconds = timecode_to_seconds("3:42.125")
print(seconds)  # 222.125
```

### video_frames_to_seconds()
Convert video frames to seconds.

```python
from BPMtoFPS import video_frames_to_seconds

seconds = video_frames_to_seconds(input_value, fps)
```

**Parameters:**
- `input_value` (int): Number of frames to convert
- `fps` (float): Frames per second of the video

**Returns:** Total seconds as float (rounded to 2 decimal places)

**Raises:**
- `ZeroDivisionError`: If fps is zero
- `TypeError`: If arguments are not numbers

**Formula:** `seconds = frames / frames_per_second`

**Examples:**
```python
# Convert 90 frames at 30 FPS
seconds = video_frames_to_seconds(90, 30.0)
print(seconds)  # 3.0

# Convert 750 frames at 29.97 FPS (NTSC)
seconds = video_frames_to_seconds(750, 29.97)
print(seconds)  # 25.03

# High frame rate
seconds = video_frames_to_seconds(1440, 120.0)
print(seconds)  # 12.0
```

## Output Converter Functions

These functions convert seconds to video time formats.

### seconds_to_frames()
Convert seconds to video frames with intelligent rounding.

```python
from BPMtoFPS import seconds_to_frames

frames = seconds_to_frames(seconds, fps, frac=0.75)
```

**Parameters:**
- `seconds` (float): Number of seconds to convert
- `fps` (float): Frames per second of the video project
- `frac` (float, optional): Rounding threshold (default: 0.75)

**Returns:** Total frames as int

**Raises:**
- `TypeError`: If arguments are not numbers
- `ValueError`: If frac is not between 0 and 1

**Smart Rounding:** If fractional part ≥ frac threshold, rounds up

**Examples:**
```python
# Convert 2.5 seconds at 24 FPS
frames = seconds_to_frames(2.5, 24.0)
print(frames)  # 60

# Custom rounding threshold
frames = seconds_to_frames(1.8, 29.97, frac=0.5)
print(frames)  # 54

# Default rounding (0.75 threshold)
frames = seconds_to_frames(3.7, 30.0)  # 3.7 * 30 = 111.0, no rounding
print(frames)  # 111

frames = seconds_to_frames(3.76, 30.0)  # 3.76 * 30 = 112.8, 0.8 ≥ 0.75, round up
print(frames)  # 113
```

### seconds_to_timecode()
Convert seconds to video timecode format.

```python
from BPMtoFPS import seconds_to_timecode

timecode = seconds_to_timecode(seconds, fps, frac=0.75)
```

**Parameters:**
- `seconds` (float): Number of seconds to convert
- `fps` (float): Frames per second of the video project  
- `frac` (float, optional): Rounding threshold for frames (default: 0.75)

**Returns:** Timecode string in "seconds:frames" format

**Raises:**
- `TypeError`: If arguments are not numbers
- `ValueError`: If frac invalid or values result in invalid timecode

**Format:** `"ss:ff"` where ss=seconds, ff=frames (zero-padded)

**Examples:**
```python
# Convert 45.5 seconds at 30 FPS
timecode = seconds_to_timecode(45.5, 30.0)
print(timecode)  # '45:15'

# Convert 12.8 seconds at 29.97 FPS
timecode = seconds_to_timecode(12.8, 29.97)
print(timecode)  # '12:24'

# Custom rounding
timecode = seconds_to_timecode(10.9, 24.0, frac=0.5)
print(timecode)  # '10:22'
```

## Advanced Usage Patterns

### Two-Step Conversions with Processing
```python
from BPMtoFPS import beats_to_seconds, seconds_to_frames

# Convert beats to seconds, apply custom processing, then to frames
seconds = beats_to_seconds(24, 120)  # 12.0 seconds

# Apply custom offset or processing
adjusted_seconds = seconds + 0.1  # Add 100ms delay

# Convert to frames
frames = seconds_to_frames(adjusted_seconds, 29.97)
print(frames)  # Result with custom processing
```

### Batch Processing
```python
from BPMtoFPS import measures_to_seconds, seconds_to_frames

# Process multiple measures
measures = [1, 2, 4, 8, 16, 32]
bpm = 128
fps = 29.97

results = []
for measure in measures:
    seconds = measures_to_seconds(measure, bpm, 4)
    frames = seconds_to_frames(seconds, fps)
    results.append({'measure': measure, 'frames': frames, 'seconds': seconds})

for result in results:
    print(f"Measure {result['measure']}: Frame {result['frames']} ({result['seconds']}s)")
```

### Custom Rounding Analysis
```python
from BPMtoFPS import seconds_to_frames

# Compare different rounding thresholds
seconds = 3.76
fps = 30.0

for threshold in [0.25, 0.5, 0.75, 0.9]:
    frames = seconds_to_frames(seconds, fps, frac=threshold)
    print(f"Threshold {threshold}: {frames} frames")
```

### Precision Comparison
```python
from BPMtoFPS import ticks_to_seconds, beats_to_seconds

# Compare tick-level vs beat-level precision
bpm = 120
ticks_per_beat = 480

# Beat-level
beat_seconds = beats_to_seconds(1, bpm)  # 1 beat

# Tick-level (same duration)
tick_seconds = ticks_to_seconds(480, bpm, ticks_per_beat)  # 480 ticks = 1 beat

print(f"Beat precision: {beat_seconds}")
print(f"Tick precision: {tick_seconds}")
print(f"Difference: {abs(beat_seconds - tick_seconds)}")  # Should be 0.0
```

---

*For command-line usage, see [CLI.md](CLI.md)*

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