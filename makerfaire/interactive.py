#!/usr/bin/env python

import operator
import math
from comms import DeltaComms
import pygame
import sys


class LinearDeltaKinematics:

    def __init__(self,model):
        self.model = model

    def xyz_to_zzz(self,(x,y,z)):
        target_xy = (x,y)
        z_height = z

        #calculate the position of the head joints
        head_position = []
        for j in self.model["head"]:
            head_position.append(tuple([x+y for x,y in zip(target_xy,j)]))
            #head_position.append(tuple(map(operator.add,target_xy,j)))
        head_position = tuple(head_position)
#        print head_position


        #calculate the z values
        zzz = []
        for index,body_joint in enumerate(self.model["body"]):
            delta_x = body_joint[0] - head_position[index][0]
            delta_y = body_joint[1] - head_position[index][1]
            z = pow(self.model["rods"][index],2) - pow(delta_x,2) -pow(delta_y,2)
            z = math.sqrt(z)
            zzz.append(z)

        #add the z_offset to all z values
        zzz = tuple([-z_height - z  for z in zzz])
        #Alternate map + lambda function way for the giggles
        #zzz = tuple(map(lambda x: x+z_offset,zzz))
        return zzz

    def float_range(self,start,stop,step):
        """A utility generator to produce ranges with float intervals"""
        count = start
        if step >0:
            while count<stop:
                yield count
                count+= step
        if step <0:
            while count>stop:
                yield count
                count+= step

    def line_3d_generator(self,start,stop,step=0.1):
        for a in self.float_range(0,1,step):
            x = start[0]+a*(stop[0]-start[0])
            y = start[1]+a*(stop[1]-start[1])
            z = start[2]+a*(stop[2]-start[2])
            yield(x,y,z)

    def line_step_generator(self,start,stop,step=0.1):
        line = self.line_3d_generator(start,stop,step)
        prev = self.xyz_to_zzz(line.next())
        for pos in line:
            pos = self.xyz_to_zzz(pos)
            diff = tuple([pos[index]-prev[index] for index in range(3)])
            prev = pos
            yield diff

    def zzz_optimal_motion_creator(self,start,stop):
        stepable = False
        step = 1.0
        magnitude = math.sqrt(pow(start[0]-stop[0],2)+pow(start[1]-stop[1],2)+pow(start[2]-stop[2],2))
        print "Travel distance: "+str(magnitude)
        while True:
            for zzz_step in self.line_step_generator(start,stop,step):
                if zzz_step[0]>self.model["z_stepsize"] or zzz_step[0]<-self.model["z_stepsize"]:
                    stepable = False
                    break
                elif zzz_step[1]>self.model["z_stepsize"] or zzz_step[1]<-self.model["z_stepsize"]:
                    stepable = False
                    break
                elif zzz_step[2]>self.model["z_stepsize"] or zzz_step[2]<-self.model["z_stepsize"]:
                    stepable = False
                    break
                else:
                    stepable = True
            
            if stepable:
                break 
            #step = step-0.001
            step = step/1.2
        
        acc = (0.0,0.0,0.0)
        prev = (0,0,0)
        step_commands =[]
        for move in self.line_step_generator(start,stop,step):
            acc = tuple([acc[i]+move[i] for i in range(3)])
            current = (int(acc[0]/self.model["z_stepsize"]),int(acc[1]/self.model["z_stepsize"]),int(acc[2]/self.model["z_stepsize"]))
            step_commands.append(tuple([current[i]-prev[i] for i in range(3)]))
            prev= current
        print "Number of steps: "+str(len(step_commands))
        print "Approximate Steps Per mm: "+str(magnitude/len(step_commands))
        return step_commands
        
    def zzz_motion_creator(self,start,stop,step = 0.001):
        magnitude = math.sqrt(pow(start[0]-stop[0],2)+pow(start[1]-stop[1],2)+pow(start[2]-stop[2],2))
        print "Travel distance: "+str(magnitude)
        
        acc = (0.0,0.0,0.0) #accumulator
        prev = (0,0,0)
        step_commands =[]
        for move in self.line_step_generator(start,stop,step):
            acc = tuple([acc[i]+move[i] for i in range(3)])
            current = (int(acc[0]/self.model["z_stepsize"]),int(acc[1]/self.model["z_stepsize"]),int(acc[2]/self.model["z_stepsize"]))
            step_commands.append(tuple([current[i]-prev[i] for i in range(3)]))
            prev= current
        print "Number of steps: "+str(len(step_commands))
        print "Approximate Steps Per mm: "+str(magnitude/len(step_commands))
        return step_commands
        

model = {\
    "body":((0,171.6581),(148.6603,-85.829),(-148.6603,-85.829)),\
    "head":((0,42),(36.3731,-21),(-36.3731,-21)),\
#    "rods":(250,245,255),\
#    "rods":(255,250,245),\
#    "rods":(245,255,250),\
    "rods":(245,245,245),\
    "z_stepsize":(25.0*2.5)/(200.0*8),\
    "z_offsets":(0,2,0),\
    "z_maximum":0,\
    "z_minimum":0\
}




def main():
    #manual_control()

    kinematics = LinearDeltaKinematics(model)
    comms = DeltaComms()
    comms.microstep = 8
    comms.delay = 0.00001


    pygame.init()
    size = width,height = 800,640
    screen = pygame.display.set_mode(size)
   
    current = [0,0,0]
    target =  [0,0,0]

#    font = pygame.font.Font(None, 36)
#    text = font.render("Click and Drag in the Black Square", 1, (10, 10, 10))
#    textpos = text.get_rect()
#    textpos.centerx = background.get_rect().centerx
#    background.blit(text, textpos)


 
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if pygame.mouse.get_pressed()[0]:
            mouse = pygame.mouse.get_pos()
            target[0] = float(mouse[0]-width/2)/10.0
            target[1] = float(mouse[1]-height/2)/10.0


        if pygame.mouse.get_pressed()[2]:
            print "changing z"
            if target[2] == 0:
                target[2] = 10

            elif target[2] == 10:
                target[2] = 0

        print target[2]
        steps = kinematics.zzz_optimal_motion_creator(current,target)
        comms.sendCommands(steps)
        current = list(target)

#        print target


    #start =xyz[0]
    #stop = (0,0,0)
    #for index in range(len(xyz)-1):
    #    stop = xyz[index+1]
    #    steps = kinematics.zzz_optimal_motion_creator(start,stop)
    #    print str(start) + " "+str(stop)
    #    comms.sendCommands(steps)
    #    start = stop
    #stop = (0,0,0)
    #steps = kinematics.zzz_optimal_motion_creator(start,stop)
    #comms.sendCommands(steps)
    #quit()
            
            

if __name__ == "__main__":
    main()
