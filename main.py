import svg_stack as ss


class Region(object):
    def __init__(self, file: str, x=float, y=float):
        self.file = file
        self.x = x
        self.y = y

    def getImage(self):
        return self.file

    def getX(self):
        return self.x

    def getY(self):
        return self.y


class EnumeratedRegion(Region):
    def __init__(self, enumtype: str, prefix: str, x=float, y=float):
        self.enumtype = enumtype + ".svg"
        self.prefix = prefix
        super(EnumeratedRegion, self).__init__(self.prefix + self.enumtype, x, y)


class LightRegion(EnumeratedRegion):
    def __init__(self, name: str, x=float, y=float):
        super(LightRegion, self).__init__(name, "./light/", x, y)


class ToxicRegion(EnumeratedRegion):
    def __init__(self, name: str, x=float, y=float):
        super(ToxicRegion, self).__init__(name, "./toxic/", x, y)


class Labeler:
    def __init__(self, light: str, toxic: str):
        self.regions = []
        self.regions.append(LightRegion(light))
        self.regions.append(ToxicRegion(toxic))
        self.doc = ss.Document()

    def appendRegion(self, r: Region):
        print(r.getImage())

    def build(self):
        print("building...")
        layout1 = ss.HBoxLayout()
        for r in self.regions:
            layout1.addSVG(r.getImage())

        ss.
        self.doc.setLayout(layout1)
        self.doc.save("label.svg")

if __name__ == '__main__':
    labeler = Labeler(light="bright", toxic="low")
    labeler.build()
