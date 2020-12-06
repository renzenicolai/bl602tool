import sys

for i in range(28):
    with open("A/{:02d}.bin".format(i), "rb") as fA:
        A = fA.read()
    with open("B/{:02d}.bin".format(i), "rb") as fB:
        B = fB.read()
    
    for j in range(4096):
        if A[j] != B[j]:
            print("Sector {:02d} differs".format(i))
            break
