import pathlib

import cadquery as cq

from cadquery_skylark import common, wall_a, wall_b, wall_c, wall_d

HEIGHTS = {
    "XXS": 1500,
    "XS": 1800,
    "S": 2100,
    "M": 2400,
    "L": 2700,
    "XL": 3000,
}

EXPORT_DIR = pathlib.Path(__file__).parent.parent / "exports"


def export_all():
    E = EXPORT_DIR
    for k, height in HEIGHTS.items():
        name = f"SKYLARK250_WALL-{k}"
        print(name, "...")
        P = E / name
        P.mkdir(parents=True, exist_ok=True)
        save_cnc(wall_a.make_cnc(height), P / f"{name}-A.dxf")
        save_cnc(wall_b.make_cnc(), P / f"{name}-B.dxf")
        save_cnc(wall_c.make_cnc(height), P / f"{name}-C.dxf")
        save_cnc(wall_d.make_cnc(height), P / f"{name}-D.dxf")

        save_part(wall_a.make_part(height), P / f"{name}-A")
        save_part(wall_b.make_part(), P / f"{name}-B")
        save_part(wall_c.make_part(height), P / f"{name}-C")
        save_part(wall_d.make_part(height), P / f"{name}-D")


def save_cnc(layers, filepath):
    doc = common.to_dxf(layers)
    doc.document.saveas(filepath)


def save_part(part: cq.Solid, filepath: pathlib.Path):
    assy = cq.Assembly(name=filepath.stem)
    assy.add(part)
    opt = {"write_pcurves": False}
    assy.save(str(filepath.with_suffix(".step")), opt=opt)
    assy.save(str(filepath.with_suffix(".glb")))


export_all()
