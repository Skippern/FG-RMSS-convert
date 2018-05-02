# FG-RMSS-convert
Convert between FantasyGround extension/mod format and irm_lib format

Purpose is to be able to convert between unpacked FantasyGround `.ext`/`.pak`/`.mod` files and `irm_lib` data. This will help in adjusting data in FantasyGround extensions towards the `irm_lib` data model.

# Usage

`fg2irm_lib.py --data <path to irm_lib data directory> --xml <path to XML file>`

This will generate a series of subfolders and `.json` files containing the data extracted from the XML input file.
