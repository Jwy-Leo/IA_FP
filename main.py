import numpy as np
import argparse
import cv2
from agent import costumer_generator,company,taxi
from Graph import Graph
'''
from taxi import taxi
from company import company
from costumer import costumer_generator
'''
parse=argparse.ArgumentParser(description="Muti-agent system simulation taxi and costomer")
parse.add_argument("--CMN",default=5,help="Costomer_Max_Number")
parse.add_argument("--Taxi_number",default=5)
parse.add_argument("--STS",default=1*24*60,help="Simulation_Time_Step(minute)")

args=parse.parse_args()

# Global parameter
Visualize=True
Write_VIDEO=False
class Map_visiualize():
    def __init__(self,Map):
        self.mapsize = 1000
        self.Mapwindow = 700
        self.windowbias= (self.mapsize - self.Mapwindow) // 2
        self.scale=self.Mapwindow//14
        self.graph=Map
        self.graph_absolutely={}
        self.BG=self.back_ground()
    def begin(self,timestep):
        Map = np.copy(self.BG)
        Map = self.Top(Map, timestep)
        return Map
    def back_ground(self):
        Map = np.zeros((self.mapsize, self.mapsize, 3))
        '''
        cv2.rectangle(Map, (self.windowbias, self.windowbias),
                      (self.mapsize - self.windowbias, self.mapsize - self.windowbias),
                      color=(255, 255, 255))
        '''
        keys=self.graph.get_vertices_name()
        local_bias_horizontal=self.windowbias
        local_bias_vertical=self.windowbias
        for i in range(8):
            for j in range(8):
                if not '%d,%d'%(i,j) in keys:
                    continue
                else:
                    dictinfo=self.graph.get_vertices_information('%d,%d'%(i,j))
                    cv2.circle(Map, (local_bias_horizontal,local_bias_vertical), radius=5, color=(0, 255, 255))
                    self.graph_absolutely['%d,%d'%(i,j)]=(local_bias_horizontal,local_bias_vertical)
                    for k in dictinfo.keys():
                        x = int(dictinfo[k][0] * np.cos(2 * np.pi / 360 * dictinfo[k][1]) * self.scale)
                        y = -1*int(dictinfo[k][0] * np.sin(2 * np.pi / 360 * dictinfo[k][1]) * self.scale)
                        cv2.line(Map, (local_bias_horizontal, local_bias_vertical),
                                 (local_bias_horizontal + x, local_bias_vertical + y),
                                 color=(255, 255, 255))
                    if '%d,%d'%(i,j+1) in dictinfo.keys():
                        local_bias_horizontal += self.scale * dictinfo['%d,%d'%(i,j+1)][0]
                    else:
                        local_bias_horizontal=self.windowbias
            if not '%d,%d' % (i, 0) in keys:
                continue
            else:
                dictinfo = self.graph.get_vertices_information('%d,%d' % (i, 0))
                if '%d,%d' % (i+1,0) in dictinfo.keys():
                    local_bias_vertical += self.scale * dictinfo['%d,%d' % (i+1,0)][0]#*2
        return Map
    def Top(self,Map,time,timescale="MINUTE"):
        if timescale=="HOUR":
            time_context="Hour:%02d,%02d"%(time//24,time%24)
        elif timescale=="MINUTE":
            time_context = "Hour:%02d,%02d:%02d" % ((time//60) // 24, (time//60) % 24,time%60)
        cv2.putText(Map,time_context,
                    (self.Mapwindow//2//2//2,self.windowbias//2),thickness=5,
                    fontFace=1,fontScale=5,color=(255,255,255))
        return Map
    def put_message(self,Map,verticle_name,number):
        Map=cv2.putText(Map, '%d'%number,
                    self.graph_absolutely[verticle_name], thickness=5,
                    fontFace=1, fontScale=3, color=(255, 255, 255))
        return Map
if Write_VIDEO:
    video = cv2.VideoWriter('video.avi',
                        #apiPreference=cv2.CAP_ANY,
                        fourcc=cv2.VideoWriter_fourcc(*'MJPG'),
                        fps=30.0,
                        frameSize=(1000,1000),
                        isColor=True)
#Map
def V_city_map():
    g=Graph()

    g.add_vertex('0,0',{'0,1':(2,0),'1,0':(2,270)})
    g.add_vertex('0,1', {'0,0':(2,180),'0,2': (4, 0), '1,1': (2, 270)})
    g.add_vertex('0,2', {'0,1': (4, 180), '0,3': (2, 0), '1,2': (2, 270)})
    g.add_vertex('0,3', {'0,2': (2, 180), '0,4': (4, 0), '1,4': (2, 270)})
    g.add_vertex('0,4', {'0,3': (4, 180), '0,5': (2, 0), '1,5': (2, 270)})
    g.add_vertex('0,5', {'0.4': (2, 180), '1,6': (2, 270)})

    g.add_vertex('1,0', {'1,1': (2, 0), '2,0': (1, 270),'0,0': (2,90) })
    g.add_vertex('1,1', {'1,0': (2, 180), '1,2': (4, 0), '2,1': (1, 270),'0,1': (2,90) })
    g.add_vertex('1,2', {'1,1': (4, 180), '1,3': (1, 0), '2,2': (1, 270),'0,2': (2,90) })
    g.add_vertex('1,3', {'1,2': (1, 180), '1,4': (1,0) ,'2,3':(1,270)})
    g.add_vertex('1,4', {'1,3': (1, 180), '1,5': (4, 0), '2,4': (1, 270),'0,3': (2,90) })
    g.add_vertex('1,5', {'1,4': (4, 180), '1,6': (2, 0), '2,5': (1, 270),'0,4': (2,90) })
    g.add_vertex('1,6', {'1.5': (2, 180), '2,6': (1, 270),'0,5': (2,90) })

    g.add_vertex('2,0', {'2,1': (2, 0), '3,0': (1, 270), '1,0': (1, 90)})
    g.add_vertex('2,1', {'2,0': (2, 180), '2,2': (4, 0), '3,1': (1, 270), '1,1': (1, 90)})
    g.add_vertex('2,2', {'2,1': (4, 180), '2,3': (1, 0), '3,2': (1, 270), '1,2': (1, 90)})
    g.add_vertex('2,3', {'2,2': (1, 180), '2,4': (1, 0),'1,3':(1,90), '3,3': (1, 270)})
    g.add_vertex('2,4', {'2,3': (1, 180), '2,5': (4, 0), '3,4': (1, 270), '1,3': (1, 90)})
    g.add_vertex('2,5', {'2,4': (4, 180), '2,6': (2, 0), '3,5': (1, 270), '1,4': (1, 90)})
    g.add_vertex('2,6', {'2.5': (2, 180), '3,6': (1, 270), '1,5': (1, 90)})

    g.add_vertex('3,0', {'3,1': (2, 0), '4,0': (1, 270), '2,0': (1, 90)})
    g.add_vertex('3,1', {'3,0': (2, 180), '3,2': (2, 0), '4,1': (1, 270), '2,1': (1, 90)})
    g.add_vertex('3,2', {'3,1': (2, 180), '3,3': (2, 0), '4,2': (1, 270)})
    g.add_vertex('3,3', {'3,2': (2, 180), '3,4': (1, 0), '4,3': (1, 270), '2,2': (1, 90)})
    g.add_vertex('3,4', {'3,3': (1, 180), '3,5': (1, 0),'2,3':(1,90)})
    g.add_vertex('3,5', {'3,4': (1, 180), '3,6': (4, 0), '4,4': (1, 270), '2,4': (1, 90)})
    g.add_vertex('3,6', {'3,5': (4, 180), '3,7': (2, 0), '4,5': (1, 270), '2,5': (1, 90)})
    g.add_vertex('3,7', {'3.6': (2, 180), '4,6': (1, 270), '2,6': (1, 90)})

    g.add_vertex('4,0', {'4,1': (2, 0), '5,0': (2, 270), '3,0': (1, 90)})
    g.add_vertex('4,1', {'4,0': (2, 180), '4,2': (2, 0), '5,1': (2, 270), '3,1': (1, 90)})
    g.add_vertex('4,2', {'4,1': (2, 180), '4,3': (2, 0), '5,2': (2, 270), '3,2': (1, 90)})
    g.add_vertex('4,3', {'4,2': (2, 180), '4,4': (2, 0), '5,3': (2, 270),'3,3':(1,90)})
    g.add_vertex('4,4', {'4,3': (2, 180), '4,5': (4, 0), '5,4': (2, 270), '3,5': (1, 90)})
    g.add_vertex('4,5', {'4,4': (4, 180), '4,6': (2, 0), '5,5': (2, 270), '3,6': (1, 90)})
    g.add_vertex('4,6', {'4.5': (2, 180), '5,6': (2, 270), '3,7': (1, 90)})

    g.add_vertex('5,0', {'5,1': (2, 0),  '4,0': (2, 90)})
    g.add_vertex('5,1', {'5,0': (2, 180), '5,2': (2, 0), '4,1': (2, 90)})
    g.add_vertex('5,2', {'5,1': (2, 180), '5,3': (2, 0), '4,2': (2, 90)})
    g.add_vertex('5,3', {'5,2': (2, 180), '5,4': (2, 0), '4,3': (2, 90)})
    g.add_vertex('5,4', {'5,3': (2, 180), '5,5': (4, 0), '4,4': (2, 90)})
    g.add_vertex('5,5', {'5,4': (4, 180), '5,6': (2, 0), '4,5': (2, 90)})
    g.add_vertex('5,6', {'5.5': (2, 180), '4,6': (2, 90)})
    #'vertical,horizental'
    return g
#Company_agent initial
def Company_agent_and_Taxi_register():
    CompanyLocation=(4,4)
    Company_agent=company(company_location=CompanyLocation)
    for i in range(4):
        Company_agent.register_taxi(taxi(worktime_begin=3, worktime_end=13,x=CompanyLocation[0],y=CompanyLocation[1]))
        Company_agent.register_taxi(taxi(worktime_begin=9, worktime_end=19,x=CompanyLocation[0],y=CompanyLocation[1]))
        Company_agent.register_taxi(taxi(worktime_begin=18, worktime_end=4,x=CompanyLocation[0],y=CompanyLocation[1]))
    return Company_agent

VCM=V_city_map()
Map_visiual=Map_visiualize(VCM)
CA=Company_agent_and_Taxi_register()
CG=costumer_generator()
costumer_list=[]
TTT = 0
v_list=VCM.get_vertices_name()
for time in range(args.STS):
    CG.change_lamda(time)
    # Initial Map
    # Generate costumer information
    # node_list=np.random.permutation(len(v_list))
    node_list = np.random.permutation(len(v_list))
    for i in range(len(v_list)):  # Scanning all map
        costumer_list += CG.generate_costumer(v_list[node_list[i]], time)
    NL={}
    for i in range(len(costumer_list)):
        if costumer_list[i][0] not in NL.keys():
            NL[costumer_list[i][0]]=1
        else:
            NL[costumer_list[i][0]] += 1
    if Visualize:
        Map = Map_visiual.begin(time)
        for k in NL.keys():
            Map=Map_visiual.put_message(Map,k,NL[k])
        cv2.imshow("V_city", Map)
    '''
    node_list = np.random.permutation(36)
    for i in range(36): # Scanning all map
        costumer_list+=CG.generate_costumer(node_list[i]//6,node_list[i]%6,time)
        put_message
    '''


    #Initial costomer
    #company.bidding()
    print("Hour:%d,%d:%d"%((time//60)%24,time%60,len(costumer_list)))
    # delete item
    delitem = []
    for i in range(len(costumer_list)):
        if costumer_list[i][2] == time:
            delitem.append(costumer_list[i])
    for i in range(len(delitem)):
        costumer_list.remove(delitem[i])
    if Write_VIDEO:
        video.write(np.uint8(np.clip(Map*255,0,255)))
    if Visualize:
        cv2.waitKey(70)
if Write_VIDEO:
    video.release()

