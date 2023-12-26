# BPMtoFPS
This package provides tools to convert music time into video time.

Do you have the timecode for the moment in your song where you want a critical action to take place in the video? Are you looking to create a visualization of your favorite piece of music? Do you want to edit your own music video but need to put down markers on your timeline for where all the important beats are? BPMtoFPS was constructed with these exact needs in mind.

The math involved in this process is not complicated. If you know the exact parameters already you can find countless guides and websites for one-off conversions. For a more programmatic approach, however, these tools can save you time by taking large datasets of time values and converting them to the formats you need.

## Inputs
What information about your music do you have on hand? This package accepts the following with examples:
1. Beats (integer) - You know your song is 128 beats per minute and you need the timing for every 24 beats in your 29.97fps video project.
2. Ticks (integer) - You know your MIDI song file has a 480 tick-per-quarter-note resolution, is an instrument from a slow jam at 86 BPM, and you need to know when the note at the 34,812th tick appears in your 60fps video timeline.
3. Timecode (string) - Your song isn't of digital origin or has a shifting BPM, but you pause the music at 37.333 and realize you need a video effect to take place at that exact time in your 23.96fps video and don't feel like doing the math.

## Outputs
To assist with constructing your video project, the included functions can deliver results in these formats, with examples:
1. Frames (integer) - Video compositing software like Adobe After Effects and 3D animation software like Blender cooperate better when you can supply the exact frame number of when things should occur as long as you know the FPS of your project.
2. Timecode (string) - Editing software like Final Cut Pro or Adobe Premiere rely more on timecodes for exact position of video events.
3. Both (int, string) - Both frames and timecode can be outputted as a tuple.

## Examples of Use
`from BPMtoFPS import convert_time`
1. `convert_time('beats', 'frames', 24, bpm=128, fps=29.97)`
returns `337`
2. `convert_time('ticks', 'timecode', 34812, bpm=86, fps=60)`
returns `50:36`
3. `convert_time('timecode', 'timecode', '0:37.333', fps=23.96)`
returns `37:07`
4. `convert time('ticks', 'both', 3840, bpm=192, fps=29.97, ticks_per_beat=360)`
returns `(100, '3:10')`

## Handy Features

### Custom Fraction
With v1.2.0, you can provide your own threshold for when a resulting decimal in a frame number should be rounded up or down. Because audio has exponentially granular timing in comparison to video (to the tune of 360 or 480 ticks per second with MIDI, or 44,100 or 48,000 samples per second with recorded audio), video editors have to compensate for this by choosing where to place an action on the timeline, either at the frame before or after the exact moment occurs in the audio. By default, BPMtoFPS enforces a 0.75 threshold, so an action occuring at 4:33.67 (4 seconds, 33 frames, and... 67) will be rounded down to 4:33, whereas traditional rouding (0.5) would have rounded up to 4:34. This is *purely personal preference* and has generally been the threshold I use for my own projects. You can supply your own using the specific functions detailed below (look for the new "fraction" parameter.

### Direct Access to Conversion Functions
In addition to custom rounding, if you know what you're doing, you can skip past the mumbo jumbo of the main convert_time() function and instead go directly to the conversion functions themselves. There are two sets of functions that you can access directly:

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

### Command-line Execution

To be detailed here soon!