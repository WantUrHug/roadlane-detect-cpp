#include <string>
#include <stdlib.h>
#include <vector>
#include <iostream>
#include <opencv2/opencv.hpp>
#include <math.h>
#include "BirdEye.h"

using namespace std;
using namespace cv;

int main() {
	string path = "D:\\GitFile\\roadlane-segmentation\\imgs\\train\\data\\00002.png";
	string test1 = "test02.jpg";
	Mat im = imread(test1);
	//cout << im.channels() << endl;
	double height = 0.328;
	double yaw = 45 * CV_PI / 180;
	double alpha = 45/2 * CV_PI / 180;
	double beta = 45/2 * CV_PI / 180;
	Mat output;
	spatial_coordinate p1;
	pixel_coordinate p2 = { 100,100 };
	p1 = pixel2world(p2, height, yaw, alpha, beta);
	pixel_coordinate p3 = world2pixel(p1, height, yaw, alpha, beta);
	//cout << tan(90);
	//cout << p3.u << "," << p3.v << endl;
	getBirdEye(im, output, height, yaw, alpha, beta);
	imwrite("output.jpg", output);
	system("pause");
}