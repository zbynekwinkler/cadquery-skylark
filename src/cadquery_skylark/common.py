import cadquery as cq
from cadquery.occ_impl.exporters import dxf


def to_dxf(layers: tuple[cq.Sketch, ...]) -> dxf.DxfDocument:
    doc = dxf.DxfDocument()
    layers = layers + (cq.Sketch(),) * (3 - len(layers))
    blue, cyan, green = layers
    blue_w = cq.Workplane("XY").add(blue.faces().vals())
    cyan_w = cq.Workplane("XY").add(cyan.faces().vals())
    green_w = cq.Workplane("XY").add(green.faces().vals())
    doc.add_layer("4_ANYTOOL_CUTTHROUGH_OUTSI", color=5)
    doc.add_shape(blue_w, "4_ANYTOOL_CUTTHROUGH_OUTSI")
    doc.add_layer("3_ANYTOOL_CUTTHROUGH_INSID", color=4)
    doc.add_shape(cyan_w, "3_ANYTOOL_CUTTHROUGH_INSID")
    doc.add_layer("5_ANYTOOL_HALF_MILL_9MM_IN", color=3)
    doc.add_shape(green_w, "5_ANYTOOL_HALF_MILL_9MM_IN")
    return doc
