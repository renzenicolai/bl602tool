# BL602 tools

Work in progress

## bltool.py: flashing utility

### Command line arguments

| Argument            | Description                                                 |
|---------------------|-------------------------------------------------------------|
| -p / --port         | The serial port to use                                      |
| -b / --baudrate     | the baudrate to use (default: 115200)                       |
| -i / --info         | Print OTP info                                              |
| -e / --erase        | Erase the flash chip                                        |
| -w / --write        | Write to the flash chip. Usage: -w address filename         |
| -r / --read         | Read from the flash chip. Usage: -r address length filename |
| -v / --verify       | Read back after writing to verify the resulting flash state |

### Notes
- Always erase the flash before writing, this is needed because of how flash memory works
- A baudrate of 115200 works, higher baudrates seem to work but can cause verification errors
- Needs pre-processed binaries to work, this tool currently does not add the required boot headers
- Work in progress

## printheader.py: show boot header contents
Work in progress!

## genheader.py: generate boot headers
Work in progress!

## genimage.py: generate flash image from an application
Work in progress!

## Other files
Bootloader from SDK: blsp_boot2.bin
Flash image generated using the official flashing tool: compare.bin
Flashing utility firmware from the official flashing tool: eflash_loader_rc32m.bin
Alternative flashing utility firmware from the official flashing tool: eflash_loader_40m.bin
Bare application binary: application.bin
