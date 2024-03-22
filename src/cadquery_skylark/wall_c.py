import cadquery as cq

from . import details, common

mm = int


def _slot_pairs_points(x: mm, height: mm):
    for y in range(-height // 2 + 300, height // 2, 600):
        yield x, y


def _slot_pair() -> cq.Sketch:
    s = cq.Sketch()
    s.push([(0, -118.75), (0, 118.75)]).face(details.t_slot(162.5)).reset()
    return s


def _slot_pair_service() -> cq.Sketch:
    s = cq.Sketch()
    s.rect(32 * 2, 75)
    s.push([(0, -118.75), (0, 118.75)]).face(details.t_slot(162.5, 56 * 2)).reset()
    return s


def _top_and_bottom_slot_point(width: mm, height: mm):
    for x in (width / 2 - 89, width / 2 - 89 - 120):
        for y in (-height / 2, height / 2):
            yield x, y


def outside(width, height) -> cq.Sketch:
    s = cq.Sketch().rect(width, height)
    s.push(_slot_pairs_points(width / 2, height)).face(_slot_pair(), mode="s")
    s.push(_slot_pairs_points(-width / 2, height)).face(_slot_pair_service(), mode="s")

    rest = height % 600
    if rest > 200:
        s.push([(width / 2, height // 2 - rest / 2)]).face(details.t_slot(100), mode="s")
        s.push([(-width / 2, height // 2 - rest / 2)]).face(details.t_slot(100, 56 * 2), mode="s")

    s.push(_top_and_bottom_slot_point(width, height)).face(details.t_slot(60), angle=90, mode="s")
    return s.reset()


def inside(width: mm, height: mm) -> cq.Sketch:
    def points(xx):
        for yy in range(-height // 2 + 600, height // 2, 600):
            yield xx, yy

    s = cq.Sketch()

    x = width / 2 - 9 * 1.5
    y = height / 2 - (40 + 25 / 2)
    s.push([(x, -y), (x, y)]).slot(25, 9, angle=90).reset()
    s.push(points(x)).slot(50, 9, angle=90).reset()

    x = width / 2 - 18 - 250 - 9 / 2
    s.push([(x, -y), (x, y)]).slot(25, 9, angle=90).reset()
    x = width / 2 - 18 - 250 - 18
    s.push(points(x)).face(details.m_slot()).reset()
    s.push(points(width / 2 - 250 / 2 - 18)).face(details.t_slot(50, 30), angle=90).reset()
    return s.reset()


def make_part(height: mm) -> cq.Solid:
    width = 318
    outside_s = outside(width, height)
    inside_s = inside(width, height)
    p = cq.Workplane("XY").placeSketch(outside_s).extrude(18)
    p = p.faces(">Z").workplane(centerOption="CenterOfBoundBox")
    p = p.placeSketch(inside_s).cutThruAll()
    return common.recenter(p.findSolid())


def make_cnc(height: mm):
    width = 318
    blue = outside(width, height).wires().offset(-0.25, mode="i").reset().clean()
    cyan = inside(width, height).wires().offset(0.25, mode="a").reset().clean()
    return blue, cyan
