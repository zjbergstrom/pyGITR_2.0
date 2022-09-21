#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generation of particles distribution for GITR.
@author: guterl
"""
import numpy as np
from numpy import random
import netCDF4
from netCDF4 import Dataset
from pyGITR.Particles import *
import matplotlib.pyplot as plt

ParticleFile='particleConf.nc'

p = ParticleDistribution()

NP=100
p.SetAttr('Np', NP)

# p.ShowAvailablePdfs()

# Set positions of particles
r_shift = 1.485
z_shift = -1.250

# Define DiMES cap surface
xDiMES=r_shift
yDiMES=0.0
zDiMES=z_shift
rDiMES=0.025

# Define bounding box
xBox = xDiMES
yBox = yDiMES
zBox = zDiMES
dxBox = rDiMES*8.5
dyBox = rDiMES*8.5
dzBox = rDiMES*8.5

# Define metal rings
dxBlock = 0.05
dyBlock = dyBox
xBlock=xDiMES-0.01-rDiMES-dxBlock
yBlock=yDiMES
zBlock=zDiMES

print(dyBlock)

xmr = []
ymr = []
while len(xmr) != NP:
    xmr.append(random.uniform(xBlock,xBlock+dxBlock))
    ymr.append(random.uniform(yBlock-dyBlock/2,yBlock+dyBlock/2))
xmr = np.array(xmr)
ymr = np.array(ymr)

p.SetAttr('x',xmr)
p.SetAttr('y',ymr)
p.SetAttr('z',zDiMES+1e-6)

# Set velocities of particles
p.SetAttr(['vx','vy'],'Gaussian')
p.SetAttr(['vz'],'Gaussian')

# Rescale velocity by characteristic velocity
vpara = 1e4
vperp = 1e5
p.ScaleAttr(['vx','vz'],vperp)
p.ScaleAttr('vy',vpara)

# Rotate velocity of particles to put in the reference frame of the magnetic field
# Define rotation
thetaB = 2 #degree by default, set Degree=False in RotateVector for radian
AxisrotB = [1,0,0]  # [0,1,0]

# Check results of the rotation
B0 = [0,1,0]
B = RotateVector(B0, AxisrotB, thetaB)
# PlotVector(B)

# Rotate velocity vector
p.Rotate('v', AxisrotB, thetaB) #rotate (vx,vy,vz) along AxisrotB of angle thetaB
p.ShowAttr()

# Write particle distribution in netcdf file
p.WriteParticleFile('particleConf.nc')


# Distribution can be also defined with a user-defined pdf. Must be formatted as
# f(x, **kwargs)
def LevyDistrib(x, c=1, mu=0):
    return np.sqrt(c/2/np.pi)*np.exp(-c/(x-mu))/((x-mu)**1.5)


p.SetAttr(['vx','vy'],'Gaussian')
p.SetAttr(['vz'],LevyDistrib, x=np.linspace(0.001,10,1000), c=2, mu=0)
p.ScaleAttr(['vx','vz'],vperp)
p.ScaleAttr('vy',vpara)
p.Rotate('v', AxisrotB, thetaB) #rotate (vx,vy,vz) along AxisrotB of angle thetaB
# p.PlotAttr('vz')
p.WriteParticleFile('particleConf2.nc')
p.ShowAttr()
# plt.show()
os.system("mv particleConf* input")


FileNameParticleConf='input/particleConf2.nc'
ParticleConfData = Dataset(FileNameParticleConf, "r", format="NETCDF4")
x = np.array(ParticleConfData['x'])
y = np.array(ParticleConfData['y'])
z = np.array(ParticleConfData['z'])
vx = np.array(ParticleConfData['vx'])
vy = np.array(ParticleConfData['vy'])
vz = np.array(ParticleConfData['vz'])

# plt.scatter(x,y)
# plt.xlabel('x')
# plt.ylabel('y')
# plt.title('x-y scatter')
# plt.savefig('plots/x-y_scatter')

#plot Gaussian v dist
plt.close()
plt.hist(vx,bins=100)
plt.xlabel('Energy Bins [eV]')
plt.ylabel('Histogram')
plt.title('Thomson Energy Distribution')
plt.savefig('plots/vx_hist')

plt.close()
plt.hist(vz,bins=100)
plt.xlabel('Energy Bins [eV]')
plt.ylabel('Histogram')
plt.title('Thomson Energy Distribution')
plt.savefig('plots/vz_hist')


