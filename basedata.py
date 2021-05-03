#Example of possible input data
import numpy as np

#Example of possible array:

#TC = np.array([15, 20, 25])

TC = 15
#coolant temperature celsius
PP = 980
#density of plastic part kg/m^3
CP = 1300
#specific heat capacity of plastic part J/KG*K
LP = 0.001
#half the plastic part thickness m
W = 0.010
#cooling line pitch distance m
D = 0.005
#cooling line diameter m
LM = 0.004
#distance from cooling line to mold wall
TMelt = 180
#Part melted temperature
TEject = 64.9
#Part ejection temperature
TCycle = 10
#Cycle time seconds
TMO = 13
#Initial mold temperature
CVV = 0.227
#coolant velocity liters/sec
DV = 1.002 * 10**-3
#coolant dynamic viscosity
WDV = 0.0009775
#coolant dynamic viscosity when near wall
KC = 0.5918
#thermal conductivity of coolant
PC = 998.2
#coolant density
CC = 4187
#specific heat capacity of coolant
L = 1.15
#coolant line length

moldmatname = "316 Steel" 
#name of  mold material
PM = 7930.
#Mold density kg/m^3: 316 steel
CM = 510.
#Mold specific heat 316 steel
fancye = 0.00015
#average height of pipe surface irregularities (m) 316 steel
KM = 16.5
#thermal conductivity of mold: 316 steel
