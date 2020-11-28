"""
Copyright 2020 Renze Nicolai

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import serial, time

commands = {
    'get_boot_info':    {'id': 0x10, 'length': 0x0000},
    'load_boot_header': {'id': 0x11, 'length': 0x00b0},
    'load_public_key':  {'id': 0x12, 'length': 0x0044},
    'load_public_key2': {'id': 0x13, 'length': 0x0044},
    'load_signature':   {'id': 0x14, 'length': 0x0004},
    'load_signature2':  {'id': 0x15, 'length': 0x0004},
    'load_aes_iv':      {'id': 0x16, 'length': 0x0014},
    'load_seg_header':  {'id': 0x17, 'length': 0x0010},
    'load_seg_data':    {'id': 0x18, 'length': 0x0100},
    'check_image':      {'id': 0x19, 'length': 0x0000},
    'run_image':        {'id': 0x1a, 'length': 0x0000},
    'change_rate':      {'id': 0x20, 'length': 0x0008},
    'reset':            {'id': 0x21, 'length': 0x0000},
    'flash_erase':      {'id': 0x30, 'length': 0x0000},
    'flash_write':      {'id': 0x31, 'length': 0x0100},
    'flash_read':       {'id': 0x32, 'length': 0x0100},
    'flash_boot':       {'id': 0x33, 'length': 0x0000},
    'efuse_write':      {'id': 0x40, 'length': 0x0080},
    'efuse_read':       {'id': 0x41, 'length': 0x0000},
}

try:
    import serial.tools.list_ports as list_ports
except ImportError:
    print("The installed version (%s) of pyserial appears to be too old (Python interpreter %s). " % (sys.VERSION, sys.executable))
    raise

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

def executeCommand(cmd, params=bytes([]), length=None):
    if cmd in commands:
        cmd = commands[cmd]
        if length == None:
            length = cmd['length']
        if not len(params) == length:
            print("Error, wrong parameter length!", len(params), length)
            return None
        port.write(bytes([cmd['id'], 1, length & 0xFF, length >> 8]))
        if length > 0:
            port.write(params)
        time.sleep(0.1)
        if port.inWaiting() >= 2:
            answer = port.read(2)
            if answer[0] == ord('O') and answer[1] == ord('K'):
                answer = port.read(8096)
                return answer
            elif answer[0] == ord('F') and answer[1] == ord('L'):
                error = port.read(8096)
                print("Error response! ", error)
                exit(1)
            return None
    return None

ser_list = sorted(ports.device for ports in list_ports.comports())
port = openPort(str(ser_list[-1:][0]))

if not sync(port):
    print("Not synced! Please reset target and try again.")
    exit(0)

result = executeCommand('get_boot_info')
lengthField = result[0] + (result[1] << 8)
result = result[2:]
if lengthField != len(result):
    print("Length does not match", lengthField, len(result))
    exit(1)

bootromVersion = result[:4]
bootromVersion = bootromVersion[0] + (bootromVersion[1] << 8) + (bootromVersion[2] << 16) + (bootromVersion[3] << 24)
result = result[4:]
print("Bootrom version: {:d}".format(bootromVersion))

otpInfo = result[:16]
result = result[16:]
print("OTP info: ", otpInfo)

with open('eflash_loader_rc32m.bin', 'rb') as loaderFile:
    loaderBinary = loaderFile.read()

bootHeader = loaderBinary[:176]
loaderBinary = loaderBinary[176:]

print("Sending boot header...")

result = executeCommand('load_boot_header', bytes(bootHeader))

segHeader = loaderBinary[:16]
loaderBinary = loaderBinary[16:]

print("Sending segment header...")

result = executeCommand('load_seg_header', bytes(segHeader))

print("Writing application to RAM...")

while len(loaderBinary) > 0:
    length = 4092
    if len(loaderBinary) < length:
        length = len(loaderBinary)
    result = executeCommand('load_seg_data', bytes(loaderBinary[:length]), length)
    loaderBinary = loaderBinary[length:]
    print(".", end="", flush=True)
    
print(" Done!")

print ("Checking...")
_ = executeCommand('check_image')

print("Jumping...")
_ = executeCommand('run_image')
