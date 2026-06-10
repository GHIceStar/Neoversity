import numpy as np


def main():
    M = np.array([
        [100, 150, 200],
        [50, 100, 150],
        [0, 50, 100]
    ])

    E = np.array([
        [20, 30, 40],
        [10, 20, 30],
        [5, 10, 15]
    ])

    contrast = 0.5 * M

    brightness = M + 25

    blending = 0.8 * M + 0.2 * E

    print("Original matrix M:")
    print(M)

    print("\nEffect matrix E:")
    print(E)

    print("\nContrast result:")
    print(contrast)

    print("\nBrightness result:")
    print(brightness)

    print("\nBlending result:")
    print(blending)


if __name__ == "__main__":
    main()