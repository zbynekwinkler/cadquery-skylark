import pathlib
import cadquery as cq
from cadquery.occ_impl.exporters import dxf

from . import details, wall_a

from .wall_a import outside as outside

mm = int


def inside(height: mm) -> cq.Sketch:
    sketch = cq.Sketch()
    sketch.push(wall_a._middle_hole_points(height))
    sketch.face(details.t_slot(120, 30), angle=90)
    return sketch.reset()


def half_depth(width: mm, height: mm) -> cq.Sketch:
    bowtie_handles = wall_a._bowtie_handles(width, height)
    corner_trim = wall_a._corner_trim(width, height)
    return cq.Sketch().face(bowtie_handles).face(corner_trim)


def make_part(width: mm, height: mm) -> cq.Workplane:
    outside_s = outside(width, height)
    inside_s = inside(height)
    half_s = half_depth(width, height)

    p = cq.Workplane("XY").placeSketch(outside_s).extrude(18)
    p = p.faces(">Z").placeSketch(inside_s).cutThruAll()
    p = p.faces(">Z").placeSketch(half_s).cutBlind(-18 / 2)

    return p


def make_cnc(width: mm, height: mm, dirpath):
    doc = dxf.DxfDocument()
    blue = outside(width, height).wires().offset(-0.25, mode="i").reset().clean()
    cyan = inside(height).wires().offset(0.25, mode="a").reset().clean()
    green = half_depth(width, height).wires().offset(0.25, mode="a").reset().clean()
    blue_w = cq.Workplane("XY").add(blue.faces().vals())
    cyan_w = cq.Workplane("XY").add(cyan.faces().vals())
    green_w = cq.Workplane("XY").add(green.faces().vals())
    doc.add_layer("4_ANYTOOL_CUTTHROUGH_OUTSI", color=5)
    doc.add_shape(blue_w, "4_ANYTOOL_CUTTHROUGH_OUTSI")
    doc.add_layer("3_ANYTOOL_CUTTHROUGH_INSID", color=4)
    doc.add_shape(cyan_w, "3_ANYTOOL_CUTTHROUGH_INSID")
    doc.add_layer("5_ANYTOOL_HALF_MILL_9MM_IN", color=3)
    doc.add_shape(green_w, "5_ANYTOOL_HALF_MILL_9MM_IN")
    filepath = pathlib.Path(dirpath) / "SKYLARK250_WALL-M-D.dxf"
    doc.document.saveas(filepath)
    return blue_w, cyan_w, green_w
