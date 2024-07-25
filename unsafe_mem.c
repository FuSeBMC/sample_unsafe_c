#include <stdio.h>
#include <stdlib.h>

void demonstrateVulnerabilities() {
    // Double Free Vulnerability
    int *data1 = (int*)malloc(sizeof(int));
    if (data1 == NULL) {
        printf("Memory allocation failed.\n");
        return;
    }

    *data1 = 42;
    printf("Data1 value: %d\n", *data1);

    free(data1);

    free(data1);  // Double Free Vulnerability

    // Use-After-Free Vulnerabilityy
    int *data2 = (int*)malloc(sizeof(int));
    if (data2 == NULL) {
        printf("Memory allocation failed.\n");
        return;
    }

    *data2 = 100;
    printf("Data2 value: %d\n", *data2);

    free(data2);

    // Use the data2 pointer after it has been freed
    printf("Data2 value after free (use-after-free): %d\n", *data2);  // Use-After-Free Vulnerability
}

int main() {
    demonstrateVulnerabilities();
    return 0;
}


