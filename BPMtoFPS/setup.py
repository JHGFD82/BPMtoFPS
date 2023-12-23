from setuptools import setup, find_packages

setup(
    name="BPMtoFPS",
    version="1.0.0",
    packages=find_packages(),
    author="Jeff Heller (JHGFD)",
    author_email="jeffheller@jhgfd.com",
    description="Convert time in a musical composition to time in a video production.",
    entry_points={
        'console_scripts': [
            'convert_audio_to_video_timing=BPMtoFPS.main:convert_audio_to_video_timing',
        ],
    },
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Video"
    ],
    python_requires='>=3.6',
    install_requires=[],
    include_package_data=True,
    zip_safe=False
)
