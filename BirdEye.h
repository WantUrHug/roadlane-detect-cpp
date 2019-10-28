#pragma once

#ifndef __SPATIAL_COORDINATE__
#define __SPATIAL_COORDINATE__
typedef struct spatial_coodinate
{
	float x;
	float y;
}spatial_p; 
#endif //定义描述平面上坐标的点的结构体

#ifndef __PIXEL_COORDINATE__
#define __PIXEL_COORDINATE__
typedef struct pixel_coordinate
{
	int u;
	int v;
}pixel_p;
#endif //定义描述像素坐标系中的像素点的结构体 
