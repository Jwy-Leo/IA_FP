import numpy as np
import random
# 1. Map :need to build
# 2. costumer_generator :Based on Map calculate candidate of dst by distance information
# 3. Taxi agent : need to finish the cost function
# 4. company:need to finish bidding
# 5. Taxi need update location


# Taxi not work
_Default_Value=-1
_SIMULATION_MODE="MINUTE" #{"HOUR","MINUTE","SECOND"}
class Map():
    def __init__(self,info_dict):
        pass
    def update_map(self,src,dst,d_long,direction):
        pass
    def shortest_path(self,src,dst):
        if isinstance(dst,tuple):
            pass
        else:
            pass
    def shortest_path_method_tuple(self,src,dst):
        pass
    def shortest_path_method_node(self,src,dst):
        pass
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
            timestep = (timestep // 60) % 24
        else:
            scale = 1.0 / 3600.0
        # minute scale need to divide by 60
        if (timestep >= 7 and timestep < 9) or (timestep >= 17 and timestep < 19):
            self.average_call_lamda = 1/(3.*scale)
        elif (timestep >= 9 and timestep < 17) or (timestep >= 19 and timestep < 23):
            self.average_call_lamda = 1/(2.*scale)
        else:
            self.average_call_lamda = 1/(1.*scale)
    def generate_costumer(self,LocationX,LocationY,timestep):
        number=random.expovariate(self.average_call_lamda)
        self.c_sum+=number
        if self.c_sum>1:
            self.c_sum-=1
            return [self.costumer_infomation(LocationX, LocationY,timestep) for i in range(int(1))]
        return [self.costumer_infomation(LocationX,LocationY,timestep) for i in range(int(number))]
    def costumer_infomation(self,LocationX,LocationY,timestep):
        src_loc= (LocationX,LocationY,0)
        distance=self.normal_distrubution()
        '''
        candidate=self.search_candidatex(x,y,distance)
        dst_loc=candidate[random.randint(0,len(candidate)-1)]
        '''
        dst_loc=None
        wait_time = timestep+5
        #dst_x = 0
        #dst_y = 0
        #vert1 = item[0]
        #vert2 = item[1]
        #d_long = item[2]
        return (src_loc,dst_loc,wait_time,distance)
    def generate_costumer(self,verticle,timestep):
        number=random.expovariate(self.average_call_lamda)
        self.c_sum+=number
        if self.c_sum>1:
            self.c_sum-=1
            return [(verticle,timestep,timestep+5) for i in range(int(1))]
        return [(verticle,timestep,timestep+5) for i in range(int(number))]
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

class taxi():
    # Speed=30km/hour
    Speed=30
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
        self.profit=0

        self.carry = False
        self.costumer = None

        if self.WB>self.WE:
            for i in range(self.WB,24,1):
                self.time_s.append(i)
            for i in range(0,self.WE, 1):
                self.time_s.append(i)
        else:
            self.time_s=[i for i in range(self.WB,self.WE,1)]
    def cost(self,time_step,costumer_infomation):
        if _SIMULATION_MODE=="MINUTE":
            time_step=(time_step // 60) % 24
        elif _SIMULATION_MODE=="SECOND":
            time_step = (time_step // 60//60) % 24
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
        return self.WB,self.WE
    def IF_WORK(self,time):
        if time in self.time_s:
            return True
        else:
            return False
    def profit(self):
        return self.profit
    def assign_costumer(self,time_step,costumer):
        if not self.IF_WORK():
            raise Exception("The aution algorithm assign the rest taxi")
        if self.carry:
            raise Exception("The aution algorithm assign the taxi carry more one task or didn't change them status")

        if self.IF_WORK():
            if not self.carry:
                #self.profit+=
                self.carry=True
                #print("Using the Hour rule")
                #finish_time_step=time_step+1.*costumer[4]/self.Speed
                #self.costumer = (finish_time_step % 24, costumer)
                print("Using the Minute rule")
                finish_time_step=time_step[1]+1.*costumer[4]/self.Speed/60
                self.costumer = ((finish_time_step//60+time_step[0])%24,finish_time_step % 60, costumer)
    def update_taxi(self,time_step):
        '''
        :param time_step:
        :return location
        Todo :
        1.Based on self.costumer information and planning path to run the location
        2.If arrive carry will False
        '''
        pass
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
        # ??????????? If we need to merge the route of costumer ???????????
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

if __name__=='__main__':
    VMap={'0,0':('0,1',0,)}
