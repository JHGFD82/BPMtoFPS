"""
Input validation functions for BPMtoFPS package.
"""

from typing import Union
from .models import InputFormat


def validate_input_value(input_value: Union[int, str, float], ref_format: str) -> Union[int, str]:
    """Validate and convert input value based on reference format.
    
    Args:
        input_value (Union[int, str, float]): The input value to validate.
        ref_format (str): The reference format type ('ticks', 'beats', 'measures', 
            'timecode', 'video_frames').
        
    Returns:
        Union[int, str]: Properly typed input value (int for numeric formats, 
            str for timecode).
        
    Raises:
        ValueError: If input value is invalid for the given format, or if a float 
            is provided (floats are not accepted).
            
    Example:
        >>> # Validate integer for beats
        >>> result = validate_input_value(24, 'beats')
        >>> print(result, type(result))
        24 <class 'int'>
        
        >>> # Validate string for timecode
        >>> result = validate_input_value("1:30.5", 'timecode')
        >>> print(result, type(result))
        1:30.5 <class 'str'>
        
        >>> # This will raise ValueError
        >>> try:
        ...     validate_input_value(24.5, 'beats')
        ... except ValueError as e:
        ...     print("ValueError:", str(e)[:50] + "...")
        ValueError: Input must be a string for timecodes or an inte...
    """
    # Do not allow floats under any circumstances. While timecode can have a float in seconds, 
    # it must be entered as string.
    if isinstance(input_value, float):
        raise ValueError("Input must be a string for timecodes or an integer for beats and ticks. "
                        "Floats are not accepted.")

    # Convert input value to integer if numeric format is specified
    numeric_formats = {InputFormat.TICKS.value, InputFormat.BEATS.value, 
                      InputFormat.MEASURES.value, InputFormat.VIDEO_FRAMES.value}
    
    if ref_format in numeric_formats:
        try:
            return int(input_value)
        except ValueError:
            raise ValueError(f"Input for {ref_format} must be an integer.")
    else:
        return str(input_value)
