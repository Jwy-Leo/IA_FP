import numpy as np
import random
from cfg import *
# 3. Taxi agent : need to finish the cost function
# 5. Taxi need update location


# Taxi not work
class taxi():
    # Speed=30km/hour
    Speed = 30
    charge_rate_per_km = 60
    gas_cost_per_km = 4

    def __init__(self,
                 worktime_begin,
                 worktime_end,
                 x,
                 y):
        self.WB = worktime_begin
        self.WE = worktime_end
        self.time_s = []
        self.locationx = x
        self.locationy = y
        self.profit = 0

        self.carry = False
        self.costumer = None

        if self.WB > self.WE:
            for i in range(self.WB, 24, 1):
                self.time_s.append(i)
            for i in range(0, self.WE, 1):
                self.time_s.append(i)
        else:
            self.time_s = [i for i in range(self.WB, self.WE, 1)]

    def cost(self, time_step, costumer_infomation):
        if _SIMULATION_MODE == "MINUTE":
            time_step = (time_step // 60) % 24
        elif _SIMULATION_MODE == "SECOND":
            time_step = (time_step // 60 // 60) % 24
        else:
            pass
        if self.IF_WORK(time_step):
            if not self.carry:
                print("work and caculate")
            else:
                return _Default_Value
        else:
            return _Default_Value

        '''
        chargeable distance * (charge_rate_per_kilometer)-total_traveling_distance * gas-cost-per-kilometer 
        - payment_to_the_auction

        The winning payment = 
        30% *(60 - 4)* requested_distance - {lowest bidding-price or second lowest bidding price}

        '''

    def getworktime(self):
        return self.WB, self.WE

    def IF_WORK(self, time):
        if time in self.time_s:
            return True
        else:
            return False

    def profit(self):
        return self.profit

    def assign_costumer(self, time_step, costumer):
        # self.profit+=
        self.carry = True
        # print("Using the Hour rule")
        # finish_time_step=time_step+1.*costumer[4]/self.Speed
        # self.costumer = (finish_time_step % 24, costumer)
        print("Using the Minute rule")
        finish_time_step = time_step[1] + 1. * costumer[4] / self.Speed / 60
        self.costumer = ((finish_time_step // 60 + time_step[0]) % 24, finish_time_step % 60, costumer)

    def update_taxi(self, time_step):
        '''
        :param time_step:
        :return location
        Todo :
        1.Based on self.costumer information and planning path to run the location
        2.If arrive carry will False
        '''
        pass