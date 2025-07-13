# Command-line Interface

BPMtoFPS provides an intuitive command-line interface for converting between music time and video time formats.

## Installation

Once installed via pip, you can use the `BPMtoFPS` command:

```bash
pip install BPMtoFPS
BPMtoFPS --help
```

## Basic Usage

The CLI follows a simple, readable pattern:

```bash
BPMtoFPS [INPUT_FORMAT] [VALUE] --bpm [BPM] --fps [FPS] --to [OUTPUT_FORMAT]
```

You can use either long form or short form parameters:

```bash
# Long form (self-documenting)
BPMtoFPS beats 24 --bpm 128 --fps 29.97 --to frames

# Short form (quick typing)
BPMtoFPS beats 24 -b 128 -f 29.97 --to frames

# Mixed (common usage)
BPMtoFPS measures 8 -b 140 --notes-per-measure 4 -f 30 --to all
```

## Input Formats

Choose one of these input formats as the first argument:

- **`beats`** - Musical beats (requires `--bpm`)
- **`ticks`** - MIDI ticks (requires `--bpm`)  
- **`measures`** - Musical measures (requires `--bpm` and `--notes-per-measure`)
- **`timecode`** - Time in mm:ss.sss format
- **`video-frames`** - Video frame numbers (requires `--fps`)

## Output Formats

Use the `--to` flag to specify output format:

- **`frames`** - Video frame numbers (default)
- **`timecode`** - Video timecode in ss:ff format
- **`seconds`** - Time in seconds
- **`all`** - All three formats

## Required Parameters

Depending on your input and output formats, you may need:

- **`-b, --bpm`** - Beats per minute (required for beats, ticks, measures)
- **`-f, --fps`** - Frames per second (required for video outputs or video-frames input)
- **`-n, --notes-per-measure`** - Quarter notes per measure (required for measures)

## Optional Parameters

- **`-t, --ticks-per-beat`** - MIDI resolution (default: 480)
- **`-q, --quiet`** - Output only values (useful for scripting)
- **`--no-output`** - Suppress all output (useful for validation)

## Examples

### Convert beats to video frames
```bash
# Long form
BPMtoFPS beats 24 --bpm 128 --fps 29.97 --to frames
# Output: Frames: 337

# Short form
BPMtoFPS beats 24 -b 128 -f 29.97 --to frames
# Output: Frames: 337
```

### Convert MIDI ticks to timecode
```bash
BPMtoFPS ticks 480 -b 120 -f 24 --to timecode
# Output: Timecode: 0:12
```

### Convert timecode to seconds
```bash
BPMtoFPS timecode "1:30.5" --fps 25 --to seconds
# Output: Seconds: 90.500
```

### Convert measures to all formats
```bash
BPMtoFPS measures 8 -b 140 -n 4 -f 30 --to all
# Output:
# Seconds: 13.714
# Frames: 411
# Timecode: 13:21
```

### Convert video frames to seconds
```bash
BPMtoFPS video-frames 720 -f 24 --to seconds
# Output: Seconds: 30.000
```

## Alternative Usage

You can also run the CLI directly from the source:

```bash
# From the project directory
python BPMtoFPS/main.py beats 24 -b 128 -f 29.97 --to frames

# Or as a module
python -m BPMtoFPS.cli beats 24 -b 128 -f 29.97 --to frames
```

## Error Handling

The CLI provides clear error messages for missing requirements:

```bash
BPMtoFPS beats 24 --fps 29.97 --to frames
# Error: --bpm is required when converting from beats

BPMtoFPS measures 8 -b 140 -f 30 --to frames  
# Error: --notes-per-measure is required when converting from measures
```

## Scripting Support

Use `--quiet` for machine-readable output:

```bash
BPMtoFPS beats 24 --bpm 128 --fps 29.97 --to frames --quiet
# Output: 337
```

This makes it easy to use in scripts:

```bash
#!/bin/bash
FRAMES=$(BPMtoFPS beats 24 --bpm 128 --fps 29.97 --to frames --quiet)
echo "Video should start at frame $FRAMES"
```