from setuptools import setup, find_packages

setup(
    name='air-pong-game',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='Air Pong Game with Real Hand Control using OpenCV and MediaPipe',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'opencv-python',
        'mediapipe',
    ],
    entry_points={
        'console_scripts': [
            'air-pong-game=main:main',
        ],
    },
)