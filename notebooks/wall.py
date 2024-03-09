# %%
import cadquery as cq
from ocp_vscode import *

set_defaults(reset_camera=Camera.KEEP, axes=True, collapse=Collapse.LEAVES, grid=True)

%load_ext autoreload
%autoreload 2
%aimport -cadquery

# %%
from cadquery_skylark import details, wall_a, wall_d


# %%
show(details.bowtie())

# %%
show(details.t_slot(75))

# %%
show(details.bowtie_pair())

# %%
show(details.slot_pair())

# %%
show(details.round_cutouts())

# %%
show(details.corner())

# %%
show(details.middle_hole())

# %%
show(details.bowtie_handle())

# %%
show(details.bowtie_handle_pair())

# %%
height, width = 2400, 600
p = wall_a.make_part(width, height)
cq.exporters.export(p, "SKYLARK250_WALL-M-A.step", opt={"write_pcurves": False})

show(p)

# %%

blue_w, cyan_w, green_w = wall_a.make_cnc(width, height, '.')

show(p, blue_w, cyan_w, green_w, names=["part", "blue", "cyan", "green"], colors=["goldenrod", "blue", "cyan", "green"])


# %%
p = wall_d.make_part(width, height)
show(p)

# %%
blue_w, cyan_w, green_w = wall_d.make_cnc(width, height, '.')

show(p, blue_w, cyan_w, green_w, names=["part", "blue", "cyan", "green"], colors=["goldenrod", "blue", "cyan", "green"])
