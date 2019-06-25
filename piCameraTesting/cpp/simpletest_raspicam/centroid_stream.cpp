
#include <chrono>
#include <iostream>
#include <string>
#include <raspicam/raspicam_cv.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/core/core.hpp>
using namespace std; 


string type2str(int type) {
  string r;

  uchar depth = type & CV_MAT_DEPTH_MASK;
  uchar chans = 1 + (type >> CV_CN_SHIFT);

  switch ( depth ) {
    case CV_8U:  r = "8U"; break;
    case CV_8S:  r = "8S"; break;
    case CV_16U: r = "16U"; break;
    case CV_16S: r = "16S"; break;
    case CV_32S: r = "32S"; break;
    case CV_32F: r = "32F"; break;
    case CV_64F: r = "64F"; break;
    default:     r = "User"; break;
  }

  r += "C";
  r += (chans+'0');

  return r;
}

class HSVTrackbars {
    public:
    HSVTrackbars(): winName("HSV Vals"){
        cv::namedWindow(winName, cv::WINDOW_AUTOSIZE);
    
        cv::createTrackbar("H max", winName, &hmax, 255);
        cv::createTrackbar("H min", winName, &hmin, 255);
        cv::createTrackbar("S max", winName, &smax, 255);
        cv::createTrackbar("S min", winName, &smin, 255);
        cv::createTrackbar("V max", winName, &vmax, 255);
        cv::createTrackbar("V min", winName, &vmin, 255);
    }

    cv::Scalar getMax() {
        return cv::Scalar( cv::getTrackbarPos("H max", winName),
                           cv::getTrackbarPos("S max", winName),
                           cv::getTrackbarPos("V max", winName) );
    }
    cv::Scalar getMin() {
        return cv::Scalar( cv::getTrackbarPos("H min", winName),
                           cv::getTrackbarPos("S min", winName),
                           cv::getTrackbarPos("V min", winName) );

    }

    private:
    int hmax, hmin, smax, smin, vmax, vmin;
    std::string winName;


};

void maskHSVOrig(const cv::Mat &image, const cv::Scalar &max, const cv::Scalar &min, cv::Mat &mask) {
    cv::Mat blurImage;
    cv::GaussianBlur(image, blurImage, cv::Size(11,11), 0);
    
    cv::Mat hsvImage;
    cv::cvtColor(image, hsvImage, cv::COLOR_BGR2HSV);

    // cv::Mat hsvImage[3];
    // cv::split(image, hsvImage);
    // 
    // cv::inRange(hsvImage[0], cv::Scalar(60), cv::Scalar(120), mask);

    cv::inRange(hsvImage, min, max, mask);
}

int main ( int argc,char **argv ) {
    bool showImages = false;
   
    raspicam::RaspiCam_Cv Camera;
    cv::Mat image, mask;
    
    //set camera params
    Camera.set( CV_CAP_PROP_FORMAT, CV_8UC3 );
    Camera.set( CV_CAP_PROP_FRAME_WIDTH, 640);
    Camera.set( CV_CAP_PROP_FRAME_HEIGHT, 480);
    Camera.set( CV_CAP_PROP_GAIN, 100);
    Camera.set( CV_CAP_PROP_FPS, 15);
    Camera.set( CV_CAP_PROP_WHITE_BALANCE_RED_V, -1);
    Camera.set( CV_CAP_PROP_WHITE_BALANCE_BLUE_U, -1);

    HSVTrackbars trackbars;

    //Open camera
    cout<<"Opening Camera..."<<endl;
    if (!Camera.open()) {cerr<<"Error opening the camera"<<endl;return -1;}
    //Start capture
    
    using Clock = std::chrono::steady_clock;

    auto start = Clock::now();
    while (true) {
        Camera.grab();
        Camera.retrieve ( image);

        //string ty = type2str(image.type());
        //std::cout << ty << std::endl;
        
        cv::Scalar max = trackbars.getMax();
        cv::Scalar min = trackbars.getMin();
        maskHSVOrig(image, max, min, mask);
        if (showImages) {
            cv::imshow("raw",image);
            cv::imshow("mask", mask);

            cv::waitKey(1);
            if (0 != 0) {
                break;
            }
        }
        
        // use this to print fps later
        //if ( i%5==0 )  cout<<"\r captured "<<i<<" images"<<std::flush;
        auto end = Clock::now();
        std::chrono::duration<double> dur = end - start;
        start = end;

        double freq = 1.0 / dur.count();
        std::cout << freq << " fps" << std::endl;
    }
    
    cout<<"Stop camera..."<<endl;
    Camera.release();
    
}
