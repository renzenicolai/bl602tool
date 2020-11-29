"""
Copyright 2020 Renze Nicolai

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import serial, time, argparse
import serial.tools.list_ports as list_ports

def openPort(device, baudrate=115200):
    return serial.Serial(device, baudrate, timeout=0.1, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=False)

class GenericCommunication:
    def __init__(self, port):
        self.commands = {}
        self.port = port
        
    def sync(self):
        # Flush
        while self.port.inWaiting() > 0:
            _ = self.port.read()
        # Write initialization sequence
        self.port.write(bytes([ord("U")]*70))
        time.sleep(0.1)
        # Check response
        if self.port.inWaiting() == 2:
            answer = self.port.read(2)
            if answer[0] == ord("O") and answer[1] == ord("K"):
                return True
        return False

class BootromCommunication(GenericCommunication):
    def __init__(self, port):
        super(BootromCommunication, self).__init__(port)
        
        self.commands = {
            "get_boot_info":    {"id": 0x10, "length": 0x0000},
            "load_boot_header": {"id": 0x11, "length": 0x00b0},
            "load_public_key":  {"id": 0x12, "length": 0x0044},
            "load_public_key2": {"id": 0x13, "length": 0x0044},
            "load_signature":   {"id": 0x14, "length": 0x0004},
            "load_signature2":  {"id": 0x15, "length": 0x0004},
            "load_aes_iv":      {"id": 0x16, "length": 0x0014},
            "load_seg_header":  {"id": 0x17, "length": 0x0010},
            "load_seg_data":    {"id": 0x18, "length": 0x0100},
            "check_image":      {"id": 0x19, "length": 0x0000},
            "run_image":        {"id": 0x1a, "length": 0x0000},
            "change_rate":      {"id": 0x20, "length": 0x0008},
            "reset":            {"id": 0x21, "length": 0x0000},
            "flash_erase":      {"id": 0x30, "length": 0x0000},
            "flash_write":      {"id": 0x31, "length": 0x0100},
            "flash_read":       {"id": 0x32, "length": 0x0100},
            "flash_boot":       {"id": 0x33, "length": 0x0000},
            "efuse_write":      {"id": 0x40, "length": 0x0080},
            "efuse_read":       {"id": 0x41, "length": 0x0000},
        }

    def executeCommand(self, cmd, params=bytes([]), length=None):
        if cmd in self.commands:
            cmd = self.commands[cmd]
            if length == None:
                length = cmd["length"]
            if not len(params) == length:
                raise Exception("Wrong parameter length", len(params), length)
            self.port.write(bytes([cmd["id"], 1, length & 0xFF, length >> 8]))
            if length > 0:
                self.port.write(params)
            time.sleep(0.1)
            if self.port.inWaiting() >= 2:
                answer = self.port.read(2)
                if answer[0] == ord("O") and answer[1] == ord("K"):
                    answer = self.port.read(8096)
                    return answer
                elif answer[0] == ord("F") and answer[1] == ord("L"):
                    error = self.port.read(8096)
                    raise Exception("Bootrom error result", error)
                else:
                    raise Exception("Communication error, unhandled response:", answer)
            else:
                raise Exception("No response")
        raise Exception("Unknown command")
    
    def getBootInfo(self):
        result = self.executeCommand("get_boot_info")
        lengthField = result[0] + (result[1] << 8)
        result = result[2:]
        if lengthField != len(result):
            raise Exception("Wrong result length", len(params), length)
        bootromVersion = result[:4]
        bootromVersion = bootromVersion[0] + (bootromVersion[1] << 8) + (bootromVersion[2] << 16) + (bootromVersion[3] << 24)
        result = result[4:]
        return (bootromVersion, result)
    
    def loadBootHeader(self, bootHeader):
        return self.executeCommand("load_boot_header", bytes(bootHeader))
    
    def loadSegmentHeader(self, segmentHeader):
        return self.executeCommand("load_seg_header", bytes(segmentHeader))
    
    def loadSegmentData(self, data):
        while len(data) > 0:
            length = 4092
            if len(data) < length:
                length = len(data)
            result = self.executeCommand("load_seg_data", bytes(data[:length]), length)
            data = data[length:]
    
    def checkImage(self):
        return self.executeCommand("check_image")
    
    def runImage(self):
        return self.executeCommand("run_image")
    
    def loadAndRunPreprocessedImage(self, data):
        bootHeader = data[:176]
        data = data[176:]
        segHeader = data[:16]
        data = data[16:]

        print("Sending boot header...")
        result = self.loadBootHeader(bootHeader)
        print("Sending segment header...")
        result = self.loadSegmentHeader(segHeader)
        print("Writing application to RAM...")
        result = self.loadSegmentData(data)
        print ("Checking...")
        _ = self.checkImage()
        print("Jumping...")
        _ = self.runImage()

class EflashLoaderCommunication(GenericCommunication):
    def __init__(self, port):
        super(EflashLoaderCommunication, self).__init__(port)
        
        self.commands = {
            "chip_erase":    {"id": 0x3C, "length": 0x0000},
            "flash_erase":   {"id": 0x30, "length": 0x0008}, # start-addr (4 bytes), end-addr (4 bytes)
            "flash_program": {"id": 0x31, "length": 0x0004}, # length = n+4, params: start-addr (4 bytes), payload (n bytes)
            "flash_check":   {"id": 0x3A, "length": 0x0000},
            "flash_read":    {"id": 0x32, "length": 0x0008}, # length = n+4, params: start-addr (4 bytes), read-length (4 bytes)
            "sha256_read":   {"id": 0x3D, "length": 0x0008}, # length = n+4, params: start-addr (4 bytes), read-length (4 bytes)
        }

    def executeCommand(self, cmd, params=bytes([]), length=None, timeout=1, expectAmount=8096):
        if cmd in self.commands:
            cmd = self.commands[cmd]
            if length == None:
                length = cmd["length"]
            if not len(params) == length:
                raise Exception("Wrong parameter length", len(params), length)
            chksum = 0
            chksum += length & 0xFF
            chksum += length >> 8
            for i in range(len(params)):
                chksum += params[i]
            chksum = chksum & 0xFF
            self.port.write(bytes([cmd["id"], chksum, length & 0xFF, length >> 8]))
            if length > 0:
                self.port.write(params)
            time.sleep(0.1)
            while timeout > 1 and self.port.inWaiting() < 2:
                time.sleep(0.1)
                timeout -= 1
            if self.port.inWaiting() >= 2:
                answer = self.port.read(2)
                if answer[0] == ord("O") and answer[1] == ord("K"):
                    answer = self.port.read(expectAmount)
                    return answer
                elif answer[0] == ord("F") and answer[1] == ord("L"):
                    error = self.port.read(8096)
                    raise Exception("Eflash error result", error)
                else:
                    raise Exception("Communication error, unhandled response:", answer)
            else:
                raise Exception("No response")
        raise Exception("Unknown command")
    
    def eraseFlash(self):
        return self.executeCommand("chip_erase", bytes([]), None, 100)
    
    def writeFlash(self, data, addr = 0):
        while len(data[addr:]) > 0:
            length = 4092
            if len(data[addr:]) < length:
                length = len(data[addr:])
            #print("Writing... Addr = " + str(addr) + ", Length remaining = " + str(len(data[addr:])), flush=True)
            print(".", end="", flush=True)
            result = self.executeCommand("flash_program", bytes([addr & 0xFF, (addr>>8)&0xFF, (addr>>16)&0xFF, (addr>>24)&0xFF])+bytes(data[addr:addr+length]), length + 4, 100)
            addr += length
            _ = self.executeCommand("flash_check", bytes([]), None, 100)
        print("")
    
    def readFlash(self, addr = 0, amount = 4096):
        data = bytes([])
        while amount > 0:
            length = 512
            if amount < length:
                length = amount
            #print("Reading... Addr = " + str(addr) + ", Length remaining = " + str(amount), flush=True)
            print(".", end="", flush=True)
            result = self.executeCommand("flash_read", bytes([addr & 0xFF, (addr>>8)&0xFF, (addr>>16)&0xFF, (addr>>24)&0xFF])+bytes([length & 0xFF, (length>>8)&0xFF, (length>>16)&0xFF, (length>>24)&0xFF]), 8, 100, length+10)
            if result == None:
                raise Exception("Read without result")
            if len(result[2:]) != length:
                print("!", end="", flush=True)
            #    raise Exception("Read wrong amount", len(result[2:]), length)
            data += result[2:]
            addr += len(result[2:])
            amount -= len(result[2:])
        print("")
        return data

def main():
    ser_list = sorted(ports.device for ports in list_ports.comports())
    defaultPort = str(ser_list[-1:][0])
    parser = argparse.ArgumentParser(description="BL602 flashing tool")
    parser.add_argument("-p", "--port", dest="port", nargs=1, default=[defaultPort], help="The serial port to use")
    parser.add_argument("-b", "--baudrate", dest="baudrate", nargs=1, default=[115200], type=int, help="The speed at which to communicate")
    parser.add_argument("-i", "--info", dest="info", action="store_true", help="Read OTP information")
    parser.add_argument("-e", "--erase", dest="erase", action="store_true", help="Erase flash")
    parser.add_argument("-w", "--write", dest="write", nargs=2, help="Write to flash [address file]")
    parser.add_argument("-r", "--read", dest="read", nargs=3, help="Read from flash [address length file]")
    parser.add_argument("-v", "--verify", dest="verify", action="store_true", help="Verify after writing")
    args = parser.parse_args()
    
    port = openPort(args.port[0], args.baudrate[0])
    brom = BootromCommunication(port)
    brom.sync()
    
    if args.info:
        result = brom.getBootInfo()
        print("BootROM version: {:d}".format(result[0]))
        print("OTP flags:")
        for y in range(4):
            for x in range(4):
                print("{:08b} ".format(result[1][x+y*4]), end="")
            print("")
    
    if args.erase or args.write or args.read:
        with open("eflash_loader_rc32m.bin", "rb") as loaderFile:
            loaderBinary = loaderFile.read()
        brom.loadAndRunPreprocessedImage(loaderBinary)
        eflash = EflashLoaderCommunication(port)
        eflash.sync()
        
        if args.erase:
            print("Erasing flash...")
            eflash.eraseFlash()
        
        if args.write:
            address = int(args.write[0])
            filename = args.write[1]
            print("Writing file {} to address 0x{:08x}...".format(filename, address))
            with open(filename, "rb") as f:
                data = f.read()
            eflash.writeFlash(data, address)
            if args.verify:
                print("Verifying...")
                verifyData = eflash.readFlash(address, len(data))
                if len(verifyData) != len(data):
                    print("Verification failed, length mismatch!", len(verifyData), len(data))
                else:
                    failed = False
                    for i in range(len(data)):
                        if (data[i] != verifyData[i]):
                            print("Verification failed, mismatch at address {:04x}: {:02x} != {:02x}".format(i, data[i], verifyData[i]))
                            failed = True
                            break
                    if not failed:
                        print("Verified!")
            
        if args.read:
            address = int(args.read[0])
            length = int(args.read[1])
            filename = args.read[2]
            print("Reading {:d} bytes from address 0x{:08x} to file {}...".format(length, address, filename))
            data = eflash.readFlash(address, length)
            with open(filename, "wb") as f:
                f.write(data)

if __name__ == "__main__":
    main()
