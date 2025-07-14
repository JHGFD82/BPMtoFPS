"""
Command-line interface for BPMtoFPS package.
"""

import argparse
import sys
from typing import Dict, Union

from .models import InputFormat, OutputFormat
from .constants import DEFAULT_TICKS_PER_BEAT
from .main import convert_time


def format_cli_output(result: Dict[str, Union[int, float, str]], quiet: bool = False) -> str:
    """Format the conversion result for CLI output in a user-friendly way.
    
    Args:
        result (Dict[str, Union[int, float, str]]): Dictionary containing conversion 
            results from convert_time().
        quiet (bool, optional): If True, return only values without labels for 
            piping. Defaults to False.
        
    Returns:
        str: Formatted string for CLI output. If quiet=True, returns space-separated 
            values. Otherwise, returns human-readable labeled output.
            
    Example:
        >>> result = {'frames': 720, 'timecode': '24:00'}
        >>> print(format_cli_output(result))
        Frames: 720
        Timecode: 24:00
        
        >>> print(format_cli_output(result, quiet=True))
        720 24:00
    """
    if quiet:
        # Return only values, space-separated for piping
        return ' '.join(str(v) for v in result.values())
    
    # Format for human-readable output
    formatted_lines: list[str] = []
    for key, value in result.items():
        if key == 'frames':
            formatted_lines.append(f"Frames: {value}")
        elif key == 'timecode':
            formatted_lines.append(f"Timecode: {value}")
        elif key == 'seconds':
            if isinstance(value, float):
                formatted_lines.append(f"Seconds: {value:.3f}")
            else:
                formatted_lines.append(f"Seconds: {value}")
    
    return '\n'.join(formatted_lines)


def main():
    """Main CLI entry point.
    
    Parses command-line arguments and executes the BPMtoFPS conversion,
    then formats and displays the results.
    
    Raises:
        SystemExit: If argument parsing fails, required parameters are missing,
            or conversion encounters an error. Exit codes: 1 for ValueError,
            1 for unexpected errors, 2 for argument parsing errors (from argparse).
    """
    parser = argparse.ArgumentParser(
        description='Convert between music time and video time formats',
        epilog='''
Examples:
  %(prog)s beats 24 --bpm 128 --fps 29.97 --to frames
  %(prog)s beats 24 -b 128 -f 29.97 --to frames  
  %(prog)s ticks 480 -b 120 -f 24 --to timecode  
  %(prog)s timecode "1:30.5" --fps 25 --to seconds
  %(prog)s measures 8 -b 140 -n 4 -f 30 --to all
  %(prog)s video-frames 720 -f 24 --to seconds
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Add version info
    parser.add_argument('--version', action='version', version='BPMtoFPS 1.4.0')

    # Input format as positional argument (much clearer!)
    parser.add_argument('input_format', 
                       choices=['beats', 'ticks', 'measures', 'timecode', 'video-frames'],
                       help='Input format type')
    
    # Input value as second positional argument
    parser.add_argument('input_value', type=str,
                       help='Value to convert (number for beats/ticks/measures/frames, "mm:ss.sss" for timecode)')

    # Output format - much clearer than cryptic flags
    parser.add_argument('--to', dest='output_format', 
                       choices=['frames', 'timecode', 'seconds', 'all'],
                       default='frames',
                       help='Output format (default: frames)')

    # Required/optional parameters with clear names
    parser.add_argument('-b', '--bpm', type=int,
                       help='Beats per minute (required for beats, ticks, measures)')
    parser.add_argument('-f', '--fps', type=float,
                       help='Frames per second (required for video outputs)')
    parser.add_argument('-t', '--ticks-per-beat', type=int, default=DEFAULT_TICKS_PER_BEAT,
                       help=f'MIDI ticks per beat (default: {DEFAULT_TICKS_PER_BEAT})')
    parser.add_argument('-n', '--notes-per-measure', type=int,
                       help='Quarter notes per measure (required for measures)')

    # Output control
    parser.add_argument('-q', '--quiet', action='store_true',
                       help='Output only values (useful for scripting)')
    parser.add_argument('--no-output', action='store_true',
                       help='Suppress all output (useful for validation)')

    args = parser.parse_args()

    # Convert input format to internal format
    input_format_map = {
        'beats': InputFormat.BEATS.value,
        'ticks': InputFormat.TICKS.value, 
        'measures': InputFormat.MEASURES.value,
        'timecode': InputFormat.TIMECODE.value,
        'video-frames': InputFormat.VIDEO_FRAMES.value
    }
    
    # Handle output formats
    if args.output_format == 'all':
        output_formats = [OutputFormat.FRAMES.value, OutputFormat.TIMECODE.value, OutputFormat.SECONDS.value]
    else:
        output_format_map = {
            'frames': OutputFormat.FRAMES.value,
            'timecode': OutputFormat.TIMECODE.value,
            'seconds': OutputFormat.SECONDS.value
        }
        output_formats = [output_format_map[args.output_format]]

    # Validate required parameters with clear error messages
    input_type = input_format_map[args.input_format]
    
    # Check for BPM requirement
    if input_type in [InputFormat.BEATS.value, InputFormat.TICKS.value, InputFormat.MEASURES.value]:
        if args.bpm is None:
            parser.error(f"--bpm is required when converting from {args.input_format}")
    
    # Check for notes per measure requirement  
    if input_type == InputFormat.MEASURES.value and args.notes_per_measure is None:
        parser.error("--notes-per-measure is required when converting from measures")
    
    # Check for FPS requirement
    video_outputs = [OutputFormat.FRAMES.value, OutputFormat.TIMECODE.value]
    video_inputs = [InputFormat.VIDEO_FRAMES.value]
    
    needs_fps = (any(fmt in video_outputs for fmt in output_formats) or 
                input_type in video_inputs)
    
    if needs_fps and args.fps is None:
        parser.error("--fps is required for video-related conversions")

    try:
        # Perform conversion
        result = convert_time(
            input_type,
            output_formats, 
            args.input_value,
            args.bpm,
            args.fps,
            args.ticks_per_beat,
            args.notes_per_measure,
            do_print=False
        )
        
        # Output results
        if not args.no_output:
            output = format_cli_output(result, args.quiet)
            print(output)
            
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
