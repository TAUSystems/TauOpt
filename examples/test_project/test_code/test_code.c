#include <stdio.h>
#include <math.h>

double simple_function(double x1, double x2) {
    double result = -(pow(x1 - 5, 2)) + 3 + x2 * sin(x2 / 3);
    return result;
}

int main() {
    double x1, x2;

    // Read input from input.txt (x1: first line, x2: second line)
    FILE *file = fopen("input.txt", "r");
    if (file == NULL) {
        printf("Error opening file.\n");
        return 1;
    }

    fscanf(file, "%lf", &x1);
    fscanf(file, "%lf", &x2);

    fclose(file);

    double output = simple_function(x1, x2);
    printf("Output: %.2lf\n", output);

    //Write the output in a text file : output.txt 
    FILE *outputFile = fopen("output.txt", "w");

    fprintf(outputFile, "Output: %.2lf\n", output);
    fclose(outputFile);


    return 0;
}
