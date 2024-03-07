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
face = cq.Sketch().rect(width, height)

def bowtie_pair_points():
    for x in (-width/2, width/2):
        for y in range(-height//2 + 300, height//2, 600):
            yield x, y

face.push(bowtie_pair_points())
face.face(details.bowtie_pair(), mode='s')

def slot_pairs_points():
    for x in (-width/2, width/2):
        for y in range(-height//2 + 600, height//2, 600):
            yield x, y

face.push(slot_pairs_points())
face.face(details.slot_pair(), mode='s')

def top_and_bottom_bowtie_points():
    for x in (-194.9, 0, 194.9):
        for y in (-height/2, height/2):
            yield x, y

face.push(top_and_bottom_bowtie_points())
face.face(details.bowtie(), mode='s')

def corner_points():
    for x in (-width/2, width/2):
        for y in (-height/2, height/2):
            yield x, y

face.push(corner_points()).face(details.corner(), mode='s').reset()

def middle_hole_points():
    for y in range(-height//2 + 600, height//2, 600):
        yield 0, y


face.push(middle_hole_points()).face(details.middle_hole(), mode='s').reset()

p = cq.Workplane("XY").placeSketch(face).extrude(18)
#cq.exporters.export(p, "SKYLARK250_WALL-M-face.step", opt={"write_pcurves": False})
#cq.exporters.export(cq.Workplane("XY").add(face.faces().val()), "SKYLARK250_WALL-M-face.dxf")
show(p, reset_camera=Camera.KEEP)

# 5_ANYTOOL_HALF_MILL_9MM_IN green
# 3_ANYTOOL_CUTTHROUGH_INSID cyan
# 4_ANYTOOL_CUTTHROUGH_OUTSI blue

# %%
