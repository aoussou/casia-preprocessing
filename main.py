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

        STOP
        width = struct.unpack("<H", f.read(2))[0]
        height = struct.unpack("<H", f.read(2))[0]
        photo_bytes = struct.unpack("{}B".format(height * width), f.read(height * width))

        # # Comes out as a tuple of chars. Need to be combined. Encoded as gb2312, gotta convert to unicode.
        # label = decode(raw_label[0] + raw_label[1], encoding="gb2312")
        # # Create an array of bytes for the image, match it to the proper dimensions, and turn it into an image.
        # image = fromarray(np.array(photo_bytes, dtype=np.uint8).reshape(height, width))
        #
        # yield image, label

print(len(train_chinese))
# len(test_chinese)

