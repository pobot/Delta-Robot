#!/usr/bin/env python

def main():
   reader = GCodeReader()
   steps = reader.processfile("test_file.ngc")
   print steps


class GCodeReader:

    def processfile(self,filename):
        f = open(filename)

        modes = ["fast","slow"]
        mode = modes[0]

        target = [0,0,0]

        steps =[]
        while True:
            text = f.readline().split() 
            if text == []: return steps
            new_move = False

            for command in text:
                if command.startswith("X"):
                        target[0] = float(command[1:])
                        new_move = True
                if command.startswith("Y"):
                        target[1] = float(command[1:])
                        new_move = True
                if command.startswith("Z"):
                        target[2] = float(command[1:])
                        new_move = True
                if command.startswith("G"):
                    if command == "G0":
                        mode = modes[0]
                    if command == "G1":
                        mode = modes[1]
                    new_move = True
            
            if new_move:
                #print mode + " " + str(target)
                steps.append(tuple(target))

                
if __name__ == "__main__":
    main()
