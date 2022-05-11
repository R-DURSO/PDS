from math import cos, sin, pi
import numpy as np

class Segment:
    def __init__(self, length, angle, start=None):
        self.length = length
        self.absoluteAngle = angle
        self.angle = angle
        self.start = start
        if start != None:
            self.end = self.calculateEnd()

    def calculateEnd(self):
        return (self.start[0] + self.length * cos(self.angle), self.start[1] + self.length * sin(self.angle))

    def update(self, parent):
        self.angle = self.absoluteAngle + parent.angle
        self.start = parent.end
        self.end = self.calculateEnd()

    def print(self):
        print(f"Length: {self.length}, angle: {self.angle}, start: {self.start}, end: {self.end}.")

    def param(self):
        return self.start, self.end, self.length, self.absoluteAngle


class Braccio:
    def __init__(self):
        # Rotation base 0-180
        self.base = 0
        self.segments = {
            "shoulder": Segment(10, pi/2, (0, 0)),
            "elbow": Segment(10, 0),
            "wrist": Segment(10, 0)
        }
        self.update()

    def update(self):
        parent = None
        for name, seg in self.segments.items():
            if parent != None:
                seg.update(parent)
            parent = seg

    def rotate(self, segment, angle):
        self.segments[segment].absoluteAngle = angle
        self.update()

    def estimation(self):
        print(f"End effector: {self.segments['wrist'].end}.")

braccio = Braccio()
braccio.estimation()
for name, seg in braccio.segments.items():
    seg.print()


def fk():
    starts, bs, ls, ts = braccio.segments["shoulder"].param()
    ae, be, le, te  = braccio.segments["elbow"].param()
    aw, bw, lw, tw = braccio.segments["wrist"].param()

    return (starts[0] + ls*cos(ts) + le*cos(te+ts) + lw*cos(tw+te+ts), starts[1] + ls*sin(ts) + le*sin(te+ts) + lw*sin(tw+te+ts))

def fk2(ts, te, tw):
    starts, bs, ls, _ = braccio.segments["shoulder"].param()
    ae, be, le, _  = braccio.segments["elbow"].param()
    aw, bw, lw, _ = braccio.segments["wrist"].param()

    return (starts[0] + ls*cos(ts) + le*cos(te+ts) + lw*cos(tw+te+ts), starts[1] + ls*sin(ts) + le*sin(te+ts) + lw*sin(tw+te+ts))

print(f"FK: {fk2(0, 0, 0)}.")


def ik(x, y):
    i = 0
    eps = (1, 1)
    d = np.array([[x], [y]])
    #t = np.array([[1.57], [0.78], [0]])
    t = np.array([[1.57], [1.57], [1.57]])

    est = fk2(t[0, 0], t[1, 0], t[2, 0])

    # while (d[0, 0] - est[0])**2 > eps[0] and (d[1, 0] - est[1])**2 > eps[1]:
    for i in range(1000):
        est = fk2(t[0, 0], t[1, 0], t[2, 0])
        e = np.array([[d[0, 0] - est[0]], [d[1, 0] - est[1]]])
        j = np.array([[-np.sin(t[0, 0])*(30), -np.sin(t[1, 0])*(30), -np.sin(t[2, 0])*(30)], [np.cos(t[0, 0])*30, np.cos(t[1, 0])*30, np.cos(t[2, 0])*30]])
        #np.array([[-np.sin(0)*(30), -np.sin(0)*(30), -np.sin(0)*(30)], [np.cos(0)*30, np.cos(0)*30, np.cos(0)*30]])
        inv = np.linalg.pinv(j)
        mult = np.dot(inv, e)
        #print(t)
        #print(mult)
        t = t + mult
        #print(t)
        #print("\n")

        print(f"Theta: {t}, Est: {est}, Erreur: {e}, Iter: {i}\n")

        if np.abs(d[0, 0] - est[0]) < eps[0] and np.abs(d[1, 0] - est[1]) < eps[1]:
            return

print("\n\n\nStart...")
ik(20, 10)
print("Done.")