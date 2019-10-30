#pragma once
#include <vector>
#include <opencv2/opencv.hpp>
using namespace cv;

#ifndef __SPATIAL_COORDINATE__
#define __SPATIAL_COORDINATE__
struct spatial_coordinate
{
	double x;
	double y;
}; 
#endif //��������ƽ��������ĵ�Ľṹ��

#ifndef __PIXEL_COORDINATE__
#define __PIXEL_COORDINATE__
struct pixel_coordinate
{
	double u;
	double v;
};
#endif //����������������ϵ�е����ص�Ľṹ�� 

#ifndef __GET_BIRDEYE__
#define __GET_BIRDEYE__
spatial_coordinate pixel2world(pixel_coordinate, double height, double yaw, double alpha, double beta);
pixel_coordinate world2pixel(spatial_coordinate, double height, double yaw, double alpha, double beta);
void getBirdEye(Mat, Mat &, double, double, double, double);
#endif