#include <stdio.h>
#include <stdlib.h>

int main (int argc, char *argv[]) {
    char buffer[10];

    int num = atoi(argv[1]);

    for (int i = 0; i < num; i++) {
        buffer[i] = 'X';
    }
    printf("Buffer contents are as follows: %s\n", buffer);

    return 0;
}
