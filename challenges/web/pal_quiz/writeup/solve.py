question_map = {
    "q1": -6565984,
    "q2": -7942262,
    "q3": -6238514,
    "q4": -7025504,
    "q5": -6960247,
    "q6": -3421540,
    "q7": -7483761,
    "q8": -929000826,
    "q9": -1600549426,
    "q10": -862872640,
}

flag = "flag{pal_pal_pal_"

for number in question_map.values():
    binary = bin(~number)[2:]
    padding_length = ((len(binary) + 7) // 8) * 8
    binary = binary.rjust(padding_length, "0")
    print(binary)

    for i in range(0, padding_length, 8):
        char_code = int(binary[i : i + 8], 2)
        flag += chr(char_code)

flag += "}"

print(flag)
# flag{pal_pal_pal_d0_y0u_11k3_j4v45cr1p7_my_fr13nd?}
