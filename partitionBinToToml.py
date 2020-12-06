"""
Copyright 2020 Renze Nicolai

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import sys, struct, binascii, hashlib

def readPartitionEntry(data):
    (partitionType, device, activeIndex, name, address0, address1, maxLen0, maxLen1, length, age) = struct.unpack("<BBB9sLLLLLL", data)
    print("type = {:d}".format(partitionType))
    print("name = \"{}\"".format(name.decode("utf-8")))
    print("device = {:d}".format(device))
    print("address0 = 0x{:x}".format(address0))
    print("size0 = 0x{:x}".format(maxLen0))
    print("address1 = 0x{:x}".format(address1))
    print("size1 = 0x{:x}".format(maxLen1))
    print("len = {:d}".format(length))
    print("#age = {:d}".format(age))
    print("#activeindex = {:d}".format(activeIndex))

def readPartitionTable(data):
    if len(data) < 16:
        print("Input file is too short ({:d} bytes), expected at least 16 bytes".format(len(data)))
        exit(1)
    (magic, version, entryCnt, age, crc32) = struct.unpack("<4sHHLL", data[:16])
    if magic != b"BFPT":
        print("The magic value is wrong ({}), expected BFPT".format(magic))
        exit(1)
    calcCrc32 = binascii.crc32(data[0:12], 0)
    if crc32 != calcCrc32:
        print("The CRC32 checksum of the partition table header does not match", crc32, calcCrc32)
        exit(1)
    print("[pt_table]")
    print("address0 = 0xE000")
    print("address1 = 0xF000")
    print("#version = {:d}".format(version))
    print("#age =  {:d}".format(age))
    print()
    for i in range(entryCnt):
        print("[[pt_entry]]")
        readPartitionEntry(data[16+36*i:16+36*(i+1)])
        print()


def main():
    if len(sys.argv) < 2:
        print("Usage {} <inputfile> [sector]".format(sys.argv[0]))
        exit(1)
    with open(sys.argv[1], 'rb') as f:
        data = f.read()
    sector = 0
    if len(sys.argv) > 2:
        sector = int(sys.argv[2])
    readPartitionTable(data[4096*sector:4096*(sector+1)])

if __name__ == "__main__":
    main()
