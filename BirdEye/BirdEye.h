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
#endif //定义描述平面上坐标的点的结构体

#ifndef __PIXEL_COORDINATE__
#define __PIXEL_COORDINATE__
struct pixel_coordinate
{
	double u;
	double v;
};
#endif //定义描述像素坐标系中的像素点的结构体 

#ifndef __GET_BIRDEYE__
#define __GET_BIRDEYE__
spatial_coordinate pixel2world(pixel_coordinate, double height, double yaw, double alpha, double beta);
pixel_coordinate world2pixel(spatial_coordinate, double height, double yaw, double alpha, double beta);
void getBirdEye(Mat, Mat &, double, double, double, double);
#endif