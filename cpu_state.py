"""
Course Number: ENGR 13300
Semester: Fall 2026

Description:
    Replace this line with a description of your program.

Assignment Information:
    Assignment:     CPU Framework
    Team ID:        ### - ## (e.g. LC1 - 01; for section LC1, team 01)
    Author:         Edison Zheng, zhen1058@purdue.edu
    Date:           11/26/2026

Contributors:
    Name, login@purdue [repeat for each]

    My contributor(s) helped me:
    [ ] understand the assignment expectations without
        telling me how they will approach it.
    [ ] understand different ways to think about a solution
        without helping me plan my solution.
    [ ] think through the meaning of a specific error or
        bug present in my code without looking at my code.
    Note that if you helped somebody else with their code, you
    have to list that person as a contributor here as well.

Academic Integrity Statement:
    I have not used source code obtained from any unauthorized
    source, either modified or unmodified; nor have I provided
    another student access to my code.  The project I am
    submitting is my own original work.
"""

import constants

#Register File Class
#Takes and stores operations, intermediate data, and result for future use
class RegisterFile:
    
    def __init__(self):
        #32 memory slots for each register file
        self.regs = [0]*32
        
    def read(self, index):
        return self.regs[index]
    
    def write(self, index, value):
        if index == 0: # writes to x0 is ignored
            return
        self.regs[index] = value & constants.mask32 # the result is masked because the processor needs it in 32 bits
        return

#Memory Class
#Stores the intructions and data the processor needs right now
class Memory:
    def __init__(self, size=4096):
        self.data = [0]*size
        
    def read_word(self, address):
        d = self.data
        #By convention, each byte is shifted left so that the lowest byte is at the lowest address
        return d[address] | d[address+1] << 8 | d[address+2] << 16 | d[address+3] << 24
    
    def write_word(self, address, value):
        value &= constants.mask32
        for i in range(4):
            self.data[address + i] = (self.data[address + i] >> (8*i)) & 0xFF
            
    def load_program(self, words):
        for i, word in enumerate(words):
            self.write_word(0+4*i, word)
            
#CPU Class
#Putting it all together creates a single CPU instance that is ready for use in the program
class CPU:
    def __init__(self, mem_size=4096):
        self.regs = RegisterFile()
        self.memory = Memory(mem_size)
        self.program_counter = 0
        
    def fetch(self):
        return self.memory.read_word(self.program_counter)