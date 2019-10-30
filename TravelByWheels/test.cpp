#include <iostream>
#include <vector>
#include <string>
#include <stdlib.h>
#include <math.h>

#include "TravelByWheels.h"
#define MAX_LINE 1024

using namespace std;

int main()
{
	char log_file[] = "1572417097918.log";
	FILE *fp;
	fopen_s(&fp,log_file, "r");
	int len;
	char buf[MAX_LINE];//»º³åÇø
	while (fgets(buf, MAX_LINE, fp) != NULL)
	{
		len = strlen(buf);
		buf[len - 1] = '\0';
		printf("%s %d \n", buf, len - 1);
	}
	return 0;
	system("pause");
}