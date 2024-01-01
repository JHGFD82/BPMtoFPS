import pytest
from BPMtoFPS.main import (
    ticks_to_seconds,
    beats_to_seconds,
    timecode_to_seconds,
    seconds_to_frames,
    seconds_to_timecode,
    convert_time
)


def test_ticks_to_seconds():
    # Example test case. Adjust according to your function's logic.
    assert ticks_to_seconds(480, 120, 480) == 0.5


def test_beats_to_timecode():
    assert beats_to_seconds(24, 192) == 7.5


def test_timecode_to_seconds():
    assert timecode_to_seconds("1:12.622") == 72.62


def test_video_frames_to_seconds():
    assert video_frames_to_seconds(112, 30) == 3.73


def test_seconds_to_frames():
    # Example test case. Adjust according to your function's logic.
    assert seconds_to_frames(44.4, 29.97, frac=0.65) == 1331


def test_seconds_to_timecode():
    # Add test cases for seconds_to_timecode function
    assert seconds_to_timecode(27.567, 29.97) == "27:16"


def test_convert_time():
    # Add test cases for convert_audio_to_video_timing function
    assert convert_time('ticks', 'timecode', 240, 192, 29.97) == '0:04'


def test_convert_time_beats_both():
    assert convert_time('beats', 'both', 24, 192, 29.97) == (225, '7:15')


def test_convert_time_ticks_both():
    assert convert_time('ticks', 'both', 3840, 192, 29.97,
                        ticks_per_beat=360) == (100, '3:10')


def test_convert_time_timecode_both():
    assert convert_time('timecode', 'both', '0:45.59', fps=29.97) == (1366, '45:17')
