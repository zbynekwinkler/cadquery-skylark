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

def corner_points():
    for x in (-width/2, width/2):
        for y in (-height/2, height/2):
            yield x, y

outside.push(corner_points()).face(details.corner(), mode='s').reset()

p = cq.Workplane("XY").placeSketch(outside).extrude(18)

def middle_hole_points():
    for y in range(-height//2 + 600, height//2, 600):
        yield 0, y

inside = cq.Sketch()
inside.push(middle_hole_points()).face(details.middle_hole()).reset()

p = p.faces(">Z").placeSketch(inside).cutThruAll()

#cq.exporters.export(p, "SKYLARK250_WALL-M-face.step", opt={"write_pcurves": False})
show(p, reset_camera=Camera.KEEP)

# 5_ANYTOOL_HALF_MILL_9MM_IN green

# %%
# https://cadquery.readthedocs.io/en/latest/classreference.html#cadquery.occ_impl.exporters.dxf.DxfDocument

from cadquery.occ_impl.exporters.dxf import DxfDocument
dxf = DxfDocument()
blue = outside.wires().offset(-0.25, mode='i').reset().clean()
cyan = inside.wires().offset(0.25, mode='a').reset().clean()
blue_w = cq.Workplane("XY").add(blue.faces().vals())
cyan_w = cq.Workplane("XY").add(cyan.faces().vals())
dxf.add_layer("4_ANYTOOL_CUTTHROUGH_OUTSI", color=5)
dxf.add_shape(blue_w, "4_ANYTOOL_CUTTHROUGH_OUTSI")
dxf.add_layer("3_ANYTOOL_CUTTHROUGH_INSID", color=4)
dxf.add_shape(cyan_w, "3_ANYTOOL_CUTTHROUGH_INSID")
dxf.document.saveas("SKYLARK250_WALL-M-face.dxf")

show(p, blue_w, cyan_w)
