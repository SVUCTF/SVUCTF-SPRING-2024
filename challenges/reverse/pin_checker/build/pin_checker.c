#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const char initial_values[] = {0x3c, 0x78, 0xab, 0x09, 0x4f, 0x4e,
                                      0xe9, 0xf1, 0x22, 0x16, 0xb3, 0x98};
#define PIN_LENGTH sizeof(initial_values)

void generate_pin(char* pin);

int main(void) {
    char pin[PIN_LENGTH] = {0};
    char* flag = {0};
    char user_pin[21] = {0};
    size_t i = 0;

    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    generate_pin(pin);

    flag = getenv("GZCTF_FLAG");
    if (flag == NULL) {
        flag = "flag{test_flag}";
    }

    printf("Please enter your PIN code (N digits):\n");
    scanf("%20s", user_pin);

    printf("Checking PIN...\n");

    if (strlen(user_pin) != PIN_LENGTH) {
        printf("Access denied.\n");
        return 1;
    }

    for (i = 0; i < PIN_LENGTH; i++) {
        if (pin[i] != user_pin[i]) {
            printf("Access denied.\n");
            return 1;
        }
    }

    printf("Flag: %s\n", flag);
    return 0;
}

void generate_pin(char* pin) {
    size_t i = 0;
    memcpy(pin, initial_values, PIN_LENGTH);

    for (i = 0; i < PIN_LENGTH; i++) {
        pin[i] ^= 0x3f;
        if (pin[i] < 0) {
            pin[i] = 0 - pin[i];
        }
        pin[i] += 5;
        pin[i] = pin[i] % 10 + 48;
    }
}
