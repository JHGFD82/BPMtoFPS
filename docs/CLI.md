# Command-Line Interface

BPMtoFPS provides an intuitive and powerful command-line interface for converting between music time and video time formats. Perfect for scripting, batch processing, and quick one-off conversions.

## Installation & Setup

Install BPMtoFPS via pip to access the command-line interface:

```bash
pip install BPMtoFPS
BPMtoFPS --version  # Verify installation
BPMtoFPS --help     # View help
```

## Quick Start

### Basic Syntax
```bash
BPMtoFPS [INPUT_FORMAT] [VALUE] [OPTIONS]
```

### Common Examples
```bash
# Convert 24 beats to frames
BPMtoFPS beats 24 --bpm 120 --fps 29.97

# Convert MIDI ticks to timecode  
BPMtoFPS ticks 1920 --bpm 140 --fps 24 --to timecode

# Convert multiple outputs
BPMtoFPS measures 8 --bpm 128 --notes-per-measure 4 --fps 30 --to all
```

## Input Formats

### beats
Convert musical beats to video timing.
```bash
BPMtoFPS beats [NUMBER] --bpm [BPM] --fps [FPS]

# Examples
BPMtoFPS beats 16 --bpm 120 --fps 29.97 --to frames
BPMtoFPS beats 32 -b 140 -f 24 --to timecode
```
**Required:** `--bpm`, `--fps` (for video outputs)

### ticks  
Convert MIDI ticks to video timing.
```bash
BPMtoFPS ticks [NUMBER] --bpm [BPM] --fps [FPS] [--ticks-per-beat [TPB]]

# Examples
BPMtoFPS ticks 960 --bpm 120 --fps 29.97
BPMtoFPS ticks 1440 -b 140 -f 24 --ticks-per-beat 360
```
**Required:** `--bpm`, `--fps` (for video outputs)  
**Optional:** `--ticks-per-beat` (default: 480)

### measures
Convert musical measures to video timing.
```bash
BPMtoFPS measures [NUMBER] --bpm [BPM] --notes-per-measure [NPM] --fps [FPS]

# Examples  
BPMtoFPS measures 8 --bpm 120 --notes-per-measure 4 --fps 29.97
BPMtoFPS measures 12 -b 90 -n 3 -f 24  # 3/4 time signature
```
**Required:** `--bpm`, `--notes-per-measure`, `--fps` (for video outputs)

### timecode
Convert timecode strings to other formats.
```bash
BPMtoFPS timecode "[MM:SS.SSS]" --fps [FPS]

# Examples
BPMtoFPS timecode "1:30.5" --fps 29.97 --to frames
BPMtoFPS timecode "45.25" -f 24 --to seconds  # Direct seconds input
```
**Required:** `--fps` (for video outputs)

### video-frames
Convert video frame numbers to time.
```bash
BPMtoFPS video-frames [NUMBER] --fps [FPS]

# Examples
BPMtoFPS video-frames 720 --fps 29.97 --to seconds
BPMtoFPS video-frames 1440 -f 24 --to timecode
```
**Required:** `--fps`

## Output Formats

Use the `--to` flag to specify output format(s):

### Single Output
```bash
--to frames      # Video frame numbers (default)
--to timecode    # Video timecode (ss:ff format)  
--to seconds     # Plain seconds with decimals
```

### Multiple Outputs
```bash
--to all         # All three formats: frames, timecode, seconds
```

### Examples
```bash
# Single output (default: frames)
BPMtoFPS beats 24 --bpm 120 --fps 29.97
# Output: Frames: 720

# Specific output format
BPMtoFPS beats 24 --bpm 120 --fps 29.97 --to timecode  
# Output: Timecode: 24:00

# Multiple outputs
BPMtoFPS beats 24 --bpm 120 --fps 29.97 --to all
# Output: 
# Frames: 720
# Timecode: 24:00  
# Seconds: 12.000
```

## Parameters Reference

### Required Parameters
| Parameter | Short | Description | Used With |
|-----------|-------|-------------|-----------|
| `--bpm` | `-b` | Beats per minute | beats, ticks, measures |
| `--fps` | `-f` | Frames per second | video outputs, video-frames |
| `--notes-per-measure` | `-n` | Quarter notes per measure | measures |

### Optional Parameters  
| Parameter | Short | Default | Description |
|-----------|-------|---------|-------------|
| `--ticks-per-beat` | `-t` | 480 | MIDI ticks per beat |
| `--to` | | frames | Output format |
| `--quiet` | `-q` | | Output values only (no labels) |
| `--no-output` | | | Suppress output (validation only) |

## Advanced Usage

### Quiet Mode for Scripting
Use `--quiet` to output only values, perfect for shell scripts:
```bash
# Regular output
BPMtoFPS beats 24 --bpm 120 --fps 29.97 --to all
# Frames: 720
# Timecode: 24:00
# Seconds: 12.000

# Quiet output  
BPMtoFPS beats 24 --bpm 120 --fps 29.97 --to all --quiet
# 720 24:00 12.0
```

### Validation Mode
Test parameters without output:
```bash
BPMtoFPS beats 24 --bpm 120 --fps 29.97 --no-output
# No output, but exits with error code if invalid
```

### Batch Processing Examples
```bash
#!/bin/bash
# Generate frame markers for beat positions
for beat in {4,8,12,16,20,24}; do
    frame=$(BPMtoFPS beats $beat --bpm 128 --fps 29.97 --quiet)
    echo "Beat $beat: Frame $frame"
done

# Process multiple timecodes  
echo "1:30.5\n2:15.2\n3:42.8" | while read timecode; do
    frame=$(BPMtoFPS timecode "$timecode" --fps 29.97 --quiet)
    echo "$timecode -> Frame $frame"
done
```

## Error Handling

BPMtoFPS provides clear error messages and appropriate exit codes:

```bash
# Missing required parameter
BPMtoFPS beats 24 --fps 29.97
# Error: --bpm is required when converting from beats

# Invalid input value  
BPMtoFPS beats abc --bpm 120 --fps 29.97
# Error: Input for beats must be an integer.

# Exit codes:
# 0: Success
# 1: Conversion error  
# 2: Argument parsing error
```

## Real-World Workflows

### Music Video Editing
```bash
# Generate cue markers for video editing
BPMtoFPS measures 1 --bpm 128 --notes-per-measure 4 --fps 29.97 --to all
BPMtoFPS measures 2 --bpm 128 --notes-per-measure 4 --fps 29.97 --to all  
BPMtoFPS measures 4 --bpm 128 --notes-per-measure 4 --fps 29.97 --to all
```

### MIDI Synchronization  
```bash
# Convert MIDI event positions to video frames
BPMtoFPS ticks 0 --bpm 120 --fps 24      # Song start
BPMtoFPS ticks 1920 --bpm 120 --fps 24   # First measure
BPMtoFPS ticks 3840 --bpm 120 --fps 24   # Second measure
```

### Live Performance Sync
```bash
# Generate timing cues for live show
for measure in {1..16}; do
    time=$(BPMtoFPS measures $measure --bpm 140 --notes-per-measure 4 --to seconds --quiet)
    echo "Measure $measure: ${time}s"
done
```

---

*For Python API usage, see [Functions.md](Functions.md)*
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