import pathlib

import cadquery as cq
from cadquery.occ_impl.exporters import dxf

from cadquery_skylark import details


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


def make_part(x_len, y_len) -> cq.Workplane:
    outline_s = outside(x_len, y_len)
    p = cq.Workplane("XY").placeSketch(outline_s).extrude(18)
    return p.clean()


def make_cnc(x_len, y_len, dirpath):
    blue = outside(x_len, y_len).wires().offset(-0.25, mode="i").reset().clean()
    blue_w = cq.Workplane("XY").add(blue.faces().vals())

    doc = dxf.DxfDocument()
    doc.add_layer("4_ANYTOOL_CUTTHROUGH_OUTSI", color=5)
    doc.add_shape(blue_w, "4_ANYTOOL_CUTTHROUGH_OUTSI")
    doc.add_layer("5_ANYTOOL_HALF_MILL_9MM_IN", color=3)
    filepath = pathlib.Path(dirpath) / "SKYLARK250_WALL-M-B.dxf"
    doc.document.saveas(filepath)

    return blue_w
