import cadquery as cq


def bowtie() -> cq.Sketch:
    w = cq.Workplane("XY")
    w = (
        w.moveTo(0, 56)
        .hLine(78 / 2)
        .radiusArc((78 / 2 + 6, 56 - 6), 6)
        .lineTo(55 / 2, 0)
    )
    w = w.mirrorX().mirrorY()
    s = cq.Sketch().face(w.wires().val())
    to_fillet = cq.selectors.SumSelector(
        cq.NearestToPointSelector((25, 0)), cq.NearestToPointSelector((-25, 0))
    )
    s = s.vertices(to_fillet).fillet(6).reset()
    return s


def t_slot(length, width=24 * 2) -> cq.Wire:
    s = cq.Workplane("XY")
    s = s.moveTo(0, length / 2).hLine(width / 2).vLine(-12).hLine(-6).vLineTo(0)
    s = s.mirrorX().mirrorY()
    return s.wires().val()


def m_slot() -> cq.Wire:
    length = 62
    s = cq.Workplane("XY")
    s = s.vLine(length / 2).hLine(12).vLine(-6).hLine(12).vLine(-12).hLine(-6).vLineTo(0)
    s = s.mirrorX()
    return s.wires().val()


def bowtie_pair() -> cq.Sketch:
    s = cq.Sketch()
    b = bowtie()
    s.face(t_slot(75))
    s.push(((0, 104.5), (0, -104.0))).face(b, angle=90).reset()
    return s


def slot_pair() -> cq.Sketch:
    s = cq.Sketch()
    s.push([(0, -62.5), (0, 62.5)]).face(t_slot(75)).reset()
    return s


def round_cutouts() -> cq.Sketch:
    s = cq.Sketch()
    s.circle(12)
    s.push([(0, -10)]).rect(36, 20).clean().reset()
    s.edges("%CIRCLE").vertices().fillet(6).reset()
    s.push([(0, -10)]).rect(36, 20, mode="s").reset()
    f = s.wires().val()
    s.push([(0, 0)]).face(f, angle=180).reset()
    return s.clean()


def corner() -> cq.Sketch:
    s = cq.Sketch()
    s.push([(0, 0)]).face(t_slot(80)).reset()
    s.push([(0, -82.5), (0, 82.5)]).face(t_slot(35)).reset()
    s.push([(-47.6, 0), (47.6, 0)]).face(round_cutouts()).reset()
    return s


def middle_hole() -> cq.Sketch:
    s = cq.Sketch()
    s.face(t_slot(120, 30), angle=90)
    s.push([(0, -100), (0, 100)]).slot(100 + 2 * 9, 18).reset()
    return s


def bowtie_handle():
    w = cq.Workplane("XY")
    w = w.moveTo(-21, 50).vLine(6).radiusArc((21, 56), 21).vLine(-6).close()
    wire = w.wires().val()
    s = cq.Sketch()
    s.face(wire)
    s.face(wire, angle=180)
    return s


def bowtie_handle_pair():
    s = cq.Sketch()
    bth = bowtie_handle()
    s.push(((0, 104.5), (0, -104.0))).face(bth, angle=90).reset()
    return s
