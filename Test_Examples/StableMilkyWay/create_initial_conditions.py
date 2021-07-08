#!/usr/bin/env python3
"""
Code that creates intial conditions for the Evrard collapse

"""
# load libraries
import numpy as np  # load numpy
import h5py    # hdf5 format
import math

""" initial condition parameters """
FilePath = 'IC.hdf5'

FloatType = np.float64  # double precision: np.float64, for single use np.float32
IntType = np.int64

Grid= 14 #size of the grid used to generate particle distribution
Mstar=1.989*math.exp(30) #total mass of star
Mtot=6.0*math.exp(11)*Mstar #total mass of the sphere in kg
gamma = 5./3.
k=1.38e-23 #boltzmann constant


x = np.zeros((Grid,Grid,Grid))
y = np.zeros((Grid,Grid,Grid))
z = np.zeros((Grid,Grid,Grid))
vx = np.zeros((Grid,Grid,Grid))
vy = np.zeros((Grid,Grid,Grid))
vz = np.zeros((Grid,Grid,Grid))
m = np.zeros((Grid,Grid,Grid))
u = np.zeros((Grid,Grid,Grid))

xx = ((np.arange(Grid)-(Grid/2-0.5))/(Grid/2.0))

for i in range(Grid):
	for j in range(Grid):
		x[:,i,j] = xx[:]
		y[i,:,j] = xx[:]
		z[i,j,:] = xx[:]

x = x.flatten()
y = y.flatten()
z = z.flatten()


#stretching initial conditons to get 1/r density distribution
r = np.sqrt(x**2+y**2+z**2)**0.5

x=x*r
y=y*r
z=z*r

rad = np.sqrt(x**2+y**2+z**2)

j = np.argwhere(rad < 1.0)



number_particles = j.size

particle_mass = Mtot / number_particles

print("We use "+str(number_particles)+ " particles")


x = x[j]
y = y[j]
z = z[j]


Pos = np.zeros((number_particles,3), dtype=FloatType)
Vel = np.zeros((number_particles,3), dtype=FloatType)
Uthermal = np.zeros((number_particles,3), dtype=FloatType)
Mass = np.zeros((number_particles,3), dtype=FloatType)
ids = np.arange(number_particles)

Pos[:,0] = x[:,0]
Pos[:,1] = y[:,0]
Pos[:,2] = z[:,0]




Mass[:] = particle_mass

Uthermal[:] = 0.05

rad = np.sqrt(x[:]**2+y[:]**2+z[:]**2)

rho = math.exp((-(rad[:])**2/2))/np.sqrt(2*np.pi)

#=np.sqrt(particle_mass/(2.*np.pi*k)**3)*((4.*np.pi)*Vel**2*exp(-(particle_mass*Vel**2)/2.*k) #Maxwell-Boltzmann Dist. minus T

intenergy = (gamma - 1) *  Uthermal[:] / (rho[:]**(gamma - 1))

#write intial conditions file

IC = h5py.File('IC.hdf5', 'w')

## create hdf5 groups
header = IC.create_group("Header")
part0 = IC.create_group("PartType0")

## header entries
NumPart = np.array([number_particles], dtype=IntType)
header.attrs.create("NumPart_ThisFile", NumPart)
header.attrs.create("NumPart_Total", NumPart)
header.attrs.create("NumPart_Total_HighWord", np.zeros(1, dtype=IntType) )
header.attrs.create("MassTable", np.zeros(1, dtype=IntType) )
header.attrs.create("Time", 0.0)
header.attrs.create("Redshift", 0.0)
header.attrs.create("BoxSize", 0)
header.attrs.create("NumFilesPerSnapshot", 1)
header.attrs.create("Omega0", 0.0)
header.attrs.create("OmegaB", 0.0)
header.attrs.create("OmegaLambda", 0.0)
header.attrs.create("HubbleParam", 1.0)
header.attrs.create("Flag_Sfr", 0)
header.attrs.create("Flag_Cooling", 0)
header.attrs.create("Flag_StellarAge", 0)
header.attrs.create("Flag_Metals", 0)
header.attrs.create("Flag_Feedback", 0)
if Pos.dtype == np.float64:
    header.attrs.create("Flag_DoublePrecision", 1)
else:
    header.attrs.create("Flag_DoublePrecision", 0)

## copy datasets
part0.create_dataset("ParticleIDs", data=ids )
part0.create_dataset("Coordinates", data=Pos)

part0.create_dataset("Masses", data=Mass)

part0.create_dataset("Velocities", data=Vel)
part0.create_dataset("InternalEnergy", data=intenergy)

IC.close()
