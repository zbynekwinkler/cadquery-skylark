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
outside = wall_a.outside(width, height)

def middle_hole_points():
    for y in range(-height//2 + 600, height//2, 600):
        yield 0, y

inside = cq.Sketch()
inside.push(middle_hole_points()).face(details.middle_hole()).reset()

half = cq.Sketch()
half.push(wall_a._bowtie_pair_points(width, height)).face(details.bowtie_handle_pair()).reset()
half.push(wall_a._top_and_bottom_bowtie_points(height)).face(details.bowtie_handle()).reset()
half.rect(width, height, mode='i')

slot_trim = cq.Sketch()
slot_trim.push(wall_a._slot_pairs_points(width, height)).rect(18*2, 62).reset()
slot_trim.rect(width, height, mode="i")
slot_trim.vertices().fillet(6).reset()

corner_trim = cq.Sketch()
corner_trim.push(wall_a._corner_points(width, height, dy=52.5)).rect(18*2, 37).reset()
corner_trim.rect(width, height, mode="i")
corner_trim.vertices().fillet(6).reset()

half.face(slot_trim).face(corner_trim)

p = cq.Workplane("XY").placeSketch(outside).extrude(18)
p = p.faces(">Z").placeSketch(inside).cutThruAll()
p = p.faces(">Z").placeSketch(half).cutBlind(-18/2)

#cq.exporters.export(p, "SKYLARK250_WALL-M-face.step", opt={"write_pcurves": False})

show(p, slot_trim, corner_trim)

# %%
# https://cadquery.readthedocs.io/en/latest/classreference.html#cadquery.occ_impl.exporters.dxf.DxfDocument

from cadquery.occ_impl.exporters.dxf import DxfDocument
dxf = DxfDocument()
blue = outside.copy().wires().offset(-0.25, mode='i').reset().clean()
cyan = inside.copy().wires().offset(0.25, mode='a').reset().clean()
green = half.copy().wires().offset(0.25, mode='a').reset().clean()
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
