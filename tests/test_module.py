import unittest
from BPMtoFPS.converters import (
    ticks_to_seconds,
    beats_to_seconds,
    measures_to_seconds,
    timecode_to_seconds,
    video_frames_to_seconds,
    seconds_to_frames,
    seconds_to_timecode,
)
from BPMtoFPS import convert_time


class TestBPMtoFPS(unittest.TestCase):

    def test_ticks_to_seconds(self):
        self.assertEqual(ticks_to_seconds(480, 120, 480), 0.5)

    def test_beats_to_timecode(self):
        self.assertEqual(beats_to_seconds(24, 192), 7.5)

    def test_measures_to_seconds(self):
        self.assertEqual(round(measures_to_seconds(392, 208, 6), 5), 678.46154)

    def test_timecode_to_seconds_mm_ss(self):
        self.assertEqual(timecode_to_seconds("1:12.622"), 72.622)

    def test_timecode_to_seconds_hh_mm_ss(self):
        self.assertEqual(timecode_to_seconds("1:30:15.5"), 5415.5)

    def test_timecode_to_seconds_bare_seconds(self):
        self.assertEqual(timecode_to_seconds("45.25"), 45.25)

    def test_video_frames_to_seconds(self):
        self.assertAlmostEqual(video_frames_to_seconds(112, 30), 112 / 30)

    def test_seconds_to_frames(self):
        self.assertEqual(seconds_to_frames(44.4, 29.97, frac=0.65), 1331)

    def test_seconds_to_timecode(self):
        self.assertEqual(seconds_to_timecode(27.567, 29.97), "00:00:27:16")

    def test_seconds_to_timecode_with_minutes(self):
        self.assertEqual(seconds_to_timecode(90.0, 30.0), "00:01:30:00")

    def test_seconds_to_seconds(self):
        self.assertEqual(convert_time('timecode', 'seconds', "45.2525"), {'seconds': 45.2525})

    def test_convert_time(self):
        self.assertEqual(convert_time('ticks', 'timecode', 240, 192, 29.97), {'timecode': '00:00:00:04'})

    def test_convert_time_beats_frames_timecode(self):
        self.assertEqual(convert_time('beats', ['frames', 'timecode'], 24, 192, 29.97),
                         {'frames': 225, 'timecode': '00:00:07:15'})

    def test_convert_time_ticks_frames_timecode(self):
        self.assertEqual(convert_time('ticks', ['frames', 'timecode'], 3840, 192, 29.97,
                            ticks_per_beat=360), {'frames': 100, 'timecode': '00:00:03:10'})

    def test_convert_time_timecode_frames_timecode_seconds(self):
        self.assertEqual(convert_time('timecode', ['frames', 'timecode', 'seconds'], '0:45.59',
                            fps=29.97), {'frames': 1366, 'timecode': '00:00:45:17', 'seconds': 45.59})

    def test_convert_time_output_order_preserved(self):
        # seconds requested last; it should appear last in the result dict
        result = convert_time('timecode', ['frames', 'timecode', 'seconds'], '0:45.59', fps=29.97)
        self.assertEqual(list(result.keys()), ['frames', 'timecode', 'seconds'])

    def test_bpm_float(self):
        # Fractional BPM should be accepted
        self.assertAlmostEqual(beats_to_seconds(4, 119.5), 4 / 119.5 * 60)

    def test_convert_time_frac_parameter(self):
        # Custom frac should be passed through to frame rounding.
        # 2 beats at 120 BPM = 1.0s; 1.0 * 29.97 = 29.97 (frac=0.97)
        # default frac=0.75: 0.97 >= 0.75 → rounds up to 30
        # custom  frac=0.99: 0.97 <  0.99 → rounds down to 29
        result_default = convert_time('beats', 'frames', 2, bpm=120, fps=29.97)
        result_custom = convert_time('beats', 'frames', 2, bpm=120, fps=29.97, frac=0.99)
        self.assertEqual(result_default['frames'], 30)
        self.assertEqual(result_custom['frames'], 29)


if __name__ == '__main__':
    unittest.main()
