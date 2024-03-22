import cadquery as cq

from cadquery_skylark import details, common


def outside(x_len, y_len) -> cq.Sketch:
    s = cq.Sketch()
    s.rect(x_len, y_len)

    def corners():
        for x in (-x_len / 2, x_len / 2):
            for y in (-y_len / 2, y_len / 2):
                yield x, y

    s.push(corners())
    s.face(details.t_slot(240 * 2), angle=90, mode="s")
    s.face(details.t_slot(118 * 2), mode="s")
    return s.reset().clean()


def make_part() -> cq.Solid:
    x_len, y_len = 600, 250 + 2 * 18
    outline_s = outside(x_len, y_len)
    p = cq.Workplane("XY").placeSketch(outline_s).extrude(18)
    return common.recenter(p.findSolid())


def make_cnc():
    x_len, y_len = 600, 250 + 2 * 18
    blue = outside(x_len, y_len).wires().offset(-0.25, mode="i").reset().clean()
    blue_w = cq.Workplane("XY").add(blue.faces().vals())
    return (blue_w,)
