"""
Constants used throughout the BPMtoFPS package.
"""

# MIDI and timing constants
DEFAULT_TICKS_PER_BEAT = 480  # MIDI resolution
SECONDS_PER_MINUTE = 60
DEFAULT_ROUNDING_THRESHOLD = 0.75  # Threshold for frame rounding

# Maintain backward compatibility
TPB = DEFAULT_TICKS_PER_BEAT
SPM = SECONDS_PER_MINUTE
fraction = DEFAULT_ROUNDING_THRESHOLD
