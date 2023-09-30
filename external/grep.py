import re
import sys

args = sys.argv
# Mimic 'grep' using 're' module
with open('filename', 'r') as f:
    lines = f.readlines()
matched_lines = [line for line in lines if re.search('pattern',line)]