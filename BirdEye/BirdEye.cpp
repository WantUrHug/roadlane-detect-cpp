#include <string>
#include <vector>
#include <iostream>
#include <math.h>
#include "BirdEye.h"

#define IMAGE_WIDTH 3456.0
#define IMAGE_HEIGHT 3456.0
	
#define ROI_U_MIN 1.0
#define ROI_U_MAX 3454.0
#define ROI_V_MIN 1.0
#define ROI_V_MAX 3454.0

//输出的图片尺寸
#define OUTPUT_WIDTH 960.0
#define OUTPUT_HEIGHT 640.0

using namespace std;
using namespace cv;

spatial_coordinate pixel2world(pixel_coordinate point, double height, double yaw, double alpha, double beta)
{
	spatial_coordinate output;
	output.y = height * tan(yaw - atan(2 * point.u / (IMAGE_HEIGHT - 1)*tan(alpha)));
	output.x = sqrt(pow(height, 2) + pow(output.y, 2)) * 2 * point.v / (IMAGE_WIDTH - 1) * tan(beta) / sqrt(1 + pow(2 * point.u / (IMAGE_HEIGHT - 1) * tan(alpha),2));
	return output;
}

pixel_coordinate world2pixel(spatial_coordinate point, double height, double yaw, double alpha, double beta)
{
	pixel_coordinate output;
	output.u = (IMAGE_WIDTH - 1) / 2 / tan(alpha)*tan(yaw - atan(point.y / height));
	output.v = sqrt(1 + pow((2 * output.u / (IMAGE_WIDTH - 1) * tan(alpha)), 2)) * point.x / sqrt(pow(height, 2) + pow(point.y, 2))*(IMAGE_HEIGHT - 1) / 2 / tan(beta);
	return output;
}

void getBirdEye(Mat input, Mat &output, double height, double yaw, double alpha, double beta)
{
	if (input.empty()) {
		cout << "Input coun't be empty." << endl;
		return;
	}

	//之所以需要翻转时因为我们这个算法，小孔成像点是在物和像之间，所以在输出时也要加上对 output 的翻转
	flip(input, input, 0);

	pixel_coordinate left_up = { (IMAGE_HEIGHT - 1) / 2 - ROI_V_MIN, ROI_U_MIN - (IMAGE_WIDTH - 1) / 2 };
	pixel_coordinate right_down = { (IMAGE_HEIGHT - 1)/ 2 - ROI_V_MAX, ROI_U_MAX - (IMAGE_WIDTH - 1) / 2 };
	pixel_coordinate left_down = { (IMAGE_HEIGHT - 1) / 2 - ROI_V_MAX, ROI_U_MIN - (IMAGE_WIDTH - 1) / 2 };
	pixel_coordinate right_up = { (IMAGE_HEIGHT - 1)/ 2 - ROI_V_MIN, ROI_U_MAX - (IMAGE_WIDTH - 1)/ 2 };
	spatial_coordinate right_earlier, left_farther;
	right_earlier = pixel2world(left_up, height, yaw, alpha, beta);
	left_farther = pixel2world(right_down, height, yaw, alpha, beta);
	cout << "right_earlier.x ="<<right_earlier.x << ", right_earlier.y =" << right_earlier.y << endl;
	cout << "left_farther.x ="<<left_farther.x << ", left_farther.y =" << left_farther.y << endl;
	spatial_coordinate left_earlier, right_farther;
	left_earlier = pixel2world(right_up, height, yaw, alpha, beta);
	right_farther = pixel2world(left_down, height, yaw, alpha, beta);
	cout << "left_earlier.x ="<<left_earlier.x << ", left_earlier.y =" << left_earlier.y << endl;
	cout << "right_farther.x ="<<right_farther.x << ", right_farther.y =" << right_farther.y << endl;

	double x_max, x_min, y_max, y_min;
	y_min = right_earlier.y;
	x_max = left_farther.x;
	x_min = -x_max;
	y_max = left_farther.y;
	

	double step_y, step_x;
	step_y = (y_max - y_min) / OUTPUT_HEIGHT;
	step_x = 2 * x_max / OUTPUT_WIDTH;

	double x, y;

	if (input.channels() == 3) {
		//是三通道的 RGB 彩色图片.
		//Mat output = Mat(OUTPUT_HEIGHT, OUTPUT_WIDTH, CV_8UC3);
		output = Mat(OUTPUT_HEIGHT, OUTPUT_WIDTH, CV_8UC3);
		y = y_min;
		int cnt = 0;
		for (int i = 0; i < output.rows; i++)
		{
			x = x_min;
			for (int j = 0; j < output.cols; j++) {
				spatial_coordinate tmp_point = { x, y };
				pixel_coordinate pixel_point = world2pixel(tmp_point, height, yaw, alpha, beta);
				double u, v, uu, vv;
				u = pixel_point.u;
				v = pixel_point.v;
				uu = v + IMAGE_WIDTH / 2;
				vv = IMAGE_HEIGHT / 2 - u;
				//cout << "uu=" << uu << ",vv=" << vv << endl;
				if ((uu < 1 || uu >= IMAGE_WIDTH - 1) || (vv < 1 || vv >= IMAGE_HEIGHT - 1)) {
					Vec3b val = { 0, 0 ,0 };
					output.at<Vec3b>(i, j) = val;
					x += step_x;
					cnt++;
					continue;
				}

				int u1, u2, v1, v2;
				u1 = int(uu); u2 = int(uu + 1);
				v1 = int(vv); v2 = int(vv + 1);
				double delta_u, delta_v;
				delta_u = uu - u1; delta_v = vv - v1;
				//cout << "u1 = " << u1 << "," << "v1 = " << v1 << endl;
				Vec3b val = { 0, 0, 0 };
				//cout << "three channels"<<endl;
				for (int k = 0; k < 3; k++)
				{
					double v;
					v = (double(input.at<Vec3b>(v1, u1)[k]) * (1 - delta_u) * (1 - delta_v) +
						double(input.at<Vec3b>(v1, u2)[k]) * delta_u * (1 - delta_v) +
						double(input.at<Vec3b>(v2, u2)[k]) * delta_u * delta_v +
						double(input.at<Vec3b>(v2, u1)[k]) *(1 - delta_u) * delta_v);
					
					if (v > 255) {
						val[k] = 255; //cout << "1" << endl;
					}
					else {
						val[k] = unsigned(v); //cout << "2" << endl;
					}
					//cout << "1" ;
				}
				output.at<Vec3b>(i, j) = val;
				x += step_x;
				cnt++;
			}
			y += step_y;
		}
		//return output;
		cout << "final x = " << x << ", final y = " << y << endl;
		cout << "cnt=" << cnt << endl;
		cout << "960x640=" << 960 * 640 << endl;
		flip(output, output, 0);
	}
	//Mat output;
	//return output;
}

