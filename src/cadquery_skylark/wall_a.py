import cadquery as cq

from . import details


mm = int


def _bowtie_pair_points(width: mm, height: mm):
    for x in (-width / 2, width / 2):
        for y in range(-height // 2 + 300, height // 2, 600):
            yield x, y


def _slot_pairs_points(width: mm, height: mm):
    for x in (-width / 2, width / 2):
        for y in range(-height // 2 + 600, height // 2, 600):
            yield x, y


def _top_and_bottom_bowtie_points(height: mm):
    for x in (-194.9, 0, 194.9):
        for y in (-height / 2, height / 2):
            yield x, y


def _corner_points(width: mm, height: mm, dx: mm = 0, dy: mm = 0):
    for x in (-(width / 2 - dx), width / 2 - dx):
        for y in (-(height / 2 - dy), height / 2 - dy):
            yield x, y


def outside(width: mm, height: mm) -> cq.Sketch:
    sketch = cq.Sketch().rect(width, height)

    sketch.push(_bowtie_pair_points(width, height))
    sketch.face(details.bowtie_pair(), mode="s")

    sketch.push(_slot_pairs_points(width, height))
    sketch.face(details.slot_pair(), mode="s")

    sketch.push(_top_and_bottom_bowtie_points(height))
    sketch.face(details.bowtie(), mode="s")

    sketch.push(_corner_points(width, height)).face(details.corner(), mode="s").reset()

    return sketch


def _middle_hole_points(height: mm):
    for y in range(-height // 2 + 600, height // 2, 600):
        yield 0, y


def inside(height: mm) -> cq.Sketch:
    sketch = cq.Sketch()
    sketch.push(_middle_hole_points(height)).face(details.middle_hole()).reset()
    return sketch


def half_depth(width: mm, height: mm) -> cq.Sketch:
    half = cq.Sketch()
    half.push(_bowtie_pair_points(width, height)).face(details.bowtie_handle_pair()).reset()
    half.push(_top_and_bottom_bowtie_points(height)).face(details.bowtie_handle()).reset()
    half.rect(width, height, mode="i")

    slot_trim = cq.Sketch()
    slot_trim.push(_slot_pairs_points(width, height)).rect(18 * 2, 62).reset()
    slot_trim.rect(width, height, mode="i")
    slot_trim.vertices().fillet(6).reset()

    corner_trim = cq.Sketch()
    corner_trim.push(_corner_points(width, height, dy=52.5)).rect(18 * 2, 37).reset()
    corner_trim.rect(width, height, mode="i")
    corner_trim.vertices().fillet(6).reset()

    half.face(slot_trim).face(corner_trim)

    return half


def make_part(width: mm, height: mm) -> cq.Workplane:
    outside_s = outside(width, height)
    inside_s = inside(height)
    half_s = half_depth(width, height)

    p = cq.Workplane("XY").placeSketch(outside_s).extrude(18)
    p = p.faces(">Z").placeSketch(inside_s).cutThruAll()
    p = p.faces(">Z").placeSketch(half_s).cutBlind(-18 / 2)

    return p
