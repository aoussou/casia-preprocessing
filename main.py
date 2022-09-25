import os
import struct
from codecs import decode


filename = "./data/C001-f.pot"
with open(filename, "rb") as f:
    while True:
        packed_length = f.read(2)
        if packed_length == b'':
            break

        length = struct.unpack("<H", packed_length)[0]
        packed_dword_label = f.read(4)
        meaningful_bytes = packed_dword_label[:-2]

        reversed_bytes = meaningful_bytes[-1:] + meaningful_bytes[0:1]
        gbk_decoded = reversed_bytes.decode('gbk')

        stroke_number_packed = f.read(2)
        stroke_number = struct.unpack("<H", stroke_number_packed)[0]

        stroke_coordinates = dict()

        y = None
        # for i in range(1,stroke_number+1):

        count = 0
        while y != -1:

            coordinates_list = []
            x = None
            while x != -1:
                count += 1
                x_packed = f.read(2)
                x = struct.unpack("<h", x_packed)[0]

                y_packed = f.read(2)
                y = struct.unpack("<h", y_packed)[0]

                if x != -1:
                    coordinates_list += (x,y)
                    stroke_coordinates[count] = coordinates_list

        STOP

        next_y_packed = f.read(2)
        next_y = struct.unpack("<h", next_y_packed)[0]
        STOP
        width = struct.unpack("<H", f.read(2))[0]
        height = struct.unpack("<H", f.read(2))[0]
        photo_bytes = struct.unpack("{}B".format(height * width), f.read(height * width))

