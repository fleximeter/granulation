# granulation

This is a repository for algorithmic granular synthesis. It uses a SQLite database of grains, and extracts grains from the database and a corresponding audio corpus that match certain criteria, then renders audio files.

# Building

The module `grain.grain_tools` uses Cython and must be compiled before usage: `python setup.py build_ext --inplace`

# Dependencies

`aus-python`, `cython`, `numpy`
