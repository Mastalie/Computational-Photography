#!/usr/bin/python
#
# simple python script to capture a video sequence
# input[0] is the sensor-id
# input[1] is the number of frames
# input[2] is the frame rate
#


import sys
import atexit
import subprocess

def printHelp():
    print("grab video at various frame rates")
    print("---------------------------------")
    print("to run type grabVideo.py sensor-id number-of-frames frame-rate")
    print("--help or -h prints help message and exits")

def main():
        inputs=sys.argv[1:]
        if len(inputs)==3:
                cmd="gst-launch-1.0 -e nvcamerasrc intent=3 sensor-id="
                cmd=cmd+str(inputs[0])+" num-buffers="+str(inputs[1])
                cmd=cmd+""" fpsRange=\""""+str(inputs[2])+" "+str(inputs[2])+"""\""""
                cmd=cmd+" ! 'video/x-raw(memory:NVMM), width=(int)3940, height=(int)2160, format=(string)I420, "
                cmd=cmd+"framerate=(fraction)"+str(inputs[2])+"/1' ! nvvidconv flip-method=2 ! 'video/x-raw(memory:NVMM),"
                cmd=cmd+"format=(string)I420' ! omxh264enc ! 'video/x-h264, "
                cmd=cmd+"stream-format=(string)byte-stream' ! filesink location=grabVid.h264"
                #print(cmd)
                subprocess.call(cmd,shell=True)
        else:
                printHelp()


if __name__ == '__main__':
        main()
