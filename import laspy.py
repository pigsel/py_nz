import laspy
from pathlib import Path

lasfile = Path(r"C:\temp\t74_over_r50.las")
lasedit = Path(r"C:\temp\t74_over_r50_34.las")

with laspy.open(lasfile) as fh:
        las = fh.read()

las.z = las.z + 34

with laspy.open(lasedit, mode="w", header=las.header) as writer:
        writer.write_points(las.points)

print("Done")
