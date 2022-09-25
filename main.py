import os
import struct
from codecs import decode

filename = "./data/C001-f.pot"


def get_file_datapoint_list(file_path):
    with open(filename, "rb") as f:

        file_list = []
        datapoint_nbr = 0
        while True:
            datapoint_nbr += 1
            datapoint = dict()
            packed_length = f.read(2)
            if packed_length == b'':
                break

            length = struct.unpack("<H", packed_length)[0]
            packed_dword_label = f.read(4)
            meaningful_bytes = packed_dword_label[:-2]

            reversed_bytes = meaningful_bytes[-1:] + meaningful_bytes[0:1]

            gbk_decoded = reversed_bytes.decode('gbk')

            datapoint['char'] = gbk_decoded

            # print(datapoint['char'])

            stroke_number_packed = f.read(2)
            stroke_number = struct.unpack("<H", stroke_number_packed)[0]

            datapoint["stroke_nbr"] = stroke_number

            stroke_coordinates = dict()

            y = None
            # for i in range(1,stroke_number+1):

            count = 0
            while y != -1:

                coordinates_list = []
                x = None
                count += 1
                while x != -1:

                    x_packed = f.read(2)
                    x = struct.unpack("<h", x_packed)[0]

                    y_packed = f.read(2)
                    y = struct.unpack("<h", y_packed)[0]

                    if x != -1:
                        coordinates_list.append([x, y])
                        stroke_coordinates[count] = coordinates_list

            if len(stroke_coordinates) != stroke_number:
                print("Stroke number mismatch!")

            datapoint["stroke_coord"] = stroke_coordinates

            file_list.append(datapoint)

    return file_list


test = get_file_datapoint_list(filename)

# import json
#
# with open(os.path.join('name.json'), 'w') as fp:
#     json.dump(test, fp)
# fp.close()

import glob
from matplotlib import pyplot as plt

file_dir = os.path.join("data", "competition_POT", '*')
all_files = glob.glob(file_dir)

example = test[0]
example_coordinates = example["stroke_coord"]

print(example['char'])
for i, coords in example_coordinates.items():

    X,Y = zip(*coords)

    X = list(X)
    y_max = max(Y)
    y_min = min(Y)
    Y = [(y_max-y_min)/2 - y for y in Y]

    plt.plot(X,Y, '-')
plt.show()
