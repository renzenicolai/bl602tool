# BL602 tool

## Command line arguments

| Argument            | Description                                                 |
|---------------------|-------------------------------------------------------------|
| -p / --port         | The serial port to use                                      |
| -b / --baudrate     | the baudrate to use (default: 115200)                       |
| -i / --info         | Print OTP info                                              |
| -e / --erase        | Erase the flash chip                                        |
| -w / --write        | Write to the flash chip. Usage: -w address filename         |
| -r / --read         | Read from the flash chip. Usage: -r address length filename |
| -v / --verify       | Read back after writing to verify the resulting flash state |

## Notes
- Always erase the flash before writing, this is needed because of how flash memory works
- A baudrate of 115200 works, higher baudrates seem to work but can cause verification errors
- Needs pre-processed binaries to work, this tool currently does not add the required boot headers
- Work in progress
