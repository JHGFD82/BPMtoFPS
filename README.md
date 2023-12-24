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