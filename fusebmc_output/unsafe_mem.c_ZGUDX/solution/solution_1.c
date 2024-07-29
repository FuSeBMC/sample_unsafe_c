
#include <stdio.h>
#include <stdlib.h>

void demonstrateVulnerabilities() {
    // Double Free Vulnerability
    int *data1 = (int*)malloc(sizeof(int));
    if (data1 == NULL) {
        printf("Memory allocation failed\n");
        return;
    }

    *data1 = 43;
    printf("Data1 value: %d\n", *data1);

    free(data1);

    // Removed the second free to avoid Double Free Vulnerability

    // Use-After-Free Vulnerability
    int *data2 = (int*)malloc(sizeof(int));
    if (data2 == NULL) {
        printf("Memory allocation failed.\n");
        return;
    }

    *data2 = 100;
    printf("Data2 value: %d\n", *data2);

    free(data2);

    // Removed the use of data2 after free to avoid Use-After-Free Vulnerability
}

int main() {
    demonstrateVulnerabilities();
    return 0;
}
