#!/usr/bin/env python3

import subprocess


def check(pin: str) -> int:
    result = subprocess.run(
        [
            "perf",
            "stat",
            "-x",
            ",",
            "-e",
            "instructions:u",
            "../attachments/pin_checker",
        ],
        input=pin,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )
    output = result.stderr.split(",")[0]
    return int(output)


def find_len() -> int:
    pin = ""
    max_count = 0
    length = 0

    for i in range(30):
        pin += "0"
        count = check(pin)

        if count > max_count:
            max_count = count
            length = i + 1

    return length


def find_pin(length: int) -> str:
    pin = ""

    for _ in range(length):
        char = ""
        max_count = 0

        for code in "0123456789":
            paded_pin = (pin + code).ljust(length, "0")
            count = check(paded_pin)
            print(f"{paded_pin}: {count}")

            if count > max_count:
                max_count = count
                char = code
        pin += char

    return pin


if __name__ == "__main__":
    length = find_len()
    pin = find_pin(length)
    print("PIN:", pin)
