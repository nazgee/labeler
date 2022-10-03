import io
from svglib import svglib
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.renderSVG import SVGCanvas, draw
from reportlab.lib.units import mm


class Region(object):
    def __init__(self, file: str, x: float, y: float):
        self.file = file
        self.x = x
        self.y = y

    def get_file_name(self):
        return self.file

    def get_svg(self):
        return svglib.svg2rlg(self.get_file_name())

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


class EnumeratedRegion(Region):
    def __init__(self, enumtype: str, prefix: str, x: float, y: float):
        self.enumtype = enumtype + ".svg"
        self.prefix = prefix
        super(EnumeratedRegion, self).__init__(self.prefix + self.enumtype, x, y)


class LightRegion(EnumeratedRegion):
    def __init__(self, name: str, x: float, y: float):
        super(LightRegion, self).__init__(name, "./light/", x, y)


class ToxicRegion(EnumeratedRegion):
    def __init__(self, name: str, x: float, y: float):
        super(ToxicRegion, self).__init__(name, "./toxic/", x, y)


class Labeler:
    def __init__(self, light: str, toxic: str):
        self.regions = []
        self.regions.append(LightRegion(light, 0, 0))
        self.regions.append(ToxicRegion(toxic, 20, 0))

    def build(self, filename: str):
        print("building " + filename + "...")

        d = Drawing(80 * mm, 40 * mm)

        for r in self.regions:
            print("adding " + r.get_file_name() + " at (" + str(r.get_x()) + ", " + str(r.get_y()) + ")")
            svg = r.get_svg()
            svg.translate(r.get_x() * mm, r.get_y() * mm)
            d.add(svg)

        s = io.StringIO()
        c = SVGCanvas((d.width, d.height))
        draw(d, c, 0, 0)
        c.save(s)
        s.flush()
        with open(filename, mode='w') as f:
            f.write(s.getvalue())


if __name__ == '__main__':
    labels = [
        Labeler(light="moderate", toxic="no"),
        Labeler(light="bright", toxic="low"),
        Labeler(light="low", toxic="moderate"),
        Labeler(light="low", toxic="high")
    ]

    i = 0
    for label in labels:
        i = i+1
        label.build("label" + str(i) + ".svg")
