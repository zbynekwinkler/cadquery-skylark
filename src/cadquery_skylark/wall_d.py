import cadquery as cq

from . import details, wall_a, common

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


def make_part(height: mm) -> cq.Solid:
    width = 600
    outside_s = outside(width, height)
    inside_s = inside(height)
    half_s = half_depth(width, height)

    p = cq.Workplane("XY").placeSketch(outside_s).extrude(18)
    p = p.faces(">Z").workplane(centerOption="CenterOfBoundBox")
    p = p.placeSketch(inside_s).cutThruAll()
    p = p.faces(">Z").workplane(centerOption="CenterOfBoundBox")
    p = p.placeSketch(half_s).cutBlind(-18 / 2)

    return common.recenter(p.findSolid())


def make_cnc(height: mm):
    width = 600
    blue = outside(width, height).wires().offset(-0.25, mode="i").reset().clean()
    cyan = inside(height).wires().offset(0.25, mode="a").reset().clean()
    green = half_depth(width, height).wires().offset(0.25, mode="a").reset().clean()
    return blue, cyan, green
