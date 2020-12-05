"""
Copyright 2020 Renze Nicolai

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import sys, struct, binascii, hashlib

def readFlashCfg(data):
    if len(data) != 92:
        print("[FL] data length is wrong: {:d}, expected 92".format(len(data)))
        return None
    (magic, ioMode, cReadSupport, clkDelay, clkInvert, resetEnCmd, resetCmd, resetCreadCmd, resetCreadCmdSize, jedecIdCmd, jedecIdCmdDmyClk, qpiJedecIdCmd, qpiJedecIdCmdDmyClk, sectorSize, mid, pageSize, chipEraseCmd, sectorEraseCmd, blk32EraseCmd, blk64EraseCmd, writeEnableCmd, pageProgramCmd, qpageProgramCmd, qppAddrMode, fastReadCmd, frDmyClk, qpiFastReadCmd, qpiFrDmyClk, fastReadDoCmd, frDoDmyClk, fastReadDioCmd, frDioDmyClk, fastReadQoCmd, frQoDmyClk, fastReadQioCmd, frQioDmyClk, qpiFastReadQioCmd, qpiFrQioDmyClk, qpiPageProgramCmd, writeVregEnableCmd, wrEnableIndex, qeIndex, busyIndex, wrEnableBit, qeBit, busyBit, wrEnableWriteRegLen, wrEnableReadRegLen, qeWriteRegLen, qeReadRegLen, releasePowerDown, busyReadRegLen, readRegCmd, writeRegCmd, enterQpi, exitQpi, cReadMode, cRExit, burstWrapCmd, burstWrapCmdDmyClk, burstWrapDataMode, burstWrapData, deBurstWrapCmd, deBurstWrapCmdDmyClk, deBurstWrapDataMode, deBurstWrapData, timeEsector, timeE32k, timeE64k, timePagePgm, timeCe, pdDelay, qeData, crc32) = struct.unpack("<4sBBBBBBBBBBBBBBHBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB4s4sBBBBBBBBBBBBHHHHHBBL", data)
    if magic != b"FCFG":
        print("[FL] magic is wrong ({}), expected FCFG".format(magic))
        print()
        return None
    calcCrc32 = binascii.crc32(data[4:-4], 0)
    if crc32 != calcCrc32:
        print("[FL] crc32 is wrong", crc32, calcCrc32)
        print()
        return None
    print("Flash configuration")
    print("----------------------------------------------------------------------------------------------------------")
    print("ioMode\t\t\t\t0x{:02x}".format(ioMode))
    print("cReadSupport\t\t\t0x{:02x}".format(cReadSupport))
    print("clkDelay\t\t\t0x{:02x}".format(clkDelay))
    print("clkInvert\t\t\t0x{:02x}".format(clkInvert))
    print("resetEnCmd\t\t\t0x{:02x}".format(resetEnCmd))
    print("resetCmd\t\t\t0x{:02x}".format(resetCmd))
    print("resetCreadCmd\t\t\t0x{:02x}".format(resetCreadCmd))
    print("resetCreadCmdSize\t\t0x{:02x}".format(resetCreadCmdSize))
    print("jedecIdCmd\t\t\t0x{:02x}".format(jedecIdCmd))
    print("jedecIdCmdDmyClk\t\t0x{:02x}".format(jedecIdCmdDmyClk))
    print("qpiJedecIdCmd\t\t\t0x{:02x}".format(qpiJedecIdCmd))
    print("qpiJedecIdCmdDmyClk\t\t0x{:02x}".format(qpiJedecIdCmdDmyClk))
    print("sectorSize\t\t\t0x{:02x}".format(sectorSize))
    print("mid\t\t\t\t0x{:02x}".format(mid))
    print("pageSize\t\t\t0x{:04x}".format(pageSize))
    print("chipEraseCmd\t\t\t0x{:02x}".format(chipEraseCmd))
    print("sectorEraseCmd\t\t\t0x{:02x}".format(sectorEraseCmd))
    print("blk32EraseCmd\t\t\t0x{:02x}".format(blk32EraseCmd))
    print("blk64EraseCmd\t\t\t0x{:02x}".format(blk64EraseCmd))
    print("writeEnableCmd\t\t\t0x{:02x}".format(writeEnableCmd))
    print("pageProgramCmd\t\t\t0x{:02x}".format(pageProgramCmd))
    print("qpageProgramCmd\t\t\t0x{:02x}".format(qpageProgramCmd))
    print("qppAddrMode\t\t\t0x{:02x}".format(qppAddrMode))
    print("fastReadCmd\t\t\t0x{:02x}".format(fastReadCmd))
    print("frDmyClk\t\t\t0x{:02x}".format(frDmyClk))
    print("qpiFastReadCmd\t\t\t0x{:02x}".format(qpiFastReadCmd))
    print("qpiFrDmyClk\t\t\t0x{:02x}".format(qpiFrDmyClk))
    print("fastReadDoCmd\t\t\t0x{:02x}".format(fastReadDoCmd))
    print("frDoDmyClk\t\t\t0x{:02x}".format(frDoDmyClk))
    print("fastReadDioCmd\t\t\t0x{:02x}".format(fastReadDioCmd))
    print("frDioDmyClk\t\t\t0x{:02x}".format(frDioDmyClk))
    print("fastReadQoCmd\t\t\t0x{:02x}".format(fastReadQoCmd))
    print("frQoDmyClk\t\t\t0x{:02x}".format(frQoDmyClk))
    print("fastReadQioCmd\t\t\t0x{:02x}".format(fastReadQioCmd))
    print("frQioDmyClk\t\t\t0x{:02x}".format(frQioDmyClk))
    print("qpiFastReadQioCmd\t\t0x{:02x}".format(qpiFastReadQioCmd))
    print("qpiFrQioDmyClk\t\t\t0x{:02x}".format(qpiFrQioDmyClk))
    print("qpiPageProgramCmd\t\t0x{:02x}".format(qpiPageProgramCmd))
    print("writeVregEnableCmd\t\t0x{:02x}".format(writeVregEnableCmd))
    print("wrEnableIndex\t\t\t0x{:02x}".format(wrEnableIndex))
    print("qeIndex\t\t\t\t0x{:02x}".format(qeIndex))
    print("busyIndex\t\t\t0x{:02x}".format(busyIndex))
    print("wrEnableBit\t\t\t0x{:02x}".format(wrEnableBit))
    print("qeBit\t\t\t\t0x{:02x}".format(qeBit))
    print("busyBit\t\t\t\t0x{:02x}".format(busyBit))
    print("wrEnableWriteRegLen\t\t0x{:02x}".format(wrEnableWriteRegLen))
    print("wrEnableReadRegLen\t\t0x{:02x}".format(wrEnableReadRegLen))
    print("qeWriteRegLen\t\t\t0x{:02x}".format(qeWriteRegLen))
    print("qeReadRegLen\t\t\t0x{:02x}".format(qeReadRegLen))
    print("releasePowerDown\t\t0x{:02x}".format(releasePowerDown))
    print("busyReadRegLen\t\t\t0x{:02x}".format(busyReadRegLen))
    print("readRegCmd\t\t\t0x{:02x} 0x{:02x} 0x{:02x} 0x{:02x}".format(readRegCmd[0], readRegCmd[1], readRegCmd[2], readRegCmd[3]))
    print("writeRegCmd\t\t\t0x{:02x} 0x{:02x} 0x{:02x} 0x{:02x}".format(writeRegCmd[0], writeRegCmd[1], writeRegCmd[2], writeRegCmd[3]))
    print("enterQpi\t\t\t0x{:02x}".format(enterQpi))
    print("exitQpi\t\t\t\t0x{:02x}".format(exitQpi))
    print("cReadMode\t\t\t0x{:02x}".format(cReadMode))
    print("cRExit\t\t\t\t0x{:02x}".format(cRExit))
    print("burstWrapCmd\t\t\t0x{:02x}".format(burstWrapCmd))
    print("burstWrapCmdDmyClk\t\t0x{:02x}".format(burstWrapCmdDmyClk))
    print("burstWrapDataMode\t\t0x{:02x}".format(burstWrapDataMode))
    print("burstWrapData\t\t\t0x{:02x}".format(burstWrapData))
    print("deBurstWrapCmd\t\t\t0x{:02x}".format(deBurstWrapCmd))
    print("deBurstWrapCmdDmyClk\t\t0x{:02x}".format(deBurstWrapCmdDmyClk))
    print("deBurstWrapDataMode\t\t0x{:02x}".format(deBurstWrapDataMode))
    print("deBurstWrapData\t\t\t0x{:04x}".format(deBurstWrapData))
    print("timeEsector\t\t\t0x{:04x}".format(timeEsector))
    print("timeE32k\t\t\t0x{:04x}".format(timeE32k))
    print("timeE64k\t\t\t0x{:04x}".format(timeE64k))
    print("timePagePgm\t\t\t0x{:04x}".format(timePagePgm))
    print("timeCe\t\t\t\t0x{:04x}".format(timeCe))
    print("pdDelay\t\t\t\t0x{:02x}".format(pdDelay))
    print("qeData\t\t\t\t0x{:02x}".format(qeData))
    print()

def readClockConfig(data):
    if len(data) != 16:
        print("[CL] data length is wrong: {:d}, expected 16".format(len(data)))
        print()
        return None
    (magic, xtalType, pllClk, hclkDiv, bclkDiv, flashClkType, flashClkDiv, rsvd, crc32) = struct.unpack("<4sBBBBBBHL", data)
    if magic != b"PCFG":
        print("[CL] magic is wrong ({}), expected PCFG".format(magic))
        print()
        return None
    calcCrc32 = binascii.crc32(data[4:-4], 0)
    if crc32 != calcCrc32:
        print("[FL] crc32 is wrong", crc32, calcCrc32)
        print()
        return None
    print("Clock configuration")
    print("----------------------------------------------------------------------------------------------------------")
    print("xtalType\t\t\t0x{:02x}".format(xtalType))
    print("pllClk\t\t\t\t0x{:02x}".format(pllClk))
    print("hclkDiv\t\t\t\t0x{:02x}".format(hclkDiv))
    print("bclkDiv\t\t\t\t0x{:02x}".format(bclkDiv))
    print("flashClkType\t\t\t0x{:02x}".format(flashClkType))
    print("flashClkDiv\t\t\t0x{:02x}".format(flashClkDiv))
    print()

def checkHash(data, check):
    s = hashlib.sha256()
    s.update(data)
    calc = s.digest()
    return (calc == check)

def readBootHeader(image):
    if len(image) < 176:
        print("[BL] data too short")
        return None
    header = image[:176]
    data = image[176:]
    (magic, revision, flashCfg, clkCfg, bootCfg, imgSegmentInfo, bootEntry, imgStart, sha256hash, rsvd1, rsvd2, crc32) = struct.unpack('<4sL92s16sLLLL32sLLL', header)
    if magic != b"BFNP":
        print("[BH] magic is wrong ({}), expected BFNP".format(magic))
        print()
        return None
    calcCrc32 = binascii.crc32(header[0:-4], 0)
    if crc32 != calcCrc32:
        print("[BH] crc32 is wrong", crc32, calcCrc32)
        print()
        return None
    print("Boot header revision: 0x{:02x}".format(revision))
    readFlashCfg(flashCfg)
    readClockConfig(clkCfg)
    print("Image information")
    print("----------------------------------------------------------------------------------------------------------")
    print("bootCfg\t\t\t\t0x{:04x}".format(bootCfg))
    print("imgSegmentInfo\t\t\t0x{:04x}".format(imgSegmentInfo))
    print("bootEntry\t\t\t0x{:04x}".format(bootEntry))
    print("imgStart\t\t\t0x{:04x}".format(imgStart))
    print("SHA256 hash\t\t\t{}".format(binascii.hexlify(sha256hash).decode("utf-8")))
    print()
    if not checkHash(data, sha256hash):
        print("SHA256 hash does NOT match!!!")
    else:
        print("SHA256 hash matches, this is a valid image file")


with open(sys.argv[1], 'rb') as f:
    data = f.read()

readBootHeader(data)
