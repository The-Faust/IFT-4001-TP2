from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import logging
from matplotlib.patches import Rectangle


class VisualisationService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def  plot_data(time:list, parameters:list, size:list):
        if not (len(time) == len(parameters) == len(size)):
            raise ValueError(f"time, parameters and size lists must be the same size.\nCurrent size:\ntime : {len(time)}\nparameters : {len(parameters)} \nsize : {len(size)}")
            
        newTime = []
        newParam = []
        newSize = []
        for t,p,s in zip(time,parameters,size):
            newTime.append(np.mean(t))
            newParam.append(p)
            newSize.append(s)
            
            if type(t) == list:
                newTime.append(np.min(t))
                newParam.append(p)
                newSize.append(s)
                
                newTime.append(np.max(t))
                newParam.append(p)
                newSize.append(s)
        
        dt = pd.DataFrame({'time': newTime, 'parameters': newParam, 'size': newSize})
        sns.lineplot(data=dt, x='size', y='time', hue='parameters')
        
    def set_shape_infos(self,rect_size,rect_offset,shape,valid_shapes,u,l, x_lim=160, y_lim=90):
        self.rect_size = rect_size
        self.rect_offset = rect_offset
        self.shape = shape
        self.valid_shapes = valid_shapes
        
        
        fig, ax = plt.subplots()
        
        major_ticks = np.arange(0, np.max([x_lim,y_lim])+1, 1)
        ax.set_xticks(major_ticks)
        ax.set_xticklabels([])
        ax.set_yticks(major_ticks)
        ax.set_yticklabels([])
        ax.grid(which='both')
        
        self.x_lim = x_lim
        ax.set_xlim([0,x_lim])
        
        self.y_lim = y_lim
        ax.set_ylim([y_lim,0])
        
        ax.set_aspect('equal')
        
        self.axData = ax
        self.figData = fig
        
        fig, ax = plt.subplots()
        
        xBox = u[0]-l[0]
        yBox = u[1]-l[1]
        major_ticks = np.arange(0, np.max([xBox,yBox])+1, 1)
        ax.set_xticks(major_ticks)
        ax.set_xticklabels([])
        ax.set_yticks(major_ticks)
        ax.set_yticklabels([])
        ax.grid(which='both')
        
        ax.set_xlim([0,xBox])
        ax.set_ylim([yBox,0])
        
        ax.set_aspect('equal')
        
        self.axSolution = ax
        self.figSolution = fig

    def get_cmap(self,n, name="hsv"):
        return plt.cm.get_cmap(name, n)

            
    def draw_shape(self, x_offset, y_offset, shape_index,ax,color = "blue"):
        for rectangle_index in self.shape[shape_index-1]:
            rectangle_index = rectangle_index -1
            x_rect_offset = x_offset + self.rect_offset[rectangle_index][0]
            y_rect_offset = y_offset + self.rect_offset[rectangle_index][1]
            width = self.rect_size[rectangle_index][0]
            height = self.rect_size[rectangle_index][1]
            ax.add_patch(Rectangle((x_rect_offset, y_rect_offset), width, height,color=color))
            
            
    def max_x_shape(self,shape_index):
        max_x = 0
        for rectangle_index in self.shape[shape_index-1]:
            rectangle_index -= 1
            if (x:= self.rect_offset[rectangle_index][0]+self.rect_size[rectangle_index][0]) > max_x:
                max_x = x
        
        return max_x
    
    def min_x_shape(self,shape_index):
        min_x = np.inf
        for rectangle_index in self.shape[shape_index-1]:
            rectangle_index -= 1
            if (x:= self.rect_offset[rectangle_index][0]) < min_x:
                min_x = x
        
        return min_x
    
    def max_y_shape(self,shape_index):
        max_y = 0
        for rectangle_index in self.shape[shape_index-1]:
            rectangle_index -= 1
            if (y:= self.rect_offset[rectangle_index][1]+self.rect_size[rectangle_index][1]) > max_y:
                max_y = y
        
        return max_y
    
    def min_y_shape(self,shape_index):
        min_y = np.inf
        for rectangle_index in self.shape[shape_index-1]:
            rectangle_index -= 1
            if (y:= self.rect_offset[rectangle_index][1]) < min_y:
                min_y = y
        
        return min_y
    
    def draw_all_shape(self):
        x_offset = 2
        y_offset = 2
        list_y=[0]
        for shape_indexes in self.valid_shapes:
            for shape_index in list(shape_indexes):
                max_x = self.max_x_shape(shape_index)
                min_x = self.min_x_shape(shape_index)
                min_y = self.min_y_shape(shape_index)
                if min_x != max_x :
                    if x_offset+max_x > self.x_lim:
                        x_offset = 2
                        y_offset += np.max(list_y) + 2
                        list_y = [0]
            
                    self.draw_shape(x_offset-min_x, y_offset-min_y, shape_index,self.axData)
                    list_y.append(self.max_y_shape(shape_index))
                    x_offset += max_x +2 - min_x
            x_offset = 2
            y_offset += np.max(list_y) + 2
            list_y = [0]
        
        plt.figure(self.figData.number)
        plt.subplots_adjust(0,0.02,1,0.99)
        
                
        
        
    def draw_solution(self,_x,_kind):
        cmap = self.get_cmap(len(_kind))
        for i,(k,x) in enumerate(zip(_kind,_x)):
            self.draw_shape(x[0],x[1],k,self.axSolution,cmap(i))
       
    def export(self, name):
        plt.figure(1)
        plt.savefig(Path('visualisation_files', f'Data_{name}'))
        plt.figure(2)
        plt.savefig(Path('visualisation_files', f'Solution_{name}'))
        plt.show()
        plt.close()
        
        
        