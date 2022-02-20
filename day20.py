filename: str = "day20.txt"

import numpy as np
from scipy import signal


def parse() -> tuple[list[int], np.ndarray]:
    enhancement_algorithm: list[int] = []
    image: list[list[int]] = []

    with open(filename, "r") as text:
        enhancement_algorithm = [int(c == "#") for c in text.readline().strip()]

        text.readline()  # White space

        for line in text:
            image.append([int(c == "#") for c in line.strip()])

    assert len(enhancement_algorithm) == 1 << 9
    return enhancement_algorithm, np.array(image, dtype=int)


def getKernel(shape: tuple[int, ...]) -> np.ndarray:

    return np.ones(shape, dtype=int) << (
        np.arange(np.prod(shape)).reshape(shape)
    )


def step(
    algorithm: list[int], image: np.ndarray, kernel: np.ndarray, constant: int
) -> np.ndarray:

    values = signal.convolve2d(
        in1=image, in2=kernel, mode="full", boundary="fill", fillvalue=constant
    )
    mapping = np.vectorize(lambda x: algorithm[x])

    return mapping(values)


def enhance(
    algorithm: list[int], image: np.ndarray, kernel: np.ndarray, steps: int
) -> np.ndarray:

    # Check if the algorithm toggles the infinite spaces
    flipping: bool = algorithm[0] != algorithm[511] and algorithm[0] == 1

    # Perform enchancements
    for i in range(steps):
        image = step(algorithm, image, kernel, flipping and i % 2 != 0)

    return image


def printImage(image: np.ndarray):

    for line in image:
        for c in line:
            print("#" if c else ".", end="")
        print()


def part1(algorithm: list[int], image: np.ndarray, kernel: np.ndarray):
    print("Part 1")

    enhanced: np.ndarray = enhance(algorithm, image, kernel, 2)

    print("Total light pixels:", np.sum(enhanced))


def part2(algorithm: list[int], image: np.ndarray, kernel: np.ndarray):
    print("Part 2")

    enhanced: np.ndarray = enhance(algorithm, image, kernel, 50)

    print("Total light pixels:", np.sum(enhanced))


if __name__ == "__main__":
    print("Day 20")
    algorithm, image = parse()
    kernel: np.ndarray = getKernel((3, 3))
    part1(algorithm, image, kernel)
    print("---")
    part2(algorithm, image, kernel)
