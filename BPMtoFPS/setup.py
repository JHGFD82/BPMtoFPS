from setuptools import setup, find_packages

setup(
    name="BPMtoFPS",
    version="0.1.0",
    packages=find_packages(),
    author="Jeff Heller (JHGFD)",
    author_email="jeffheller@jhgfd.com",
    description=("Convert time in a musical composition to time in a video production. "
                 "This package has tools to take either a specific beat or point in time and "
                 "converts it to a video timecode or number of frames based on the beats per "
                 "minute of the song and the frames per second of the video."),
    entry_points={
        'console_scripts': [
            'convert_audio_to_video_timing=BPMtoFPS.main:convert_audio_to_video_timing',
        ],
    },
    python_requires='>=3.6',
    install_requires=[],
    include_package_data=True,
    zip_safe=False
)
