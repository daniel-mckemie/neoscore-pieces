import numpy as np
import random
import wave
import struct
from neoscore.common import *

# audio setup
sampleRate = 4000.0  # hertz
obj = wave.open('sound902.wav', 'w')
obj.setnchannels(1)  # mono
obj.setsampwidth(2)
obj.setframerate(sampleRate)


# Probability to move up or down
prob = [0.65, 0.35]

# statistically defining the starting position
start = 0
values = [start]
np.random.seed(9104)
random.seed(7219)

# creating the random points
points = np.random.random(999)
down = points < prob[0]
up = points > prob[1]

for idown, iup in zip(down, up):
    down = idown.any() and values[-1] > -32767
    up = iup.any() and values[-1] < 32767
    values.append(values[-1] - down + up)

bipole = []


for i in range(0, len(values) - 1):
    reverse = (values[-i] * - 1)

# CHANGE THESE < and > values!!!!
    if values[i] < 32767 and values[i] > 0:
        # values[i] = abs(values[i]-32767)
        # print(abs(values[i]-32767))
        bipole.append(values[i])
    else:
        bipole.append(values[i])

    if reverse < 1745 and reverse > -3225:
        bipole.append(reverse * random.randint(1, 10))
    else:
        bipole.append(reverse)
        random.shuffle(bipole)

bipole_repeat = []


def repeater(x, y):
    for i in range(x, y):
        bipole_repeat.append(bipole[i])


def repeater2(x, y):
    for i in range(x, y):
        bipole_repeat.append(bipole[-i])


for i in range(20):
    x = np.random.randint(1, 999)
    y = np.random.randint(1, 999)
    repeater(x, y)
    for i in range(5):
        x = np.random.randint(1, 999)
        y = np.random.randint(1, 999)
        repeater2(x, y)


bipole_hammed = np.hamming(len(bipole_repeat))


# Encode waveform
for i in bipole_hammed:
    if (i < 0):
        i = i * -1
    data = struct.pack('<f', i)
    obj.writeframesraw(data)
    # print(randomZero)
obj.close()


# NEOSCORE
neoscore.setup()
center = Mm(50)

# Paths and Pens
pen_1 = Pen("000000", Mm(0.01), PenPattern.SOLID)
pen_2 = Pen("000000", Mm(0.01), PenPattern.SOLID)

path_1_origin = Point(x=Mm(0.0), y=Mm(10.0))
path_2_origin = Point(x=Mm(0.0), y=Mm(100.0))

path_1 = Path(path_1_origin, None, "#000000", pen=pen_1)
path_2 = Path(path_2_origin, path_1, "#000000", pen=pen_2)

# Staves
staff_1_origin = Point(x=Mm(0.0), y=Mm(20.0))
staff_2_origin = Point(x=Mm(0.0), y=Mm(25.0))

staff1 = Staff(staff_1_origin, path_1, Mm(170))
staff2 = Staff(staff_2_origin, path_2, Mm(170))
InstrumentName((staff1.unit(-2), staff1.center_y), staff1, "Violin I", "vln")
InstrumentName((staff2.unit(-2), staff2.center_y), staff2, "Violin II", "vln")

i = 0
while i < len(bipole_hammed):
    # print(bipole_hammed[i])
    # print(random.random())
    if i == 0:
        path_1.line_to(Mm(bipole_hammed[i] * 5), Mm(random.random() * 50))
        path_2.line_to(Mm(bipole_hammed[i]), Mm(random.random() * 50))
    elif i < 9000:
        path_1.line_to(Mm(bipole_hammed[i] * 10), Mm(random.random() * 50))
        path_2.line_to(Mm(bipole_hammed[i] * 50), Mm(random.random() * 50))
    else:
        path_1.line_to(Mm(bipole_hammed[i] * 90), Mm(random.random() * 50))
        path_2.line_to(Mm(bipole_hammed[i] * 120), Mm(random.random() * 50))
    i += 1


# Another iteration
path_3_origin = Point(x=Mm(50.0), y=Mm(10.0))
path_4_origin = Point(x=Mm(30.0), y=Mm(100.0))

path_1 = Path(path_3_origin, None, "#000000", pen=pen_1)
path_2 = Path(path_4_origin, path_1, "#000000", pen=pen_2)

j = 0
sorted(bipole_hammed)
while j < len(bipole_hammed):
    # k = random.randint(0, len(bipole_hammed)-1)
    # print(bipole_hammed[i])
    # print(random.random())
    if j == 0:
        path_1.line_to(Mm(bipole_hammed[j] * 20), Mm(random.random() * 50))
        path_2.line_to(Mm(bipole_hammed[j]) * 10, Mm(random.random() * 50))
    elif i < 9000:
        path_1.line_to(Mm(bipole_hammed[j] * 2), Mm(random.random() * 50))
        path_2.line_to(Mm(bipole_hammed[j] * 32), Mm(random.random() * 50))
    else:
        path_1.line_to(Mm(bipole_hammed[j] * 120), Mm(random.random() * 50))
        path_2.line_to(Mm(bipole_hammed[j] * 90), Mm(random.random() * 50))
    j += 1


neoscore.show()
# neoscore.render_pdf(
#     pdf_path='/Users/danielmckemie/Documents/Code/python/neoscore/neoDemo.pdf', dpi=300)


# for i in range(99999):
#    value = random.randint(-32767, 32767)
#    data = struct.pack('<h', value)
#    obj.writeframesraw( data )
# obj.close()
