import numpy as np
import random
from cfg import *
# 4. company:need to finish bidding

class company():
    def __init__(self,
                 company_location):
        # (x,y)
        self.company_location = company_location
        self.taxi_list=[]
        #self.taxi_work_list=None
    def register_taxi(self,taxi):
        self.taxi_list.append(taxi)
        '''
        if not isinstance(self.taxi_work_list,np.ndarray):
            self.taxi_work_list =np.array([[taxi.getworktime()[0]],[taxi.getworktime()[1]]]).transpose()
        else:
            self.taxi_work_list = np.concatenate([self.taxi_work_list,np.array([[taxi.getworktime()[0]],[taxi.getworktime()[1]]]).transpose()],axis=0)
        '''

    def bidding(self,time_step,costumer_list):
        # ???????????If we need to merge the route of costumer ???????????
        # Get all agent cost
        cost_array=_Default_Value*np.ones(len(self.taxi_list),len(costumer_list))
        i=0
        for agent in self.taxi_list:
            cost=[]
            for costumer in costumer_list:
                cost.append(agent.cost(time_step,costumer))
                cost_array[i,:]=np.array(cost)
            i=i+1
        # Assign the task
        pass