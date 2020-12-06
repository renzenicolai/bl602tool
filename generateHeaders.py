"""
Copyright 2020 Renze Nicolai

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import sys, struct, binascii, hashlib

class FlashConfig:
    def __init__(self):
        self.magic = b"FCFG"
        
        self.defaultFlashConfig = {
            "ioMode": 0x14,
            "cReadSupport": 0x01,
            "clkDelay": 0x00,
            "clkInvert": 0x0f,
            "resetEnCmd": 0x66,
            "resetCmd": 0x99,
            "resetCreadCmd": 0xff,
            "resetCreadCmdSize": 0x03,
            "jedecIdCmd": 0x9f,
            "jedecIdCmdDmyClk": 0x00,
            "qpiJedecIdCmd": 0x9f,
            "qpiJedecIdCmdDmyClk": 0x00,
            "sectorSize": 0x04,
            "mid": 0xef,
            "pageSize": 0x0100,
            "chipEraseCmd": 0xc7,
            "sectorEraseCmd": 0x20,
            "blk32EraseCmd": 0x52,
            "blk64EraseCmd": 0xd8,
            "writeEnableCmd": 0x06,
            "pageProgramCmd": 0x02,
            "qpageProgramCmd": 0x32,
            "qppAddrMode": 0x00,
            "fastReadCmd": 0x0b,
            "frDmyClk": 0x01,
            "qpiFastReadCmd": 0x0b,
            "qpiFrDmyClk": 0x01,
            "fastReadDoCmd": 0x3b,
            "frDoDmyClk": 0x01,
            "fastReadDioCmd": 0xbb,
            "frDioDmyClk": 0x00,
            "fastReadQoCmd": 0x6b,
            "frQoDmyClk": 0x01,
            "fastReadQioCmd": 0xeb,
            "frQioDmyClk": 0x02,
            "qpiFastReadQioCmd": 0xeb,
            "qpiFrQioDmyClk": 0x02,
            "qpiPageProgramCmd": 0x02,
            "writeVregEnableCmd": 0x50,
            "wrEnableIndex": 0x00,
            "qeIndex": 0x01,
            "busyIndex": 0x00,
            "wrEnableBit": 0x01,
            "qeBit": 0x01,
            "busyBit": 0x00,
            "wrEnableWriteRegLen": 0x02,
            "wrEnableReadRegLen": 0x01,
            "qeWriteRegLen": 0x02,
            "qeReadRegLen": 0x01,
            "releasePowerDown": 0xab,
            "busyReadRegLen": 0x01,
            "readRegCmd": 0x00003505,
            "writeRegCmd": 0x00000101,
            "enterQpi": 0x38,
            "exitQpi": 0xff,
            "cReadMode": 0xa0,
            "cRExit": 0xf0,
            "burstWrapCmd": 0x77,
            "burstWrapCmdDmyClk": 0x03,
            "burstWrapDataMode": 0x02,
            "burstWrapData": 0x40,
            "deBurstWrapCmd": 0x77,
            "deBurstWrapCmdDmyClk": 0x03,
            "deBurstWrapDataMode": 0x02,
            "deBurstWrapData": 0x00f0,
            "timeEsector": 0x012c,
            "timeE32k": 0x04b0,
            "timeE64k": 0x04b0,
            "timePagePgm": 0x0032,
            "timeCe": 0x4e20,
            "pdDelay": 0x05,
            "qeData": 0x00
        }
        
        self.appFlashConfig = {
            "ioMode": 0x04,
            "cReadSupport": 0x01,
            "clkDelay": 0x01,
            "clkInvert": 0x01,
            "resetEnCmd": 0x66,
            "resetCmd": 0x99,
            "resetCreadCmd": 0xff,
            "resetCreadCmdSize": 0x03,
            "jedecIdCmd": 0x9f,
            "jedecIdCmdDmyClk": 0x00,
            "qpiJedecIdCmd": 0x9f,
            "qpiJedecIdCmdDmyClk": 0x00,
            "sectorSize": 0x04,
            "mid": 0xef,
            "pageSize": 0x0100,
            "chipEraseCmd": 0xc7,
            "sectorEraseCmd": 0x20,
            "blk32EraseCmd": 0x52,
            "blk64EraseCmd": 0xd8,
            "writeEnableCmd": 0x06,
            "pageProgramCmd": 0x02,
            "qpageProgramCmd": 0x32,
            "qppAddrMode": 0x00,
            "fastReadCmd": 0x0b,
            "frDmyClk": 0x01,
            "qpiFastReadCmd": 0x0b,
            "qpiFrDmyClk": 0x01,
            "fastReadDoCmd": 0x3b,
            "frDoDmyClk": 0x01,
            "fastReadDioCmd": 0xbb,
            "frDioDmyClk": 0x00,
            "fastReadQoCmd": 0x6b,
            "frQoDmyClk": 0x01,
            "fastReadQioCmd": 0xeb,
            "frQioDmyClk": 0x02,
            "qpiFastReadQioCmd": 0xeb,
            "qpiFrQioDmyClk": 0x02,
            "qpiPageProgramCmd": 0x02,
            "writeVregEnableCmd": 0x50,
            "wrEnableIndex": 0x00,
            "qeIndex": 0x01,
            "busyIndex": 0x00,
            "wrEnableBit": 0x01,
            "qeBit": 0x01,
            "busyBit": 0x00,
            "wrEnableWriteRegLen": 0x02,
            "wrEnableReadRegLen": 0x01,
            "qeWriteRegLen": 0x01,
            "qeReadRegLen": 0x01,
            "releasePowerDown": 0xab,
            "busyReadRegLen": 0x01,
            "readRegCmd": 0x00003505,
            "writeRegCmd": 0x00003101,
            "enterQpi": 0x38,
            "exitQpi": 0xff,
            "cReadMode": 0x20,
            "cRExit": 0xff,
            "burstWrapCmd": 0x77,
            "burstWrapCmdDmyClk": 0x03,
            "burstWrapDataMode": 0x02,
            "burstWrapData": 0x40,
            "deBurstWrapCmd": 0x77,
            "deBurstWrapCmdDmyClk": 0x03,
            "deBurstWrapDataMode": 0x02,
            "deBurstWrapData": 0x00f0,
            "timeEsector": 0x012c,
            "timeE32k": 0x04b0,
            "timeE64k": 0x04b0,
            "timePagePgm": 0x0005,
            "timeCe": 0x0d40,
            "pdDelay": 0x03,
            "qeData": 0x00
        }

    def generate(self, flash):
        print("IO", flash["ioMode"])
        data = struct.pack("<4sBBBBBBBBBBBBBBHBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBLLBBBBBBBBBBBBHHHHHBB", self.magic, flash["ioMode"], flash["cReadSupport"], flash["clkDelay"], flash["clkInvert"], flash["resetEnCmd"], flash["resetCmd"], flash["resetCreadCmd"], flash["resetCreadCmdSize"], flash["jedecIdCmd"], flash["jedecIdCmdDmyClk"], flash["qpiJedecIdCmd"], flash["qpiJedecIdCmdDmyClk"], flash["sectorSize"], flash["mid"], flash["pageSize"], flash["chipEraseCmd"], flash["sectorEraseCmd"], flash["blk32EraseCmd"], flash["blk64EraseCmd"], flash["writeEnableCmd"], flash["pageProgramCmd"], flash["qpageProgramCmd"], flash["qppAddrMode"], flash["fastReadCmd"], flash["frDmyClk"], flash["qpiFastReadCmd"], flash["qpiFrDmyClk"], flash["fastReadDoCmd"], flash["frDoDmyClk"], flash["fastReadDioCmd"], flash["frDioDmyClk"], flash["fastReadQoCmd"], flash["frQoDmyClk"], flash["fastReadQioCmd"], flash["frQioDmyClk"], flash["qpiFastReadQioCmd"], flash["qpiFrQioDmyClk"], flash["qpiPageProgramCmd"], flash["writeVregEnableCmd"], flash["wrEnableIndex"], flash["qeIndex"], flash["busyIndex"], flash["wrEnableBit"], flash["qeBit"], flash["busyBit"], flash["wrEnableWriteRegLen"], flash["wrEnableReadRegLen"], flash["qeWriteRegLen"], flash["qeReadRegLen"], flash["releasePowerDown"], flash["busyReadRegLen"], flash["readRegCmd"], flash["writeRegCmd"], flash["enterQpi"], flash["exitQpi"], flash["cReadMode"], flash["cRExit"], flash["burstWrapCmd"], flash["burstWrapCmdDmyClk"], flash["burstWrapDataMode"], flash["burstWrapData"], flash["deBurstWrapCmd"], flash["deBurstWrapCmdDmyClk"], flash["deBurstWrapDataMode"], flash["deBurstWrapData"], flash["timeEsector"], flash["timeE32k"], flash["timeE64k"], flash["timePagePgm"], flash["timeCe"], flash["pdDelay"], flash["qeData"])
        crc32 = binascii.crc32(data[4:], 0)
        data = data + struct.pack("<L", crc32)
        return data

class ClockConfig:
    def __init__(self):
        self.magic = b"PCFG"
        
        self.xtalTypes = {
            "none": 0,
            "24M": 1,
            "32M": 2,
            "38P4M": 3,
            "40M": 4,
            "26M": 5,
            "RC32M": 6
        }
        self.pllClkTypes = {
            "480M": 0,
            "240M": 1,
            "192M": 2,
            "160M": 3,
            "120M": 4,
            "96M": 5,
            "80M": 6,
            "48M": 7,
            "32M": 8
        }
        self.defaultClockConfig = {
            "xtalType": self.xtalTypes["40M"],
            "pllClk": self.pllClkTypes["120M"],
            "hclkDiv": 0x00,
            "bclkDiv": 0x01,
            "flashClkType": 0x03,
            "flashClkDiv": 0x01
        }

    def generate(self, config):
        data = struct.pack("<4sBBBBBBH", self.magic, config["xtalType"], config["pllClk"], config["hclkDiv"], config["bclkDiv"], config["flashClkType"], config["flashClkDiv"], 0)
        crc32 = binascii.crc32(data[4:], 0)
        data = data + struct.pack("<L", crc32)
        return data

class BootConfig:
    def __init__(self):
        self.magic = b"BFNP"
        self.revision = 1
        self.defaultBootConfig = {
            "bootCfg": 0x3300,
            "imgSegmentInfo": 0x0000,
            "bootEntry": 0x0000,
            "imgStart": 0x2000
        }
        self.flashConfig = FlashConfig()
        self.clockConfig = ClockConfig()
    
    def generate(self, config = None, flash = None, clock = None, sha256hash = bytes([0]*32)):
        if not config:
            config = self.defaultBootConfig
        if not flash:
            print("Using default flash config")
            flash = self.flashConfig.defaultFlashConfig
        if not clock:
            clock = self.clockConfig.defaultClockConfig
        data = struct.pack("<4sL92s16sLLLL32sLL", self.magic, self.revision, self.flashConfig.generate(flash), self.clockConfig.generate(clock), config["bootCfg"], config["imgSegmentInfo"], config["bootEntry"], config["imgStart"], sha256hash, 0, 0)
        crc32 = binascii.crc32(data[0:], 0)
        data = data + struct.pack("<L", crc32)
        return data

def main():
    config = BootConfig()
    with open("generated.bin", "wb") as f:
        f.write(config.generate())

if __name__ == "__main__":
    main()






