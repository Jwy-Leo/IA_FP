import numpy as np
import random
from cfg import *
# 1. Map :need to build
# 2. costumer_generator :Based on Map calculate candidate of dst by distance information
# 3. Taxi agent : need to finish the cost function
# 4. company:need to finish bidding
# 5. Taxi need update location


# Taxi not work
_Default_Value=-1
_SIMULATION_MODE="MINUTE" #{"HOUR","MINUTE","SECOND"}

class costumer_generator():
    def __init__(self,
                 average_call_lamda=0,
                 Map=None):
        self.average_call_lamda = average_call_lamda
        self.c_sum=0
        '''
        if Map is None:
            raise Exception("No Map for generator reference")
        self.Map=Map
        '''
    def change_lamda(self, timestep):
        if _SIMULATION_MODE=="HOUR":
            scale = 1
        elif _SIMULATION_MODE=="MINUTE":
            scale = 1.0 / 60.0
        else:
            scale = 1.0 / 3600.0
        # minute scale need to divide by 60
        if (timestep >= 7 and timestep < 9) or (timestep >= 17 and timestep < 19):
            self.average_call_lamda = 1/(3.*scale)
        elif (timestep >= 9 and timestep < 17) or (timestep >= 19 and timestep < 23):
            self.average_call_lamda = 1/(2.*scale)
        else:
            self.average_call_lamda = 1/(1.*scale)
    def generate_costumer(self,LocationX,LocationY):
        number=random.expovariate(self.average_call_lamda)
        self.c_sum+=number
        if self.c_sum>1:
            self.c_sum-=1
            return [self.costumer_infomation(LocationX, LocationY) for i in range(int(1))]
        return [self.costumer_infomation(LocationX,LocationY) for i in range(int(number))]
    def costumer_infomation(self,LocationX,LocationY):
        x = LocationX
        y = LocationY
        distance=self.normal_distrubution()
        '''
        candidate=self.search_candidatex(x,y,distance)
        item=candidate[random.randint(0,len(candidate)-1)]
        '''
        item=None
        #dst_x = 0
        #dst_y = 0
        #vert1 = item[0]
        #vert2 = item[1]
        #d_long = item[2]
        wait_time = 5
        return (x, y, wait_time,item,distance)
    def normal_distrubution(self):
        # the
        mean = 2
        std_deviation=1.5
        def Box_Muller_normal_method(sigma,mu):
            import sys
            import math
            import random
            epsilon=sys.float_info.min
            u1=0
            while u1<=epsilon:
                u1 =random.uniform(0, 32767)/ 32767
                u2 =random.uniform(0, 32767)/ 32767
            z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2*math.pi * u2)
            return z*sigma+mu
        return abs(np.random.normal(mean,std_deviation,1))
    def search_candidate(self,x,y,distance):
        candidate=[]
        #item=(v1,v2,d_long)

        return candidate