# %%
import cadquery as cq
from ocp_vscode import *

set_defaults(reset_camera=Camera.KEEP, axes=True, collapse=Collapse.LEAVES, grid=True)

%load_ext autoreload
%autoreload 2
%aimport -cadquery

# %%
from cadquery_skylark import details


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
outside = cq.Sketch().rect(width, height)

def bowtie_pair_points():
    for x in (-width/2, width/2):
        for y in range(-height//2 + 300, height//2, 600):
            yield x, y

outside.push(bowtie_pair_points())
outside.face(details.bowtie_pair(), mode='s')

def slot_pairs_points():
    for x in (-width/2, width/2):
        for y in range(-height//2 + 600, height//2, 600):
            yield x, y

outside.push(slot_pairs_points())
outside.face(details.slot_pair(), mode='s')

def top_and_bottom_bowtie_points():
    for x in (-194.9, 0, 194.9):
        for y in (-height/2, height/2):
            yield x, y

outside.push(top_and_bottom_bowtie_points())
outside.face(details.bowtie(), mode='s')

def corner_points(dx=0, dy=0):
    for x in (-(width/2-dx), width/2-dx):
        for y in (-(height/2-dy), height/2-dy):
            yield x, y

outside.push(corner_points()).face(details.corner(), mode='s').reset()

def middle_hole_points():
    for y in range(-height//2 + 600, height//2, 600):
        yield 0, y

inside = cq.Sketch()
inside.push(middle_hole_points()).face(details.middle_hole()).reset()

half = cq.Sketch()
half.push(bowtie_pair_points()).face(details.bowtie_handle_pair()).reset()
half.push(top_and_bottom_bowtie_points()).face(details.bowtie_handle()).reset()
half.rect(width+1, height+1, mode='i')

slot_trim = cq.Sketch()
slot_trim.push(slot_pairs_points()).rect(18*2, 62).reset()
slot_trim.rect(width+1, height+1, mode="i")
slot_trim.vertices().fillet(6).reset()

corner_trim = cq.Sketch()
corner_trim.push(corner_points(dy=52.5)).rect(18*2, 37).reset()
corner_trim.rect(width+1, height+1, mode="i")
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
blue = outside.wires().offset(-0.25, mode='i').reset().clean()
cyan = inside.wires().offset(0.25, mode='a').reset().clean()
green = half
blue_w = cq.Workplane("XY").add(blue.faces().vals())
cyan_w = cq.Workplane("XY").add(cyan.faces().vals())
green_w = cq.Workplane("XY").add(green.faces().vals())
dxf.add_layer("4_ANYTOOL_CUTTHROUGH_OUTSI", color=5)
dxf.add_shape(blue_w, "4_ANYTOOL_CUTTHROUGH_OUTSI")
dxf.add_layer("3_ANYTOOL_CUTTHROUGH_INSID", color=4)
dxf.add_shape(cyan_w, "3_ANYTOOL_CUTTHROUGH_INSID")
dxf.add_layer("5_ANYTOOL_HALF_MILL_9MM_IN", color=3)
dxf.add_shape(green_w, "5_ANYTOOL_HALF_MILL_9MM_IN")
dxf.document.saveas("SKYLARK250_WALL-M-face.dxf")

show(p, blue_w, cyan_w, green_w)
