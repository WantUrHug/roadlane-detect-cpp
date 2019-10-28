#include <string>
#include <iostream>
#include <opencv2/opencv.hpp>
#include <math.h>
#include "BirdEye.h"

#define IMAGE_WIDTH 1920
#define IMAGE_HEIGHT 1056	
	
using namespace std;
using namespace cv;

spatial_p pixel2world(pixel_p point, float height, float yaw, float alpha, float beta)
{
	spatial_p output;
	output.y = height * tan(yaw - atan(2 * point.u / (IMAGE_WIDTH - 1)*tan(alpha)));
	output.x = sqrt(pow(height, 2) + pow(output.y, 2)) * 2 * point.v / (IMAGE_HEIGHT - 1)* tan(beta) / sqrt(1 + pow(2 * point.u / (IMAGE_WIDTH - 1) * tan(alpha),2));
	return output;
}

pixel_p world2pixel(spatial_p point, float height, float yaw, float alpha, float beta)
{

}

Mat GetBirdEye(Mat input, float height, float yaw, float alpha)
{

}

