#include <iostream>
#include <io.h>
#include <stdlib.h>
#include <string>
#include <vector>
#include <opencv2/opencv.hpp>
#include <opencv2/imgproc/types_c.h>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgcodecs.hpp>

using namespace std;
using namespace cv;

//******************************************************************
//*从存放文件的路径中读取文件的绝对路径，没有递归搜索的能力
//******************************************************************
void GetAllFiles(string path, vector<string>& files)
{

	intptr_t hFile = 0;
	struct _finddata_t fileinfo;
	string p;

	if ((hFile = _findfirst(p.assign(path).append("/*").c_str(), &fileinfo)) != -1)
	{
		do {
			if ((fileinfo.attrib != _A_SUBDIR))
			//查询到的对象不是子目录，那就是文件对象
			{
				files.push_back(p.assign(path).append("/").append(fileinfo.name));
				//把绝对路径加到 vector 对象中
			}
		} while (_findnext(hFile, &fileinfo) == 0);
		//还有对象，暂时不跳出循环

		_findclose(hFile);
	}
}

void YUV2JPG(string inputFileName, string savepath) 
{
	int iWidth, iHeight, iImageSize;
	iWidth = 1920;
	iHeight = 1056;
	iImageSize = iWidth * iHeight * 3 / 2;
	
	FILE * fpln;
	fpln = fopen(inputFileName.data(), "rb+");
	//读取 yuv 文件的内容，应该是暂时获得了一个指针，还没有开始读取数据
	if (fpln == NULL) {
		printf("read yuv error.\n");
	}

	cv::Mat yuvImg;
	cv::Mat rgbImg(iHeight, iWidth, CV_8UC3);
	yuvImg.create(iHeight * 3 / 2, iWidth, CV_8UC1);
	//之所以是 3/2 是跟 YUV 格式有关， NV21 也就是属于 YUV420 的一种格式
	
	unsigned char *pYUVbuf = new unsigned char[iImageSize];
	fread(pYUVbuf, iImageSize * sizeof(unsigned char), 1, fpln);
	//fread 才是真正的读取数据到缓存 buffer 中
	memcpy(yuvImg.data, pYUVbuf, iImageSize * sizeof(unsigned char));
	cv::cvtColor(yuvImg, rgbImg, CV_YUV2RGBA_NV21);

	//imshow("test", rgbImg);
	//waitKey(1000);

	imwrite(savepath, rgbImg);
}

int main() {
	string fp_front = "D:/GitFile/roadlane-detect-cpp/yuv/front/";
	string fp_rear = "D:/GitFile/roadlane-detect-cpp/yuv/rear";
	char sp_front[128], sp_rear[128];
	
	vector<string> list1, list2;
	GetAllFiles(fp_front, list1);
	GetAllFiles(fp_rear, list2);
	
	for (int i = 0; i < list1.size(); i++)
	{	
		sprintf(sp_front, "D:/GitFile/roadlane-detect-cpp/jpg/front/%d.jpg", i);
		YUV2JPG(list1.at(i), sp_front);
	}
	for (int i = 0; i < list2.size(); i++)
	{
		sprintf(sp_rear, "D:/GitFile/roadlane-detect-cpp/jpg/rear/%d.jpg", i);
		YUV2JPG(list2.at(i), sp_rear);
	}
	return 0;
}