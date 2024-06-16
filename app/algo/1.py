from app.simulator.main import simulation
import numpy as np
from data_parser.main import nodes
import matplotlib.pyplot as plt
import cv2

class Port():
    def __init__(self, coord:str):
        self.coordinates = coord


class Woolfs():
    def __init__(self, state_sim, dests, scale = 5):
        self.destinations = dests
        self.scale = scale
        self.simulation = state_sim
        self.preproc()
    def preproc(self):
        ids_lat, ids_lon = np.where(self.simulation.ice_state.to_numpy()>0)
        self.dest_ids = []
        lat_min_id = ids_lat.min()
        lat_max_id = ids_lat.max()
        lon_min_id = ids_lon.min()
        lon_max_id = ids_lon.max()
        self.lat = self.simulation.lat.to_numpy()[lat_min_id:lat_max_id,lon_min_id:lon_max_id].transpose()
        self.lon = self.simulation.lon.to_numpy()[lat_min_id:lat_max_id,lon_min_id:lon_max_id].transpose()
        self.ice = self.simulation.ice_state.to_numpy()[lat_min_id:lat_max_id,lon_min_id:lon_max_id]
        for d in self.destinations:
            d_lat, d_lon = d.coordinates.split(' ')
            mesh = np.concatenate((np.expand_dims(self.lat,-1), np.expand_dims(self.lon,-1)),-1)
            dif = np.abs(mesh-np.array([float(d_lat), float(d_lon)]))
            m = np.sqrt(dif[:,:,0]**2+dif[:,:,1]**2)
            i,j = np.where(m==m.min())
            stop = False
            if i.size!=0 and j.size!=0:
                for k in range(3):
                    if stop:
                        break
                    for l in range(3):
                        try:
                            crit = mesh[i[0]+k-1,j[0]+l-1]-np.array([float(d_lat), float(d_lon)])
                        except:
                            continue
                        if crit[0]<=0 and crit[1]<=0 :
                            self.dest_ids.append([i[0]+k-1,j[0]+l-1])
                            print(crit)
                            stop=True
                            break
    def plot(self):
        self.ice = np.where(self.ice>0,self.ice,0)
        ice_img = ((self.ice-self.ice.min())/(self.ice.max()-self.ice.min()))*255
        ice_img = ice_img.transpose()
        # ice_img = cv2.cvtColor(ice_img,cv2.COLOR_GRAY2BGR)
        ice_img = cv2.resize(ice_img, (0,0), fx=float(self.scale), fy=float(self.scale),interpolation=cv2.INTER_NEAREST)
        ice_img = cv2.blur(ice_img,(2,2))
        ports = np.zeros(ice_img.shape)
        for d in self.dest_ids:
            ports[d[0]*self.scale+self.scale//2, d[1]*self.scale+self.scale//2] = 255
        with open('map.txt','a') as file:
            print(len(self.dest_ids))
            for d in self.dest_ids:
                d.reverse()
                file.write(','.join([str(dd*self.scale+self.scale//2) for dd in d]))
                file.write('\n')
        ports_field = cv2.GaussianBlur(ports,(255,255),sigmaX=21)
        # cv2.imshow('ice', ice_img)
        # cv2.imshow('field', ports_field)
        # cv2.waitKey()
        return ports,ice_img,ports_field

ports = []
for i, r in nodes().iterrows():
    ports.append(Port(f'{r.latitude} {r.longitude}'))

w = Woolfs(simulation, ports)
p,i,f = w.plot()

print(p.shape)
cv2.imwrite('i.bmp', cv2.cvtColor(i.astype(np.uint8),cv2.COLOR_GRAY2RGBA))
cv2.imshow('p', p)
cv2.imshow('i', i)
cv2.imshow('f', f)

cv2.waitKey()

# class Ant:
#     def __init__(self, start:np.ndarray, sense:np.ndarray, speed=10, arc_class=10):
#         self.pos = start
#         self.state = False
#         self.sense = sense
#         self.direction = None
#         self.speed = speed
#         self.kind = arc_class
#         self.directions = np.array([[-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0]])
#         self.view = np.zeros((self.sense[0]*2, self.sense[1]*2, 5)).astype(np.uint8)
#     def randomStep(self):
#         index_change = 0
#         if -1.<self.random<1.:
#             index_change = 0
#         if -2<self.random<=-1:
#             index_change= -1
#         if self.random<=-2:
#             index_change= -2
#         if 1<=self.random<2:
#             index_change= 1
#         if 2<=self.random:
#             index_change= 2
#
#         if self.direction is None:
#             new_index = np.random.randint(len(self.directions))  # Случайный выбор начального направления
#         else:
#             current_index = self.directions.tolist().index(list(self.direction))
#             new_index = (current_index + index_change) % len(self.directions)
#
#         self.direction = self.directions[new_index]
#         self.pos += tuple(self.direction) # Обновление текущей позиции
#
#     def observe(self, map:np.ndarray, rand):
#         boxLU = np.clip(self.pos - self.sense,[0,0],map.shape[:-1])
#         boxRD = np.clip(self.pos + self.sense,[0,0],map.shape[:-1])
#         self.view = map[boxLU[0]:boxRD[0],boxLU[1]:boxRD[1],:]
#         self.random = rand
#
# class Sim:
#     def __init__(self, ants_n, ice, field, ports):
#         self.feromoneMap = np.expand_dims(np.zeros(ice.shape),-1)
#         self.feromoneMap_2 = np.expand_dims(np.zeros(ice.shape),-1)
#         self.weights = np.expand_dims(ice,-1)
#         self.portsField = np.expand_dims(field,-1)
#         self.ports = np.expand_dims(ports,-1)
#         self.portsIds = np.array(np.where(ports>0)).transpose()
#         self.ants = [Ant(self.portsIds[np.random.randint(len(self.portsIds))], np.ones((2,),dtype=int)*5) for _ in range(ants_n)]
#
#         self.frame = np.concatenate([self.feromoneMap,
#                                      self.feromoneMap_2,
#                                      self.weights,
#                                      self.portsField,
#                                      self.ports], -1)
#
#     def updateAnts(self):
#         r = np.random.normal(0., 0.5,len(self.ants))
#         print(r[0])
#         for ant,rand in zip(self.ants,r):
#             ant.observe(self.frame,rand)
#             ant.randomStep()
#             pos = ant.pos
#             if 0<pos[0]<self.frame.shape[0] and 0<pos[1]<self.frame.shape[1]:
#                 pass
#             else:
#                 ant.pos-=ant.direction
#                 ant.direction = ant.direction[::-1]
#                 pos = ant.pos
#             self.ports[pos[0],pos[1]] = 255
#             cv2.imshow('field', self.ports)
#             cv2.waitKey(1)
#
# s = Sim(1000,i,f,p)
# for _ in range(20000):
#     s.updateAnts()




