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
//*�Ӵ���ļ���·���ж�ȡ�ļ��ľ���·����û�еݹ�����������
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
			//��ѯ���Ķ�������Ŀ¼���Ǿ����ļ�����
			{
				files.push_back(p.assign(path).append("/").append(fileinfo.name));
				//�Ѿ���·���ӵ� vector ������
			}
		} while (_findnext(hFile, &fileinfo) == 0);
		//���ж�����ʱ������ѭ��

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
	//��ȡ yuv �ļ������ݣ�Ӧ������ʱ�����һ��ָ�룬��û�п�ʼ��ȡ����
	if (fpln == NULL) {
		printf("read yuv error.\n");
	}

	cv::Mat yuvImg;
	cv::Mat rgbImg(iHeight, iWidth, CV_8UC3);
	yuvImg.create(iHeight * 3 / 2, iWidth, CV_8UC1);
	//֮������ 3/2 �Ǹ� YUV ��ʽ�йأ� NV21 Ҳ�������� YUV420 ��һ�ָ�ʽ
	
	unsigned char *pYUVbuf = new unsigned char[iImageSize];
	fread(pYUVbuf, iImageSize * sizeof(unsigned char), 1, fpln);
	//fread ���������Ķ�ȡ���ݵ����� buffer ��
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