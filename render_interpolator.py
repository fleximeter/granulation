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
import query
import multiprocessing as mp
from datetime import datetime


# Automatically detect the platform and corresponding directories
# This would need to be manually edited for other environments
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


def render(grain_entry_categories, num_unique_grains_per_section, num_repetitions, grain_overlap_num, num_channels, source_dirs, out_dir, name):
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
                grain["distance_between_grains"] = grain_overlap_num
                grain["channel"] = 0
                grain_list.append(grain)
        # print(f"{len(grain_list)} grains added to the list")
        grain_source_lists.append(grain_list)
    
    # Duplicate some grains across boundaries
    NUM = 3
    SKIP = 3
    for i in range(len(grain_source_lists)):
        idxs = [rng.randrange(0, len(grain_source_lists[i])) for _ in range(NUM)]
        for idx in idxs:
            grain_source_lists[(i+SKIP) % len(grain_source_lists)].append(grain_source_lists[i][idx])
    
    assembled_grains_lists = []
    num = 0
    for l in grain_source_lists:
        fudge_factor = rng.randrange(-num_repetitions // 2, num_repetitions // 2)
        assembled_grains_lists.append(grain_assembler.assemble_repeat(l, num_repetitions + fudge_factor, grain_overlap_num))
        num += len(assembled_grains_lists[-1])

    # Repeat the chunks to make longer audio
    grains = assembled_grains_lists[0]
    for i in range(1, len(assembled_grains_lists)):
        overlap_num = int(min(len(grains), len(assembled_grains_lists[i])) * 0.95)
        grains = grains[:-overlap_num] + grain_assembler.interpolate(grains[-overlap_num:],
                                              assembled_grains_lists[i][:overlap_num]) + assembled_grains_lists[i][overlap_num:]
    grain_distances = grain_assembler.NthPowerEnvelope([grain_overlap_num, grain_overlap_num, int(grain_overlap_num * 0.35), 
                                                      grain_overlap_num, grain_overlap_num, int(grain_overlap_num * 0.35), grain_overlap_num, grain_overlap_num], 
                                                     [0, 5000, 5200, 5400, 
                                                      16000, 16200, 16400, 18000 ],
                                                      [2 for _ in range(11)], ["concave" for _ in range(11)])

    grain_assembler.swap_random_pair(grains, 0.2, rng)
    grain_assembler.spread_across_channels(grains, num_channels)
    # for i in range(len(grains)):
    #     grains[i]["distance_between_grains"] = grain_distances(i)
    grain_assembler.randomize_param(grains, "distance_between_grains", rng, 50)
    grain_assembler.calculate_grain_positions(grains)
    grain_sql.read_grains_from_file(grains, source_dirs)
    for i in range(len(grains)):
        print(f"Grain {i} length: {grains[i]['grain'].size}, source: {grains[i]['file']}, frames: {grains[i]['start_frame']}:{grains[i]['end_frame']}")
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
    GRAIN_LENGTH = 4096

    # Retrieve grain metadata and grains
    print("Retrieving grains...")
    db, cursor = grain_sql.connect_to_db(DB)
    grain_entry_categories = query.query1(GRAIN_LENGTH, cursor)
    db.close()

    # Generate candidate audio
    start = datetime.now()
    print("Rendering...")
    NUM_AUDIO_CANDIDATES = 1
    NUM_CHANNELS = 2
    NUM_UNIQUE_GRAINS = 10
    if NUM_AUDIO_CANDIDATES > 1:
        processes = [mp.Process(target=render, args=(grain_entry_categories, NUM_UNIQUE_GRAINS, 150, -GRAIN_LENGTH + 75, NUM_CHANNELS, SOURCE_DIRS, OUT, f"out_{i+1}.wav")) for i in range(NUM_AUDIO_CANDIDATES)]
    else:
        render(grain_entry_categories, NUM_UNIQUE_GRAINS, 200, -GRAIN_LENGTH + 75, NUM_CHANNELS, SOURCE_DIRS, OUT, "out_1.wav")    
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    duration = datetime.now() - start
    print("Elapsed time: {}:{:0>2}".format(duration.seconds // 60, duration.seconds % 60))
    