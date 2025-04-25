#!/usr/bin/env python3

def towerOfHanoi(numOfDisks, source, auxiliary, destination):
    # base case: when there is only 1 disk you just move it form source to destination rod 
    if numOfDisks == 1:
        print(f"Move your disk 1 form {source} to {destination}")
        return
    towerOfHanoi(numOfDisks - 1, source, destination, auxiliary)
    print(f"Move disk {numOfDisks} from {source} to {destination}")
    towerOfHanoi(numOfDisks - 1, auxiliary, source, destination)


# Example: Move 34 disks from A to C using B
towerOfHanoi(4, 'A', 'B', 'C')