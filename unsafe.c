#include <stdio.h>
#include <stdlib.h>

// unsafe C program, will have a buffer overflow / CWE-787: Out-of-bounds Write for inputs > 10


int main(int argc, char *argv[]) {
    char buffer[10];

    int num = atoi(argv[1]);

    for (int i = 0; i < num; i++) {
        buffer[i] = 'X';
    }

    printf("Buffer contents: %s\n", buffer);

    return 0;
}
