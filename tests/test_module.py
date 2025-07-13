import unittest
from BPMtoFPS.main import (
    ticks_to_seconds,
    beats_to_seconds,
    measures_to_seconds,
    timecode_to_seconds,
    video_frames_to_seconds,
    seconds_to_frames,
    seconds_to_timecode,
    convert_time
)


class TestBPMtoFPS(unittest.TestCase):

    def test_ticks_to_seconds(self):
        self.assertEqual(ticks_to_seconds(480, 120, 480), 0.5)

    def test_beats_to_timecode(self):
        self.assertEqual(beats_to_seconds(24, 192), 7.5)

    def test_measures_to_seconds(self):
        self.assertEqual(round(measures_to_seconds(392, 208, 6), 5), 678.46154)

    def test_timecode_to_seconds(self):
        self.assertEqual(timecode_to_seconds("1:12.622"), 72.622)

    def test_video_frames_to_seconds(self):
        self.assertEqual(video_frames_to_seconds(112, 30), 3.73)

    def test_seconds_to_frames(self):
        self.assertEqual(seconds_to_frames(44.4, 29.97, frac=0.65), 1331)

    def test_seconds_to_timecode(self):
        self.assertEqual(seconds_to_timecode(27.567, 29.97), "27:16")

    def test_seconds_to_seconds(self):
        self.assertEqual(convert_time('timecode', 'seconds', "45.2525"), {'seconds': 45.2525})

    def test_convert_time(self):
        self.assertEqual(convert_time('ticks', 'timecode', 240, 192, 29.97), {'timecode': '0:04'})

    def test_convert_time_beats_frames_timecode(self):
        self.assertEqual(convert_time('beats', ['frames', 'timecode'], 24, 192, 29.97), {'frames': 225, 'timecode': '7:15'})

    def test_convert_time_ticks_frames_timecode(self):
        self.assertEqual(convert_time('ticks', ['frames', 'timecode'], 3840, 192, 29.97,
                            ticks_per_beat=360), {'frames': 100, 'timecode': '3:10'})

    def test_convert_time_timecode_frames_timecode_seconds(self):
        self.assertEqual(convert_time('timecode', ['frames', 'timecode', 'seconds'], '0:45.59',
                            fps=29.97), {'frames': 1366, 'timecode': '45:17', 'seconds': 45.59})


if __name__ == '__main__':
    unittest.main()
