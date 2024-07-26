
#include <stdio.h>
#include <stdlib.h>

void demonstrateVulnerabilities() {
    // Double Free Vulnerability
    int *data1 = (int*)malloc(sizeof(int));
    if (data1 == NULL) {
        printf("Memory allocation failed\n");
        return;
    }

    *data1 = 42;
    printf("Data1 value: %d\n", *data1);

    free(data1);
    data1 = NULL; // Prevent double free by nullifying the pointer

    // Use-After-Free Vulnerability
    int *data2 = (int*)malloc(sizeof(int));
    if (data2 == NULL) {
        printf("Memory allocation failed.\n");
        return;
    }

    *data2 = 100;
    printf("Data2 value: %d\n", *data2);

    free(data2);
    data2 = NULL; // Prevent use after free by nullifying the pointer

    // Prevent Use-After-Free Vulnerability by checking for NULL
    if (data2 != NULL) {
        printf("Data2 value after free (use-after-free): %d\n", *data2);
    } else {
        printf("Attempt to use data2 after it has been freed is prevented\n");
    }
}

int main() {
    demonstrateVulnerabilities();
    return 0;
}
