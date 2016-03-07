import numpy as np
from numpy import pi
import pandas as pd
from pylab import *
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import os,sys

class filebox:
    def __init__(self):
        pass

    def getfile(self):
        path = os.path.abspath(os.path.join(os.path.pardir, 'param'))
        ldir = os.listdir(path)
        dirtemp = []
        for k in ldir:
            dirtemp.insert(-1, os.path.join(path, k))
        #print dirtemp
        return dirtemp

    def getparam(self, dirlist):
        param = {}
        for filedir in dirlist:
            print filedir
            try:
                data = pd.read_excel(filedir)
            except:
                data = pd.read_csv(filedir)
            param.update({filedir: data})
        return param
    
    def procparam(self, param):
        for k, v in param.items():
            v = np.array(v)
            row_l = v.shape[0]
            col_l = v.shape[1]
            #print v.shape
            if row_l == 362:
                v = v[1:, :]
            elif row_l == 181:
                arrtemp1 = v[3: 93, :]
                arrtemp1 = arrtemp1[::-1]
                arrtemp2 = v[91:, :]
                arrtemp2 = arrtemp2[::-1]
                temp = np.zeros((361, col_l))
                temp[0: 90, :] = arrtemp1
                temp[90: 271, :] = v
                temp[271:, :] = arrtemp2
                v = temp
                
            if col_l == 37:
                v = v[:, 1:]
            elif col_l == 38:
                v = v[:, 1: -1]
            param[k] = v
            #print v.shape

    def mindata(self, param):
        for k, v in param.items():
            v = np.array(v)
            v[np.where(v < -45)] = -45
            v += 45
            param[k] = v

    def plotfigure(self, param):
        for k, v in param.items():
            #print k
            theta = np.arange(-180., 181., 1) / 180 * pi
            fine = np.arange(0., 180., 5) / 180 * pi
            row_l = v.shape[0]
            col_l = v.shape[1]
            #print row_l, col_l
            x = np.transpose(np.ones((col_l, 1)).dot(np.sin(theta).reshape(1, row_l))) * np.ones((row_l, 1)).dot(np.cos(fine).reshape(1, col_l)) * np.array(v)
            y = np.transpose(np.ones((col_l, 1)).dot(np.sin(theta).reshape(1, row_l))) * np.ones((row_l, 1)).dot(np.sin(fine).reshape(1, col_l)) * np.array(v)
            z = np.transpose(np.ones((col_l, 1)).dot(np.cos(theta).reshape(1, row_l))) * np.array(v)
            fig = figure()
            ax = Axes3D(fig)
            ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap = cm.jet, linewidth=0, antialiased=False)
            ax.set_title(unicode(os.path.basename(k), "utf-8"))
            ax.set_xlabel(unicode("satespeed", "utf-8"))
            ax.set_ylabel(unicode("subspeed", "utf-8"))
            ax.set_zlabel(unicode("earthtosate", "utf-8"))
        show()
            

if __name__ == '__main__':
    filelist = filebox().getfile()
    param = filebox().getparam(filelist)
    filebox().procparam(param)
    filebox().mindata(param)
    filebox().plotfigure(param)
