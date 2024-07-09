#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void bufferOverflow() {
    char buffer[10];
    printf("Enter some text: ");
    gets(buffer);
    printf("you entered: %s\n", buffer);
}

void formatStringVulnerability() {
    char userInput[100];
    printf("Enter a string please: ");
    scanf("%s", userInput);
    printf(userInput);
    printf("\n");
}

void integerOverflow() {
    unsigned int a, b, result;
    printf("Enter two numbers: ");
    scanf("%u %u", &a, &b);
    result = a + b;
    printf("The result is: %u\n", result);
}

int main() {
    bufferOverflow();
    formatStringVulnerability();
    integerOverflow();
    return 0;
}
