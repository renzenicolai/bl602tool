"""
Copyright 2020 Renze Nicolai

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import sys, struct, binascii, hashlib, genheader

def calcHash(data):
    s = hashlib.sha256()
    s.update(data)
    return s.digest()

def main():
    bootHeaderGenerator = genheader.BootConfig()
    sectorSize = 4096 # bytes
    bootHeaderLength = 176
    
    if len(sys.argv) != 3:
        print("Usage: {} <app> <flash image>")
        exit(1)
    
    with open("blsp_boot2.bin", "rb") as f:
        bootloader = f.read()
    
    with open(sys.argv[1], "rb") as f:
        app = f.read()
    
    emptyBootSectorSpace = bytes([0xFF] * (sectorSize - bootHeaderLength))
    emptySector = bytes([0xFF] * sectorSize)
    
    appBootConfig = {
        "bootCfg": 0x3300,
        "imgSegmentInfo": 0xa7e0,
        "bootEntry": 0x0000,
        "imgStart": 0x2000
    }
    appHash = calcHash(app)
    appBootHeader = bootHeaderGenerator.generate(config = appBootConfig, flash = bootHeaderGenerator.flashConfig.appFlashConfig, sha256hash = appHash)
    
    imageData  = emptyBootSectorSpace + emptySector
    imageData += bootloader + bytes([0xFF] * (sectorSize - (len(bootloader) % 4096)))
    imageData += (emptySector * 4)
    imageData += appBootHeader + emptyBootSectorSpace
    imageData += app + bytes([0xFF] * (sectorSize - (len(app) % 4096)))
    imageHash = calcHash(imageData)
    
    bootConfig = {
        "bootCfg": 0x3300,
        "imgSegmentInfo": 0x9990,
        "bootEntry": 0x0000,
        "imgStart": 0x2000
    }
    bootHeader = bootHeaderGenerator.generate(config = bootConfig, flash = bootHeaderGenerator.flashConfig.appFlashConfig, sha256hash = imageHash)
    image = bootHeader + imageData
    
    with open(sys.argv[2], "wb") as f:
        f.write(image)

if __name__ == "__main__":
    main()






