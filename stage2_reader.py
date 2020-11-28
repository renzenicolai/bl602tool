"""
Copyright 2020 Renze Nicolai

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import serial, time

commands = {
    'chip_erase':    {'id': 0x3C, 'length': 0x0000},
    'flash_erase':   {'id': 0x30, 'length': 0x0008}, # start-addr (4 bytes), end-addr (4 bytes)
    'flash_program': {'id': 0x31, 'length': 0x0004}, # length = n+4, params: start-addr (4 bytes), payload (n bytes)
    'flash_check':   {'id': 0x3A, 'length': 0x0000},
    'flash_read':    {'id': 0x32, 'length': 0x0008}, # length = n+4, params: start-addr (4 bytes), read-length (4 bytes)
    'sha256_read':   {'id': 0x3D, 'length': 0x0008}, # length = n+4, params: start-addr (4 bytes), read-length (4 bytes)
}

def openPort(device):
    return serial.Serial(device, 115200, timeout=0.1, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=False)

def sync(port):
    # Flush
    while port.inWaiting() > 0:
        _ = port.read()
    # Write initialization sequence
    port.write(bytes([ord('U')]*70))
    time.sleep(0.1)
    # Check response
    if port.inWaiting() == 2:
        answer = port.read(2)
        if answer[0] == ord('O') and answer[1] == ord('K'):
            return True
    return False

def executeCommand(cmd, params=bytes([]), length=None, timeout=1):
    if cmd in commands:
        cmd = commands[cmd]
        if length == None:
            length = cmd['length']
        if not len(params) == length:
            print("Error, wrong parameter length!", len(params), length)
            return None
        chksum = 0
        chksum += length & 0xFF
        chksum += length >> 8
        for i in range(len(params)):
            chksum += params[i]
        chksum = chksum & 0xFF
        port.write(bytes([cmd['id'], chksum, length & 0xFF, length >> 8]))
        if length > 0:
            port.write(params)
        time.sleep(0.1)
        didPrintTimeout = False
        while timeout > 1 and port.inWaiting() < 2:
            time.sleep(0.1)
            timeout -= 1
            if timeout > 0:
                print("#", end="", flush=True)
                didPrintTimeout = True
        if didPrintTimeout:
            print("")
        if port.inWaiting() >= 2:
            answer = port.read(2)
            if answer[0] == ord('O') and answer[1] == ord('K'):
                answer = port.read(8096)
                time.sleep(0.01)
                while port.inWaiting() > 0:
                    print("Receiving more data...")
                    answer += port.read(8096)
                    time.sleep(0.01)
                return answer
            elif answer[0] == ord('F') and answer[1] == ord('L'):
                error = port.read(8096)
                print("Error response! ", error)
                exit(1)
            else:
                print("Bug: unhandled response!")
                print(hex(answer[0]), hex(answer[1]))
            return None
    print("Bug: unknown command!")
    return None

port = openPort('/dev/ttyUSB0')

if not sync(port):
    print("Not synced! Please reset target and try again.")
    exit(0)


print("Reading flash...")

readData = bytes([])
readAmount = 1024 * 256 #256KB
addr = 0
while readAmount > 0:
    length = 512
    if readAmount < length:
        length = readAmount
    print("Reading... Addr = " + str(addr) + ", Length remaining = " + str(readAmount), flush=True)
    result = executeCommand('flash_read', bytes([addr & 0xFF, (addr>>8)&0xFF, (addr>>16)&0xFF, (addr>>24)&0xFF])+bytes([length & 0xFF, (length>>8)&0xFF, (length>>16)&0xFF, (length>>24)&0xFF]), 8, 100)
    if result == None:
        print("No result!")
        exit(1)
    readData += result[2:]
    addr += length
    readAmount -= length

with open("read.bin", "wb") as f:
    f.write(readData)

print("Done!")
