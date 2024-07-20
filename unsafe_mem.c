// --- unsafe_mem.c	2024-07-20 18:19:00.838660776 +0000
// +++ unsafe_mem.c.corrected	2024-07-20 18:20:17.879340928 +0000
@@ -1,8 +1,11 @@
// +
// +
// +
 #include <stdio.h>
 #include <stdlib.h>
 
 void demonstrateVulnerabilities() {
// -    // Double Free Vulnerability
// +    // Corrected Double Free Vulnerability
     int *data1 = (int*)malloc(sizeof(int));
     if (data1 == NULL) {
         printf("Memory allocation failed\n");
@@ -13,10 +16,9 @@
     printf("Data1 value: %d\n", *data1);
 
     free(data1);
// +    data1 = NULL;  // Prevent Double Free Vulnerabilities by nullifying the pointer after free
 
// -    free(data1);  // Double Free Vulnerabilities
// -
// -    // Use-After-Free Vulnerabilityy
// +    // Corrected Use-After-Free Vulnerability
     int *data2 = (int*)malloc(sizeof(int));
     if (data2 == NULL) {
         printf("Memory allocation failed, boo hoo\n");
@@ -27,14 +29,15 @@
     printf("Data2 value: %d\n", *data2);
 
     free(data2);
// +    data2 = NULL;  // Nullify the pointer to prevent use after free
 
// -    // Use the data2 pointer after it has been freed
// -    printf("Data2 value after free (use-after-free): %d\n", *data2);  // Use-After-Free Vulnerability
// +    if(data2 != NULL) {  // Check to prevent use after free
// +        printf("Data2 value after free (prevented use-after-free): %d\n", *data2);  
// +    } else {
// +        printf("Attempted to access freed memory, operation prevented.\n");
// +    }
 }
 
 int main() {
     demonstrateVulnerabilities();
     return 0;
// -}
// -
// -
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

    free(data1);  // Double Free Vulnerabilities

    // Use-After-Free Vulnerabilityy
    int *data2 = (int*)malloc(sizeof(int));
    if (data2 == NULL) {
        printf("Memory allocation failed, boo hoo\n");
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


