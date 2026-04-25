import io
import unittest
from contextlib import redirect_stdout, redirect_stderr
from typing import Dict, Tuple, Union
from unittest.mock import patch

from BPMtoFPS.cli import format_cli_output, main


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run_cli(*args: str) -> Tuple[str, str, Union[str, int, None]]:
    """Run main() with the given argv, capture stdout/stderr, return both.

    Returns a tuple (stdout_str, stderr_str, exit_code_or_None).
    exit_code_or_None is None when main() returns normally, or the integer
    exit code when SystemExit is raised.
    """
    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()
    exit_code = None
    with patch('sys.argv', ['BPMtoFPS', *args]):
        try:
            with redirect_stdout(stdout_buf), redirect_stderr(stderr_buf):
                main()
        except SystemExit as exc:
            exit_code = exc.code
    return stdout_buf.getvalue(), stderr_buf.getvalue(), exit_code


# ---------------------------------------------------------------------------
# format_cli_output
# ---------------------------------------------------------------------------

class TestFormatCliOutput(unittest.TestCase):

    def test_frames_only(self):
        self.assertEqual(format_cli_output({'frames': 225}), 'Frames: 225')

    def test_timecode_only(self):
        self.assertEqual(format_cli_output({'timecode': '00:00:07:15'}), 'Timecode: 00:00:07:15')

    def test_seconds_float(self):
        self.assertEqual(format_cli_output({'seconds': 7.5}), 'Seconds: 7.500')

    def test_seconds_int(self):
        self.assertEqual(format_cli_output({'seconds': 7}), 'Seconds: 7')

    def test_all_formats(self):
        result: Dict[str, Union[int, float, str]] = {'frames': 225, 'timecode': '00:00:07:15', 'seconds': 7.5}
        expected = 'Frames: 225\nTimecode: 00:00:07:15\nSeconds: 7.500'
        self.assertEqual(format_cli_output(result), expected)

    def test_quiet_single(self):
        self.assertEqual(format_cli_output({'frames': 225}, quiet=True), '225')

    def test_quiet_multiple(self):
        result: Dict[str, Union[int, float, str]] = {'frames': 225, 'timecode': '00:00:07:15'}
        self.assertEqual(format_cli_output(result, quiet=True), '225 00:00:07:15')


# ---------------------------------------------------------------------------
# main() — happy paths
# ---------------------------------------------------------------------------

class TestCliHappyPaths(unittest.TestCase):

    def test_beats_to_frames(self):
        stdout, _, code = run_cli('beats', '24', '-b', '192', '-f', '29.97', '--to', 'frames')
        self.assertIsNone(code)
        self.assertIn('225', stdout)

    def test_beats_to_timecode(self):
        stdout, _, code = run_cli('beats', '24', '-b', '192', '-f', '29.97', '--to', 'timecode')
        self.assertIsNone(code)
        self.assertIn('00:00:07:15', stdout)

    def test_ticks_to_timecode(self):
        stdout, _, code = run_cli('ticks', '240', '-b', '192', '-f', '29.97', '--to', 'timecode')
        self.assertIsNone(code)
        self.assertIn('00:00:00:04', stdout)

    def test_measures_to_seconds(self):
        stdout, _, code = run_cli('measures', '2', '-b', '120', '-n', '4', '--to', 'seconds')
        self.assertIsNone(code)
        self.assertIn('4.000', stdout)

    def test_timecode_to_seconds(self):
        stdout, _, code = run_cli('timecode', '1:30.5', '--to', 'seconds')
        self.assertIsNone(code)
        self.assertIn('90.500', stdout)

    def test_video_frames_to_seconds(self):
        stdout, _, code = run_cli('video-frames', '90', '-f', '30', '--to', 'seconds')
        self.assertIsNone(code)
        self.assertIn('3.000', stdout)

    def test_to_all(self):
        stdout, _, code = run_cli('beats', '24', '-b', '192', '-f', '29.97', '--to', 'all')
        self.assertIsNone(code)
        self.assertIn('Frames:', stdout)
        self.assertIn('Timecode:', stdout)
        self.assertIn('Seconds:', stdout)

    def test_quiet_flag(self):
        stdout, _, code = run_cli('beats', '24', '-b', '192', '-f', '29.97', '--to', 'frames',
                                  '--quiet')
        self.assertIsNone(code)
        self.assertEqual(stdout.strip(), '225')

    def test_no_output_flag(self):
        stdout, _, code = run_cli('beats', '24', '-b', '192', '-f', '29.97', '--to', 'frames',
                                  '--no-output')
        self.assertIsNone(code)
        self.assertEqual(stdout.strip(), '')

    def test_bpm_float(self):
        stdout, _, code = run_cli('beats', '4', '-b', '119.5', '-f', '30', '--to', 'seconds')
        self.assertIsNone(code)
        self.assertIn('Seconds:', stdout)

    def test_timecode_hh_mm_ss_input(self):
        stdout, _, code = run_cli('timecode', '1:30:15.5', '--to', 'seconds')
        self.assertIsNone(code)
        self.assertIn('5415.500', stdout)

    def test_default_output_is_frames(self):
        # --to defaults to 'frames' when omitted
        stdout, _, code = run_cli('beats', '24', '-b', '192', '-f', '29.97')
        self.assertIsNone(code)
        self.assertIn('Frames:', stdout)


# ---------------------------------------------------------------------------
# main() — error paths
# ---------------------------------------------------------------------------

class TestCliErrorPaths(unittest.TestCase):

    def test_missing_bpm_exits(self):
        _, stderr, code = run_cli('beats', '24', '-f', '29.97', '--to', 'frames')
        self.assertEqual(code, 2)
        self.assertIn('--bpm', stderr)

    def test_missing_fps_exits(self):
        _, stderr, code = run_cli('beats', '24', '-b', '120', '--to', 'frames')
        self.assertEqual(code, 2)
        self.assertIn('--fps', stderr)

    def test_missing_notes_per_measure_exits(self):
        _, stderr, code = run_cli('measures', '4', '-b', '120', '-f', '30', '--to', 'seconds')
        self.assertEqual(code, 2)
        self.assertIn('--notes-per-measure', stderr)

    def test_invalid_input_value_exits(self):
        _, stderr, code = run_cli('beats', 'notanumber', '-b', '120', '-f', '30', '--to', 'frames')
        self.assertEqual(code, 1)
        self.assertIn('Error:', stderr)

    def test_invalid_input_format_rejected_by_argparse(self):
        # argparse enforces choices, so an unknown format exits with code 2
        _, _stderr, code = run_cli('unknown_format', '24', '-b', '120', '-f', '30')
        self.assertEqual(code, 2)

    def test_unexpected_exception_exits_with_code_1(self):
        # Patch convert_time to raise a non-ValueError to hit the generic except branch
        with patch('BPMtoFPS.cli.convert_time', side_effect=RuntimeError('boom')):
            _, stderr, code = run_cli('beats', '24', '-b', '120', '-f', '30')
        self.assertEqual(code, 1)
        self.assertIn('Unexpected error', stderr)


if __name__ == '__main__':
    unittest.main()
