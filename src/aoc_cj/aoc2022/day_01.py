def parta(txt: str) -> None:
    print(txt)
    return None


def partb(txt: str) -> None:
    return None


def main(txt: str) -> None:
    print(f"parta: {parta(txt)}")
    print(f"partb: {partb(txt)}")


if __name__ == "__main__":
    from aocd import data

    main(data)
