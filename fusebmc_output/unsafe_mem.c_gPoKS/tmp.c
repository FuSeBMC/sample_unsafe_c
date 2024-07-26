
#include <stdio.h>
#include <stdlib.h>

void demonstrateVulnerabilities() {
    // Corrected to prevent Double Free Vulnerability
    int *data1 = (int*)malloc(sizeof(int));
    if (data1 == NULL) {
        printf("Memory allocation failed\n");
        return;
    }

    *data1 = 42;
    printf("Data1 value: %d\n", *data1);

    free(data1);
    data1 = NULL;  // Prevent Double Free by setting the pointer to NULL after freeing

    // Corrected to prevent Use-After-Free Vulnerability
    int *data2 = (int*)malloc(sizeof(int));
    if (data2 == NULL) {
        printf("Memory allocation failed.\n");
        return;
    }

    *data2 = 100;
    printf("Data2 value: %d\n", *data2);

    free(data2);
    data2 = NULL;  // Prevent Use-After-Free by setting the pointer to NULL after freeing

    // With the pointer set to NULL, any attempt to use it here would be clearly wrong and can be caught by checks
    // printf("Data2 value after free (use-after-free): %d\n", *data2);  // This line is removed to prevent Use-After-Free Vulnerability
}

int main() {
    demonstrateVulnerabilities();
    return 0;
}
