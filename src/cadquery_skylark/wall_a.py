import cadquery as cq

from . import details


def _bowtie_pair_points(width, height):
    for x in (-width / 2, width / 2):
        for y in range(-height // 2 + 300, height // 2, 600):
            yield x, y


def _slot_pairs_points(width, height):
    for x in (-width / 2, width / 2):
        for y in range(-height // 2 + 600, height // 2, 600):
            yield x, y


def _top_and_bottom_bowtie_points(height):
    for x in (-194.9, 0, 194.9):
        for y in (-height / 2, height / 2):
            yield x, y


def _corner_points(width, height, dx=0, dy=0):
    for x in (-(width / 2 - dx), width / 2 - dx):
        for y in (-(height / 2 - dy), height / 2 - dy):
            yield x, y


def outside(width, height) -> cq.Sketch:
    sketch = cq.Sketch().rect(width, height)

    sketch.push(_bowtie_pair_points(width, height))
    sketch.face(details.bowtie_pair(), mode="s")

    sketch.push(_slot_pairs_points(width, height))
    sketch.face(details.slot_pair(), mode="s")

    sketch.push(_top_and_bottom_bowtie_points(height))
    sketch.face(details.bowtie(), mode="s")

    sketch.push(_corner_points(width, height)).face(details.corner(), mode="s").reset()

    return sketch
