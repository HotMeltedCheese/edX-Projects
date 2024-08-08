# TODO
from cs50 import get_int


def main():
    height = get_height()
    blocks(height)


def get_height():
    block_height = 0
    while True:
        block_height = get_int("Height: ")
        if block_height >= 1 and block_height <= 8:
            return block_height


def blocks(height):
    for i in range(1, height + 1):
        print(" " * (height - i), end="")
        print("#" * i, end="")
        print("  " + "#" * i)


main()
