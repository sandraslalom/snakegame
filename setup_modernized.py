#!/usr/bin/env python3
"""
Setup script for Snake Game
"""
from setuptools import setup, find_packages

setup(
    name='snake_game',
    version='1.0.0',
    description='A classic snake game implementation using Pygame',
    author='Sandra Slalom',
    author_email='sandra@example.com',
    packages=find_packages(),
    install_requires=[
        'pygame>=2.0.0',
    ],
    entry_points={
        'console_scripts': [
            'snake-game=game:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Games/Entertainment :: Arcade',
    ],
    python_requires='>=3.6',
)