import io
import csv
import re
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
        super(LightRegion, self).__init__(name, "./img/light/", x, y)


class ShadeRegion(EnumeratedRegion):
    def __init__(self, name: str, x: float, y: float):
        super(ShadeRegion, self).__init__(name, "./img/shade/", x, y)


class ToxicRegion(EnumeratedRegion):
    def __init__(self, name: str, x: float, y: float):
        super(ToxicRegion, self).__init__(name, "./img/toxic/", x, y)


class SprayRegion(EnumeratedRegion):
    def __init__(self, name: str, x: float, y: float):
        super(SprayRegion, self).__init__(name, "./img/spray/", x, y)


class WaterRegion(EnumeratedRegion):
    def __init__(self, days: str, x: float, y: float):
        day_values = re.split(' - |-|, | |,|\n', days)
        if len(day_values) == 1:
            self.days = range(int(day_values[0]))
        else:
            self.days = range(int(day_values[0]), int(day_values[1]))

        if self.days.stop <= 7:
            super(WaterRegion, self).__init__("level3", "./img/water/", x, y)
        elif self.days.stop <= 14:
            super(WaterRegion, self).__init__("level2", "./img/water/", x, y)
        else:
            super(WaterRegion, self).__init__("level1", "./img/water/", x, y)

    def get_svg(self):
        svg = super().get_svg()
        if self.days.start != 0:
            txt_range = str(self.days.start) + "-" + str(self.days.stop)
        else:
            txt_range = str(self.days.stop)

        # txt = svglib.String(5 * mm, 9.1 * mm, txt_range, fontSize=15)
        txt = svglib.String(1 * mm, 15 * mm, txt_range, fontSize=15)
        svg.add(txt)
        return svg


class FertilizerRegion(EnumeratedRegion):
    def __init__(self, days: range, x: float, y: float):
        day_values = re.split(' - |-|, | |,|\n', days)
        if len(day_values) == 1:
            self.days = range(int(day_values[0]))
        else:
            self.days = range(int(day_values[0]), int(day_values[1]))

        if self.days.stop <= 7:
            super(FertilizerRegion, self).__init__("level3", "./img/fertilizer/", x, y)
        elif self.days.stop <= 14:
            super(FertilizerRegion, self).__init__("level2", "./img/fertilizer/", x, y)
        else:
            super(FertilizerRegion, self).__init__("level1", "./img/fertilizer/", x, y)

    def get_svg(self):
        svg = super().get_svg()
        if self.days.start != 0:
            txt_range = str(self.days.start) + "-" + str(self.days.stop)
        else:
            txt_range = str(self.days.stop)

        txt = svglib.String(5 * mm, 9.1 * mm, txt_range, fontSize=15, textAnchor='end')
        svg.add(txt)
        return svg


class TemperaturRegion(EnumeratedRegion):
    def __init__(self, name: str, x: float, y: float):
        super(TemperaturRegion, self).__init__(name, "./img/temperature/", x, y)


class HumidityRegion(EnumeratedRegion):
    def __init__(self, name: str, x: float, y: float):
        super(HumidityRegion, self).__init__(name, "./img/humidity/", x, y)


class PhRegion(Region):
    def __init__(self, ph: str, x: float, y: float):
        super(PhRegion, self).__init__("./img/ph/ph.svg", x, y)
        self.ph = ph.replace(' ', '')

    def get_svg(self):
        svg = super().get_svg()
        self.add_ph(svg)
        self.add_arrow(svg, self.get_ph_position())
        return svg

    def add_arrow(self, svg, value: float):
        arrow = svglib.svg2rlg("./img/ph/arrow.svg")
        arrow.translate(0 * mm, value * 10.5 * mm)
        svg.add(arrow)

    def add_ph(self, svg):
        if any(i.isdigit() for i in self.ph):
            txt = svglib.String(5 * mm, 15 * mm, self.ph, fontSize=13, textAnchor='middle')
            svg.add(txt)
        return svg

    def get_ph_average(self):
        if any(i.isdigit() for i in self.ph):
            phs = re.split(' - |-|, | |,|\n', self.ph)
            avg = 0.0
            for ph in phs:
                avg += float(ph)
            avg = avg / len(phs)
            return avg
        else:
            if "alka" in self.ph and "neut" in self.ph:
                return 7.6
            elif "acid" in self.ph and "neut" in self.ph:
                return 6.3
            elif "acid" in self.ph:
                return 5.9
            elif "neut" in self.ph:
                return 7.0
            elif "alka" in self.ph:
                return 8.1
            else:
                return -0.25

    def get_ph_position(self):
        ph: float = self.get_ph_average()
        if ph < 6.0:
            return 1.00 # acidic
        elif ph <= 6.5:
            return 0.75 # slightly acidic
        elif ph <= 7.3:
            return 0.50 # neutral
        elif ph <= 7.8:
            return 0.25 # slightly alkaline
        else:
            return 0.0 # alkaline


class Labeler:
    def __init__(self, name: str, light: str, shade: str, spray: str, water: range, fertilizer: range, toxic: str, temperature: str, humidity: str, ph: str):
        self.regions = []
        self.name = name
        self.regions.append(LightRegion(light, 0, 20))
        self.regions.append(WaterRegion(water, 20, 20))
        self.regions.append(TemperaturRegion(temperature, 38, 20))
        self.regions.append(HumidityRegion(humidity, 52, 20))
        self.regions.append(PhRegion(ph, 65, 20))
        self.regions.append(ShadeRegion(shade, 0, 0))
        self.regions.append(SprayRegion(spray, 20, 0))
        self.regions.append(FertilizerRegion(fertilizer, 40, 0))
        self.regions.append(ToxicRegion(toxic, 60, 0))

    def build(self):
        filename = "labels/" + self.name.replace(" ", "_") + ".svg"
        print("building " + filename + "...")

        d = Drawing(80 * mm, 47 * mm)

        for r in self.regions:
            print("adding " + r.get_file_name() + " at (" + str(r.get_x()) + ", " + str(r.get_y()) + ")")
            svg = r.get_svg()
            svg.translate(r.get_x() * mm, r.get_y() * mm)
            d.add(svg)

        txt = svglib.String(1 * mm, 42 * mm, self.name, fontSize=15)
        d.add(txt)

        s = io.StringIO()
        c = SVGCanvas((d.width, d.height))
        draw(d, c, 0, 0)
        c.save(s)
        s.flush()
        with open(filename, mode='w') as f:
            f.write(s.getvalue())


if __name__ == '__main__':
    labels = []
    with open('flowers.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            labels.append(Labeler(name=row['name'],
                                  light=row['light'],
                                  shade=row['shade'],
                                  spray=row['spray'],
                                  water=row['water'],
                                  fertilizer=row['fertilizer'],
                                  toxic=row['toxic'],
                                  temperature=row['temperature'],
                                  humidity=row['humidity'],
                                  ph=row['ph']))

    i = 0
    for label in labels:
        i = i+1
        label.build()
