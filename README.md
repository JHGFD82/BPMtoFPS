# BPMtoFPS

Convert time between musical and video production formats with precision and ease.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Overview

BPMtoFPS bridges the gap between music production and video editing by providing precise conversions between different time formats. Whether you're creating music videos, visualizations, or need to sync audio and video workflows, this package handles the complex timing calculations for you.

**Perfect for:**
- 🎵 Music video editors syncing beats to visual effects
- 🎬 Video producers working with musical content  
- 🎛️ Audio engineers collaborating with video teams
- 🎨 Visual artists creating music visualizations
- 🎪 Live performers synchronizing multimedia shows

## Quick Start

### Installation
```bash
pip install BPMtoFPS
```

### Basic Usage
```python
from BPMtoFPS import convert_time

# Convert 24 beats at 120 BPM to video frames at 29.97 FPS
result = convert_time('beats', 'frames', 24, bpm=120, fps=29.97)
print(result)  # {'frames': 720}

# Convert multiple output formats at once
result = convert_time('beats', ['frames', 'timecode', 'seconds'], 
                     24, bpm=120, fps=29.97)
print(result)  # {'frames': 720, 'timecode': '24:00', 'seconds': 12.0}
```

### Command Line Usage
```bash
# Convert beats to frames
BPMtoFPS beats 24 --bpm 120 --fps 29.97 --to frames

# Convert with multiple outputs
BPMtoFPS measures 8 --bpm 140 --notes-per-measure 4 --fps 30 --to all
```

## Supported Conversions

### Input Formats
| Format | Description | Example | Required Parameters |
|--------|-------------|---------|-------------------|
| **`beats`** | Musical beats | `24` | `bpm` |
| **`ticks`** | MIDI ticks | `1920` | `bpm`, `ticks_per_beat` |
| **`measures`** | Musical measures | `8` | `bpm`, `notes_per_measure` |
| **`timecode`** | Time string | `"1:30.5"` | None |
| **`video_frames`** | Video frames | `720` | `fps` |

### Output Formats  
| Format | Description | Example | Required Parameters |
|--------|-------------|---------|-------------------|
| **`frames`** | Video frame numbers | `720` | `fps` |
| **`timecode`** | Video timecode | `"24:00"` | `fps` |
| **`seconds`** | Plain seconds | `12.0` | None |

## Real-World Examples

### Music Video Production
```python
# Find the exact frame for a beat drop at measure 32
result = convert_time('measures', 'frames', 32, 
                     bpm=128, notes_per_measure=4, fps=29.97)
# Use result['frames'] to place your effect

# Sync multiple beat markers for a sequence
beats = [16, 32, 48, 64]
for beat in beats:
    frame = convert_time('beats', 'frames', beat, bpm=128, fps=29.97)
    print(f"Beat {beat}: Frame {frame['frames']}")
```

### MIDI to Video Sync
```python
# Convert MIDI tick positions to video timeline
midi_events = [480, 960, 1440, 1920]  # Quarter note positions
for tick in midi_events:
    result = convert_time('ticks', ['frames', 'timecode'], tick,
                         bpm=120, fps=24, ticks_per_beat=480)
    print(f"Tick {tick}: Frame {result['frames']}, Time {result['timecode']}")
```

### Live Performance Sync
```python
# Generate cue points for a live show
measures = range(1, 17)  # 16 measures
cue_points = []
for measure in measures:
    result = convert_time('measures', 'seconds', measure,
                         bpm=140, notes_per_measure=4)
    cue_points.append(result['seconds'])
```

## Advanced Features

### Smart Frame Rounding
BPMtoFPS uses intelligent rounding for frame calculations. By default, fractional frames are rounded up when ≥ 0.75, providing better sync accuracy for musical timing.

```python
# Custom rounding threshold
from BPMtoFPS import seconds_to_frames

frames = seconds_to_frames(2.8, fps=30, frac=0.5)  # Round at 50%
```

### Direct Function Access
For specialized use cases, access conversion functions directly:

```python
from BPMtoFPS import beats_to_seconds, seconds_to_frames

# Two-step conversion with custom processing
seconds = beats_to_seconds(24, 120)
# ... custom processing ...
frames = seconds_to_frames(seconds, 29.97)
```

### Batch Processing
```python
# Process multiple timecodes
timecodes = ["1:30.5", "2:15.2", "3:42.8"]
results = []
for tc in timecodes:
    result = convert_time('timecode', 'frames', tc, fps=29.97)
    results.append(result['frames'])
```

## Error Handling

BPMtoFPS provides clear error messages for common issues:

```python
try:
    result = convert_time('beats', 'frames', 24, fps=29.97)  # Missing bpm!
except ValueError as e:
    print(f"Error: {e}")  # "bpm is required for beats conversion"
```

## Documentation

- **[CLI Documentation](docs/CLI.md)** - Complete command-line interface guide
- **[Function Reference](docs/Functions.md)** - Direct function usage and examples
- **[API Documentation](https://github.com/JHGFD82/BPMtoFPS)** - Full API reference

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.