"""
Test for generating random CPPNs.

Author:     Aaron Stone
Date:       09/01/2022
"""
from make_cppn import load_cppn
import os


ORIGINAL = "cppns/115"
SAVE_DIR = "cppns/iteration_1"

NUM_PER_GENERATION = 10

# create the directory if it doesn't exist
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

current_path = ""
keep_going = True

while keep_going:
    cppn = load_cppn(ORIGINAL)
    for i in range(NUM_PER_GENERATION):
        cppn.evolve()
        cppn.save(SAVE_DIR)