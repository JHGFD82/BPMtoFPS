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
    # Example test case. Adjust according to your function's logic.
    assert timecode_to_seconds("1:00") == 60


def test_seconds_to_frames():
    # Example test case. Adjust according to your function's logic.
    assert seconds_to_frames(1, 30) == 30


def test_seconds_to_timecode():
    # Add test cases for seconds_to_timecode function
    assert seconds_to_timecode(27.567, 29.97) == "27:16"


def test_convert_audio_to_video_timing():
    # Add test cases for convert_audio_to_video_timing function
    assert convert_time('ticks', 'timecode', 240, 192, 29.97) == '0:04'
