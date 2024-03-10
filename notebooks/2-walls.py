# %%
import cadquery as cq
from ocp_vscode import *

set_defaults(reset_camera=Camera.KEEP, axes=True, collapse=Collapse.LEAVES, grid=True)

%load_ext autoreload
%autoreload 2
%aimport -cadquery

# %%
import pathlib
from cadquery_skylark import wall_a, wall_b, wall_c, wall_d

export_directory = pathlib.Path(__file__).parent.parent / "exports"
names = ["part", "blue", "cyan", "green"]
colors = ["goldenrod", "blue", "cyan", "green"]

# %%
width, height = 600, 2400
p = wall_a.make_part(width, height)
filepath = export_directory / "SKYLARK250_WALL-M-A.step"
cq.exporters.export(p, str(filepath), opt={"write_pcurves": False})
show(p)

# %%
blue_w, cyan_w, green_w = wall_a.make_cnc(width, height, export_directory)
show(p, blue_w, cyan_w, green_w, names=names, colors=colors)

# %%
width, height = 600, 2400
p = wall_d.make_part(width, height)
filepath = export_directory / "SKYLARK250_WALL-M-D.step"
cq.exporters.export(p, str(filepath), opt={"write_pcurves": False})
show(p)

# %%
blue_w, cyan_w, green_w = wall_d.make_cnc(width, height, export_directory)
show(p, blue_w, cyan_w, green_w, names=names, colors=colors)

# %%
width, height = 318, 2400
p = wall_c.make_part(width, height)
filepath = export_directory / "SKYLARK250_WALL-M-C.step"
cq.exporters.export(p, str(filepath), opt={"write_pcurves": False})
show(p)

# %%
blue_w, cyan_w = wall_c.make_cnc(width, height, export_directory)
show(p, blue_w, cyan_w, names=names, colors=colors)

# %%
x_len, y_len = 600, 250+2*18
p = wall_b.make_part(x_len, y_len)
filepath = export_directory / "SKYLARK250_WALL-M-B.step"
cq.exporters.export(p, str(filepath), opt={"write_pcurves": False})
show(p)

# %%
blue_w = wall_b.make_cnc(x_len, y_len, export_directory)
show(p, blue_w, names=names, colors=colors)

# %%
