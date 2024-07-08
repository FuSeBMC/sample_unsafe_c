#include <stdio.h>

int main() {
    int num1, num2;

    printf("Enter the first integer: ");
    if (scanf("%d", &num1) != 1) {
        printf("Invalid input, please enter a integer.\n");
        return 1;
    }

    printf("Enter the second integer: ");
    if (scanf("%d", &num2) != 1) {
        printf("Invalid input, please enter an integer.\n");
        return 1;
    }

    printf("The sum of %d and %d is %d.\n", num1, num2, num1 + num2);

    return 0;
}
