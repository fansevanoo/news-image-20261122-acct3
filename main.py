"""Write the account-3 entry image to the output directory.

The entry image (entry.png) sits next to this script. This program
copies it, byte for byte, to MAKEFUN_OUTPUT_DIR (default /output)
as entry.png. Standard library only; no network, no randomness,
so both runs produce identical bytes.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SRC, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
