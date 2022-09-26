import os
import struct
import glob
from matplotlib import pyplot as plt


###############################################################################
def create_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)


###############################################################################
def get_file_datapoint_list(file_path):
    with open(file_path, "rb") as f:

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


# root_dir = "./data/competition_POT"
# filename = "C001-f.pot"

# file_path = os.path.join(root_dir, filename)


file_dir = os.path.join("data", "competition_POT", '*')
all_files = sorted(glob.glob(file_dir))

for file in all_files:

    individual_id = os.path.splitext(file)[0]
    save_dir = os.path.join('data', 'plots', individual_id)

    print(file)

    file_info = get_file_datapoint_list(file)

    for dtpt_nbr, datapoint_info in enumerate(file_info):

        example_coordinates = datapoint_info["stroke_coord"]

        char = datapoint_info['char']
        # print(char)
        for i, coords in example_coordinates.items():
            X, Y = zip(*coords)
            X = list(X)
            y_max = (max(Y))
            Y = [-y for y in Y]
            plt.plot(X, Y, '-k')

        plt.axis('off')


        create_dir(save_dir)
        try:
            save_path = os.path.join(save_dir, char + '.jpg')
            plt.savefig(save_path)
        except:
            print("couldn't process", save_path)
