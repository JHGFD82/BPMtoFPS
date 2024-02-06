# Command-line Execution
Don't want to pull open a Python console just to retrieve some numbers? BPMtoFPS can be executed from the command line! To do so, navigate to the folder that contains the main.py script and run it:

`python3 main.py`

...and proceed to go nowhere with it. That's because you need to supply some arguments! Here is what you will need to enter:

## Input (pick one)
`-m / --ticks` MIDI ticks (requires BPM and Division argument)

`-b / --beats` Beats (requires BPM argument)

`-t / --timecode` Audio timecode in mm:ss.sss format

`-v / --video_frames` Video frames

## Output (pick one or both)
`-f / --frames` Video frames

`-c / --timecode_output` Timecode

## Required Arguments
`-i / --input_value` The value being converted

`-r / --fps` Frames per second

`-p / --bpm` Beats per second, required only if inputting ticks or beats

`-d / --division` Number of MIDI ticks per beat (division), default is 480, and required only if inputting ticks

## Optional Parameters
`--print` Print to the console