"""
Copyright 2020 Renze Nicolai

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import sys, struct, binascii, hashlib

def generatePartitionTableEntry(data):
    entry = {
        "type": 0,
        "name": "",
        "device": 0,
        "address0": 0,
        "size0": 0,
        "address1": 0,
        "size1": 0,
        "len": 0,
        "age": 0,
        "activeIndex": 0
    }
    for key in data:
        if not key in entry:
            print("Error: found unknown entry parameter {}!".format(key))
            exit(1)
        if type(entry[key]) == int:
            if data[key].startswith("0x"):
                # Heximal notation
                data[key] = data[key][2:]
                if len(data[key]) & 1 == 1:
                    data[key] = "0" + data[key]
                parts = binascii.unhexlify(data[key])
                entry[key] = 0
                for i in range(len(parts)):
                    entry[key] += parts[len(parts) - i - 1] << (i * 8)
            else:
                # Decimal notation
                entry[key] = int(data[key])
        elif type(entry[key]) == str:
            entry[key] = data[key].encode("ascii")
    
    data = struct.pack("<BBB9sLLLLLL", entry["type"], entry["device"], entry["activeIndex"], entry["name"], entry["address0"], entry["address1"], entry["size0"], entry["size1"], entry["len"], entry["age"])
    return data

def generatePartitionTableHeader(entryCnt, version = 0, age = 0):
    data = b"BFPT" + struct.pack("<HHL", version, entryCnt, age)
    data += struct.pack("<L", binascii.crc32(data, 0))
    return data

def convertPartitionToml(data):
    lines = data.splitlines()
    data = []
    for i in range(len(lines)):
        if (not lines[i].startswith("#")) and (len(lines[i]) > 0):
            data.append(lines[i])
    
    if data.pop(0) != "[pt_table]":
        print("Error: the input file has to be a partition table description!")
        exit(1)
    
    tableParams = {}
    while not data[0].startswith("["):
        fields = data.pop(0).split("=")
        for i in range(len(fields)):
            fields[i] = fields[i].strip()
        if len(fields) != 2:
            print("Error: found a field without a value!")
            exit(1)
        tableParams[fields[0]] = fields[1]
    
    tableEntries = []
    currentEntry = None
    for line in range(len(data)):
        if data[line].startswith("["):
            if data[line] != "[[pt_entry]]":
                print("Error: found unknown section \"{}\"!".format(data[line]))
                exit(1)
            if currentEntry:
                tableEntries.append(currentEntry)
            currentEntry = {}
        else:
            fields = data[line].split("=")
            for i in range(len(fields)):
                fields[i] = fields[i].strip()
            if len(fields) != 2:
                print("Error: found a field without a value!")
                exit(1)
            currentEntry[fields[0]] = fields[1].strip("\"")
    if currentEntry:
        tableEntries.append(currentEntry)
    return (tableParams, tableEntries)

def main():
    if len(sys.argv) < 3:
        print("Usage {} <inputfile> <outputfile>".format(sys.argv[0], sys.argv[1]))
        exit(1)
    
    with open(sys.argv[1], 'r') as f:
        data = f.read()
    (tableParams, tableEntries) = convertPartitionToml(data)
    
    if "address0" in tableParams:
        print("Notice: Expected position in flash for first entry is {}".format(tableParams["address0"]))
    
    if "address1" in tableParams:
        print("Notice: Expected position in flash for secondary entry is {}".format(tableParams["address1"]))
    
    print("Partition table contains {} entries.".format(len(tableEntries)))
    
    header = generatePartitionTableHeader(len(tableEntries))
    entries = bytes([])
    for i in range(len(tableEntries)):
        entries += generatePartitionTableEntry(tableEntries[i])
    output = header + entries + struct.pack("<L", binascii.crc32(entries, 0))
    
    with open(sys.argv[2], 'wb') as f:
        f.write(output)

if __name__ == "__main__":
    main()
