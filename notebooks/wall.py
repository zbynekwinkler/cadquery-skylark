# %%
import cadquery as cq
from ocp_vscode import *

set_defaults(reset_camera=Camera.KEEP, axes=True, collapse=Collapse.LEAVES, grid=True)

%load_ext autoreload
%autoreload 2
%aimport -cadquery

# %%
from cadquery_skylark import details, wall_a


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
#cq.exporters.export(p, "SKYLARK250_WALL-M-face.step", opt={"write_pcurves": False})

show(p)

# %%
# https://cadquery.readthedocs.io/en/latest/classreference.html#cadquery.occ_impl.exporters.dxf.DxfDocument

from cadquery.occ_impl.exporters.dxf import DxfDocument
dxf = DxfDocument()
blue = wall_a.outside(width, height).wires().offset(-0.25, mode='i').reset().clean()
cyan = wall_a.inside(height).wires().offset(0.25, mode='a').reset().clean()
green = wall_a.half_depth(width, height).wires().offset(0.25, mode='a').reset().clean()
blue_w = cq.Workplane("XY").add(blue.faces().vals())
cyan_w = cq.Workplane("XY").add(cyan.faces().vals())
green_w = cq.Workplane("XY").add(green.faces().vals())
dxf.add_layer("4_ANYTOOL_CUTTHROUGH_OUTSI", color=5)
dxf.add_shape(blue_w, "4_ANYTOOL_CUTTHROUGH_OUTSI")
dxf.add_layer("3_ANYTOOL_CUTTHROUGH_INSID", color=4)
dxf.add_shape(cyan_w, "3_ANYTOOL_CUTTHROUGH_INSID")
dxf.add_layer("5_ANYTOOL_HALF_MILL_9MM_IN", color=3)
dxf.add_shape(green_w, "5_ANYTOOL_HALF_MILL_9MM_IN")
dxf.document.saveas("SKYLARK250_WALL-M-A.dxf")

show(p, blue_w, cyan_w, green_w, names=["part", "blue", "cyan", "green"])
