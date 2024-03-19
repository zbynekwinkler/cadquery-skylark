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

names = ["part", "blue", "cyan", "green"]
colors = ["goldenrod", "blue", "cyan", "green"]

# %%
height = 2400+300
p = wall_a.make_part(height)
show(p)

# %%
blue_w, cyan_w, green_w = wall_a.make_cnc(height)
show(p, blue_w, cyan_w, green_w, names=names, colors=colors)

# %%
height = 2400
p = wall_d.make_part(height)
show(p)

# %%
blue_w, cyan_w, green_w = wall_d.make_cnc(height)
show(p, blue_w, cyan_w, green_w, names=names, colors=colors)

# %%
height = 2400
p = wall_c.make_part(height)
show(p)

# %%
blue_w, cyan_w = wall_c.make_cnc(height)
show(p, blue_w, cyan_w, names=names, colors=colors)

# %%
p = wall_b.make_part()
show(p)

# %%
blue_w = wall_b.make_cnc()
show(p, blue_w, names=names, colors=colors)

# %%
