#include <stdio.h>

void printing()
{
    int c;
    do
    {
        c = getchar();
        printf("%c",c);
    }
    while ((c != EOF) && (c != '\n'));
}

void main()
{
    setvbuf(stdout, NULL, _IONBF, 0);
    printing();
    printing();
}
