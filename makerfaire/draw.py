#!/usr/bin/env python

import cv
import math
from comms import DeltaComms
from kinematics import LinearDeltaKinematics
from kinematics import model


class PathGen:
    def __init__(self):
        self.move_height = 15
        self.draw_height = 0
        pass 

    def generatePath(self,img):
        self.img = img    
        path = []
        count = 0
        while True:
            current_pixel = self.getNextFreePixel()
            #if returns -1,-1 no more free pixels
            if current_pixel == (-1,-1,-1):
                return path
            path.append((current_pixel[0], current_pixel[1],self.move_height))
            path.append(current_pixel)
            
            cv.Set2D(self.img,current_pixel[1],current_pixel[0],(0.0,0.0,0.0))
            while True:
                count += 1
                current_pixel = self.getSurroundingPixel(current_pixel)
                if current_pixel == (-1,-1,-1):
                    prev = path[-1]
                    path.append((prev[0],prev[1],self.move_height))
                    break
                path.append(current_pixel)
                cv.Set2D(self.img,current_pixel[1],current_pixel[0],(0.0,0.0,0.0))
                print count
                

    def getSurroundingPixel(self,pixel):
        locations = [(-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0)]
        width = self.img.width
        height = self.img.height
        next_pixel = (-1,-1,-1)

        for location in locations:
            x_ok = False
            y_ok = False
            if (pixel[0] + location[0] >= 0) and (pixel[0] + location[0] < width):
                x_ok = True
            if (pixel[1] + location[1] >= 0) and (pixel[1] + location[1] < height):
                y_ok = True
            if x_ok and y_ok:
                check_pixel = cv.Get2D(self.img,pixel[1]+location[1],pixel[0]+location[0])
                if check_pixel[0] > 0:
                    return (pixel[0]+location[0],pixel[1]+location[1],self.draw_height)
        return next_pixel


    def getNextFreePixel(self):
        height = self.img.height
        width = self.img.width
        for y in range(height):
            for x in range(width):
                pixel = cv.Get2D(self.img,y,x)
                if pixel[0] >0:
                    return (x,y,self.draw_height)
        return (-1,-1,-1)
    





def main():
    cv.NamedWindow("w1", cv.CV_WINDOW_AUTOSIZE)
    pathgen = PathGen()
    camera_index =0 
    capture = cv.CaptureFromCAM(camera_index)
    kinematics = LinearDeltaKinematics(model)
    comms = DeltaComms()
    comms.microstep = 8 
    comms.delay = 0.0002

    while True:
        #global capture #declare as globals since we are assigning to them now
        #global camera_index
        in_img = cv.QueryFrame(capture)
        #in_img = cv.LoadImageM("moon.jpg")
        
        #in_img = cv.LoadImageM("lenna.bmp")
        #print in_img.width
        
        grey_img = cv.CreateImage(cv.GetSize(in_img), cv.IPL_DEPTH_8U, 1)
        cv.CvtColor(in_img,grey_img,cv.CV_RGB2GRAY)

        blur_img = cv.CreateImage(cv.GetSize(in_img), cv.IPL_DEPTH_8U, 1)
        cv.Smooth(grey_img,blur_img)

        result_img = cv.CreateImage(cv.GetSize(in_img), cv.IPL_DEPTH_8U, 1)
        cv.Canny(blur_img,result_img,100,220)
       

 
        
        cv.ShowImage("w1", result_img)
        c = cv.WaitKey(10)
        
        if(c==32): #the code for space
            print "Capturing"
            path = pathgen.generatePath(result_img)

            for i in range(len(path)):
                x,y,z = path[i]
                #condition the points
                path[i] = ((float(x)-160)/3.0,(float(y))/3.0,float(z))
            print path
        #    quit()

            start =(0,0,0)
            print "start"
            print start
            #quit()
            stop = path[0]

            test_img  = cv.CreateImage(cv.GetSize(in_img), cv.IPL_DEPTH_8U, 1)
            cv.SetZero(test_img)    


            for index in range(len(path)-1):
                


                x,y,z = path[index+1]
                t  = (int(float(x)+160.0/3),int(float(y)),-int(z))
                cv.Set2D(test_img,t[1],t[0],(255,0,0))
                cv.ShowImage("w1",test_img)
                cv.WaitKey(20)

                steps = kinematics.zzz_optimal_motion_creator(start,stop)
                print str(start) + " "+str(stop)
                print "---->>    " + str(index)
                comms.sendCommands(steps)
                start = stop
                stop = path[index+1]

            start = stop
            stop = (0,0,0)
            steps = kinematics.zzz_optimal_motion_creator(start,stop)
            print str(start) + " "+str(stop)
            comms.sendCommands(steps)
            while True:
                pass #noodle away
            #quit()





        if (c == 113): # the code for "q"
            quit()

        #    if(c=="n"): #in "n" key is pressed while the popup window is in focus
        #        camera_index += 1 #try the next camera index
        #        capture = cv.CaptureFromCAM(camera_index)
        #    if not capture: #if the next camera index didn't work, reset to 0.
        #        camera_index = 0
        #        capture = cv.CaptureFromCAM(camera_index)



if __name__ == "__main__":
    main()
