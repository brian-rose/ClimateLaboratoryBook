import sys
from pathlib import Path

path = Path(__file__).resolve()  # this file
this_dir = path.parent  # this folder
notebooks_dir = this_dir
root_dir = notebooks_dir.parents[1]
data_dir = root_dir / Path("data")
test_dir = root_dir / Path("test_data")
map_dir = root_dir / Path("map_data")

sys.path.insert(0,str(root_dir))
sep = "*" * 30
print(f"{sep}\ncontext imported. Front of path:\n{sys.path[0]}\n"
      f"back of path: {sys.path[-1]}\n{sep}\n")
