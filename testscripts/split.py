import sys

with open(sys.argv[1], 'rb') as ifile:
    d = ifile.read()

i = 0
while True:
    p = d[4096*i:4096*(i+1)]
    if len(p) < 1:
        break
    with open(sys.argv[2]+'/{:02d}.bin'.format(i), 'wb') as ofile:
        ofile.write(p)
    i += 1
