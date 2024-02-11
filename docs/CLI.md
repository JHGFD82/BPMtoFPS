# Command-line Execution
Don't want to pull open a Python console just to retrieve some numbers? BPMtoFPS can be executed from the command line! To do so, navigate to the folder that contains the main.py script and run it:

`python3 main.py`

...and proceed to go nowhere with it. That's because you need to supply some arguments! Here is what you will need to enter:

## Input (pick one)
`-t / --ticks` MIDI ticks (requires BPM and Division argument)

`-b / --beats` Beats (requires BPM argument)

`-m / --measures` Measures (requires BPM and Notes Per Measure argument)

`-c / --timecode_in` Audio timecode in mm:ss.sss format

`-v / --video_frames` Video frames

## Output (pick one or both)
`-V / --frames` Video frames

`-C / --timecode_out` Timecode in ss:ff format

`-S / --seconds` Seconds in ss.sss format

## Required Arguments
`-i / --input_value` The value being converted

`-F / --fps` Frames per second, required for all inputs

`-B / --bpm` Beats per second, required if inputting ticks, beats, or measures

`-D / --division` Number of MIDI ticks per beat (division), default is 480, required if inputting ticks

`-N / --notes_per_measure` Number of notes per measure, required if inputting measures

## Optional Parameters
`-p / --print` Print to the console

Now that you have all of these options, you can do some crazy argument combinations like

`-mVCSpi`

It's fun!