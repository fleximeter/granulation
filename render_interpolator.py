"""
File: render_interpolator.py

This grain realizer produces chunks of grains with different characteristics 
and interpolates from chunk to chunk to make a final audio product.
"""

import grain.grain_sql as grain_sql
import aus.audiofile as audiofile
import aus.operations as operations
import random
import scipy.signal as signal
from grain.effects import *
import grain.grain_assembler as grain_assembler
import os
import platform
import multiprocessing as mp
from datetime import datetime


MAC = "/Users/jmartin50/recording"
ARGON = "/Users/jmartin50/recording"
PC = "D:\\recording"
SYSTEM = platform.system()

if SYSTEM == "Darwin":
    SOURCE_DIRS = os.path.join(MAC, "samples/granulation_chunks")
    OUT = os.path.join(MAC, "out")
    DB = os.path.join(MAC, "data/grains.sqlite3")
    
elif SYSTEM == "Linux":
    SOURCE_DIRS = [os.path.join(ARGON, "samples/granulation_chunks"), os.path.join("/old_Users/jmartin50/recording", "samples/granulation_chunks")]
    OUT = os.path.join(ARGON, "out")
    DB = os.path.join(ARGON, "data/grains.sqlite3")

else:
    SOURCE_DIRS = os.path.join(PC, "samples\\granulation_chunks")
    OUT = os.path.join(PC, "out")
    DB = os.path.join(PC, "data/grains.sqlite3")


def render(grain_entry_categories, num_unique_grains_per_section, num_repetitions, overlap_num, num_channels, source_dirs, out_dir, name):
    """
    Renders an audio file
    :param grain_entry_categories: A list of grain record lists
    :param num_unique: The number of unique grains to use for each category
    :param num_channels: The number of channels in the output audio file
    :param source_dirs: The location(s) of the audio files
    :param out_dir: The output directory
    :param name: The output file name
    """
    DB = -6
    rng = random.Random()
    rng.seed()
    
    # Assemble the unique grain lists. There will be N lists, one for each SELECT statement.
    grain_source_lists = []
    for j, entry_category in enumerate(grain_entry_categories):
        grain_list = []
        # select NUM unique grains
        for _ in range(num_unique_grains_per_section):
            idx = rng.randrange(0, len(entry_category))
            if "church-bell" not in entry_category[idx]["file"]:
                grain = entry_category[idx]
                grain["distance_between_grains"] = overlap_num
                grain["channel"] = 0
                grain_list.append(grain)
        # print(f"{len(grain_list)} grains added to the list")
        grain_source_lists.append(grain_list)
    
    assembled_grains_lists = []
    num = 0
    for l in grain_source_lists:
        assembled_grains_lists.append(grain_assembler.assemble_repeat(l, num_repetitions, overlap_num))
        num += len(assembled_grains_lists[-1])

    # Repeat the chunks to make longer audio
    grains = assembled_grains_lists[0]
    for i in range(1, len(assembled_grains_lists)):
        overlap_num = int(min(len(grains), len(assembled_grains_lists[i])) * 0.95)
        grains = grains[:-overlap_num] + grain_assembler.interpolate(grains[-overlap_num:],
                                              assembled_grains_lists[i][:overlap_num]) + assembled_grains_lists[i][overlap_num:]
        
    grain_assembler.swap_random_pair(grains, 0.2, rng)
    grain_assembler.randomize_param(grains, "distance_between_grains", rng, 50)
    grain_assembler.spread_across_channels(grains, num_channels)
    grain_assembler.calculate_grain_positions(grains)
    grain_sql.read_grains_from_file(grains, source_dirs)
    for i in range(len(grains)):
        grains[i]["grain"] = operations.adjust_level(grains[i]["grain"], DB)
        
    grain_audio = grain_assembler.merge(grains, num_channels, np.hanning)
    grain_audio = operations.force_equal_energy(grain_audio, -3, 22000)

    # Apply final effects to the assembled audio
    lpf = signal.butter(2, 500, btype="lowpass", output="sos", fs=44100)
    hpf = signal.butter(8, 100, btype="highpass", output="sos", fs=44100)
    grain_audio = signal.sosfilt(lpf, grain_audio)
    grain_audio = signal.sosfilt(hpf, grain_audio)
    grain_audio = operations.fade_in(grain_audio, "hanning", 22050)
    grain_audio = operations.fade_out(grain_audio, "hanning", 22050)
    grain_audio = operations.adjust_level(grain_audio, -12)

    # Write the audio
    audio = audiofile.AudioFile(sample_rate=44100, bits_per_sample=24, num_channels=num_channels)
    audio.samples = grain_audio
    path = os.path.join(out_dir, name)
    print(f"Writing file {path} with {audio.samples.shape[-1]} samples")
    audiofile.write_with_pedalboard(audio, os.path.join(out_dir, name))
    # print("Done.")


if __name__ == "__main__":
    LENGTH = 4096
    SELECT = [
        # not specifying frequency
        """SELECT grains.* FROM grains
        INNER JOIN tags ON grains.id = tags.grain_id
        WHERE (grains.length = ?) AND (grains.spectral_flatness BETWEEN ? AND ?) AND (grains.spectral_roll_off_75 BETWEEN ? AND ?) 
            AND (grains.energy > ?) AND (grains.frequency IS NULL) AND (tags.tag = ?)
        GROUP BY grains.id;""",

        # specifying frequency
        """SELECT grains.* FROM grains
        INNER JOIN tags ON grains.id = tags.grain_id
        WHERE (grains.length = ?) AND (grains.spectral_flatness BETWEEN ? AND ?) AND (grains.spectral_roll_off_75 BETWEEN ? AND ?) 
            AND (grains.energy > ?) AND (grains.frequency BETWEEN ? AND ?) AND (tags.tag = ?)
        GROUP BY grains.id;""",
    ]

    PARAMS = [
        (0, (LENGTH, 0.4, 1.0, 200.0, 400.0, 0.05, 'animal')),
        (0, (LENGTH, 0.3, 0.6, 250.0, 450.0, 0.05, 'animal')),
        (0, (LENGTH, 0.3, 0.6, 300.0, 500.0, 0.05, 'animal')),
        (0, (LENGTH, 0.2, 0.5, 350.0, 550.0, 0.05, 'animal')),
        (0, (LENGTH, 0.2, 0.3, 400.0, 600.0, 0.05, 'animal')),
        (0, (LENGTH, 0.1, 0.3, 450.0, 650.0, 0.05, 'animal')),
        (0, (LENGTH, 0.1, 0.2, 500.0, 700.0, 0.05, 'animal')),
        (0, (LENGTH, 0.0, 0.2, 550.0, 750.0, 0.05, 'animal')),
        (0, (LENGTH, 0.0, 0.2, 600.0, 750.0, 0.05, 'animal')),
        (0, (LENGTH, 0.1, 0.3, 650.0, 800.0, 0.05, 'animal')),
        (0, (LENGTH, 0.1, 0.3, 700.0, 850.0, 0.05, 'animal')),
        (0, (LENGTH, 0.2, 0.4, 650.0, 800.0, 0.05, 'animal')),
        (0, (LENGTH, 0.2, 0.4, 600.0, 750.0, 0.05, 'animal')),
        (0, (LENGTH, 0.0, 0.2, 550.0, 700.0, 0.05, 'animal')),
        (0, (LENGTH, 0.0, 0.2, 500.0, 650.0, 0.05, 'animal')),
        (0, (LENGTH, 0.0, 0.2, 500.0, 600.0, 0.05, 'animal')),
    ]

    print("Retrieving grains...")
    # Retrieve grain metadata and grains
    db, cursor = grain_sql.connect_to_db(DB)
    grain_entry_categories = []
    for i, param in enumerate(PARAMS):
        cursor.execute(SELECT[param[0]], param[1])
        records = cursor.fetchall()
        if len(records) == 0:
            raise Exception(f"No grains found for index {i}.")
        entry_category = []
        for record in records:
            entry_category.append({grain_sql.FIELDS[i]: record[i] for i in range(len(record))})
        grain_entry_categories.append(entry_category)

    db.close()
    start = datetime.now()
    print("Rendering...")

    # Generate candidate audio
    NUM_AUDIO_CANDIDATES = 5
    NUM_CHANNELS = 2
    NUM_UNIQUE_GRAINS = 10
    # render(grain_entry_categories, NUM_UNIQUE_GRAINS, 200, -LENGTH + 75, NUM_CHANNELS, SOURCE_DIRS, OUT, "out_1.wav")
    processes = [mp.Process(target=render, args=(grain_entry_categories, NUM_UNIQUE_GRAINS, 200, -LENGTH + 75, NUM_CHANNELS, SOURCE_DIRS, OUT, f"out_{i+1}.wav")) for i in range(NUM_AUDIO_CANDIDATES)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    duration = datetime.now() - start
    print("Elapsed time: {}:{:0>2}".format(duration.seconds // 60, duration.seconds % 60))
    