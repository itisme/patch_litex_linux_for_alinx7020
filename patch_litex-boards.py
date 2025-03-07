import litex_boards
import shutil
from pathlib import Path
import sys

lbpath = Path(litex_boards.__file__).parent.parent.parent
if not lbpath.exists():
    print(f"litex_boards not found at {lbpath}")
    sys.exit(1)

files = ["litex-boards/litex_boards/platforms/alinx_ax7020.py", "litex-boards/litex_boards/targets/alinx_ax7020.py"]
for src in files:
    dst = lbpath / Path(src)
    if dst.exists():
        continue
    shutil.copyfile(src, dst)
    print(f"Copied to {dst}")
