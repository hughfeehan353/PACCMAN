import matplotlib.pyplot as plt


import math
import numpy as np

programfunction = input('What would you like to use this program for? M for mold material comparison, H for heat transfer coefficient comparison, N for simple data from a single mold material and user choice of heat transfer coefficient: ' )


if programfunction == "N" or programfunction == "n": 
    heat_coefficient_correlation = input("Please choose a heat transfer correllation. D for Dittus-Boelter, G for Gnielinski, S for Sieder-Tate: ")

savegraphs = input ("Would you like to save an image of the graphs? Y for yes, N for no: ")



#general note: when programfunction = N or H, the first choice of mold material properties is used (KM1, PM1, etc.)

testTC = 15.
#coolant temperature celsius
testPP = 980.
#density of plastic part kg/m^3
testCP = 1300.
#specific heat capacity of plastic part J/KG*K
testLP = 0.001
#half the plastic part thickness m
testW = 0.010
#cooling line pitch distance m
testD = 0.005
#cooling line diameter m
testLM = 0.004
#distance from cooling line to mold wall
testTMelt = 180.
#Part melted temperature
testTEject = 64.9
#Part ejection temperature
testTCycle = 10.
#Cycle time seconds
testTMO = 13.
#Initial mold temperature
testCVV = 0.227
#coolant velocity liters/sec
testDV = 1.002 * 10**-3
#coolant dynamic viscosity
testWDV = 0.0009775
#coolant dynamic viscosity when near wall
testKC = 0.5918
#thermal conductivity of coolant
testPC = 998.2
#coolant density
testCC = 4187
#specific heat capacity of coolant
testL = 1.15
#coolant line length


moldmatname1 = "316 Steel"
#name of first mold material
moldmatname2 = "6061 Aluminum"
#name of second mold material
moldmatname3 = "Copper"
#name of third mold material
test1PM = 7930.
#First comparison Mold density kg/m^3: 316 steel
test2PM = 2700
#Second comparison Mold density kg/m^3: aluminum 6061
test3PM = 8960
#Third comparison Mold density kg/m^3: copper
test1CM = 510.
#First comparison Mold specific heat 316 steel
test2CM = 896
#Second comparison Mold specific heat aluminum
test3CM = 380
#Third comparison Mold specific heat copper
test1fancye = 0.00015
#First comparison average height of pipe surface irregularities (m) 316 steel
test2fancye =  0.000001
#Second comparison average height of pipe surface irregularities (m) aluminum
test3fancye = 0.000001
#Third comparison average height of pipe surface irregularities (m) copper
test1KM = 16.5
#First comparison thermal conductivity of mold: 316 steel
test2KM = 180
#Second comparison thermal conductivity of mold: aluminum 6061
test3KM = 402
#Third comparison thermal conductivity of mold: copper




def FVfunc(CVV, D): 
    FV = (CVV*0.001)/(np.pi*(D/2)**2)
    return FV
#flow velocity of coolant m/s

FV = FVfunc(testCVV, testD)
print ("flow velocity:", FV)

def KVfunc(DV,PC):
    KV = DV/PC
    return KV
#coolant kinematic viscosity



KV = KVfunc(testDV,testPC)
print ("kinematic viscosity:", KV)



def REfunc(FV,D,KV):
    RE = FV*D/KV
    return RE
#Reynolds number of coolant


RE = REfunc(FV,testD,KV)
print ("Reynolds number:", RE)


def PRfunc(DV,CC,KC):
    PR = DV*CC/KC
    return PR
#Prandl number of coolant


PR = PRfunc(testDV,testCC,testKC)
print ("Prandl number:", PR)


def DFfunc(fancye,D,RE):
    DF = (1/(-1.8*np.log(((fancye/(3.7*D))**1.11)+(6.9/RE))))**2
    return DF
#Darcy friction factor

DF1 = DFfunc(test1fancye,testD,RE)
print ("Darcy friction factor (",moldmatname1,"):", DF1)

if programfunction == "M" or "m":
    DF2 = DFfunc(test2fancye,testD,RE)
    print ("Darcy friction factor (",moldmatname2,"):", DF2)
if programfunction == "M" or "m":
    DF3 = DFfunc(test3fancye,testD,RE)   
    print ("Darcy friction factor (",moldmatname3,"):", DF3)
    

def DBNU(RE,PR):
    NU = (0.023*RE**0.8)*PR**0.4
    return NU
def GNU(DF,RE,PR):
    NU = ((DF/8)*(RE-1000)*PR)/(1+(12.7*((DF/8)**0.5)*(PR**(2/3)-1)))
    return NU
def STNU(RE,PR,DV,WDV):
    NU = 0.027*(RE**(4/5))*(PR**(1/3))*((DV/WDV)**0.14)
    return NU
	
def htc(KC,D,NU):
    h = (KC/D)* NU
    return h
#Heat transfer coefficient



if programfunction == "M" or "m": 
    h1 = htc(testKC,testD,GNU(DF1,RE,PR))
    print ("heat transfer coefficient (",moldmatname1,"):", h1)
    h2 = htc(testKC,testD,GNU(DF2,RE,PR))
    print ("heat transfer coefficient (",moldmatname2,"):", h2)
    h3 = htc(testKC,testD,GNU(DF3,RE,PR))
    print ("heat transfer coefficient (",moldmatname3,"):", h3)

elif programfunction == "H" or "h":
    h1 = htc(testKC,testD,DBNU(RE,PR))
    print ("heat transfer coefficient (Ditus-Boelter):", h1)
    h2 = htc(testKC,testD,DBNU(RE,PR))
    print ("heat transfer coefficient (Gnielinski):", h2)
    h3 = htc(testKC,testD,DBNU(RE,PR,testDV,testWDV))
    print ("heat transfer coefficient (Sieder-Tate):", h3)
elif programfunction == "N" or "n":
    if heat_coefficient_correlation == "D":
        h1 = htc(testKC,testD,DBNU(RE,PR))
        print ("heat transfer coefficient", h1)
    elif heat_coefficient_correlation == "G":
        h2 = htc(testKC,testD,GNU(DF1,RE,PR))
        print ("heat transfer coefficient", h2)
    elif heat_coefficient_correlation == "S":
        h3 = htc(testKC,testD,DBNU(RE,PR,testDV,testWDV))
        print ("heat transfer coefficient", h3)
        
else: 
    print ("false")



def ATMfunc(PP,CP,LP,KM,W,h,D,LM,TMelt,TEject,TCycle,TC):
    ATM = PP*CP*LP*(2.0*KM*W + h*D*LM*np.pi)*(TMelt - TEject)
    ATM = ATM/(h*D*KM*TCycle*np.pi) + TC
    return ATM

if programfunction == "M" or "m": 
    ATM1 = ATMfunc(testPP,testCP,testLP,test1KM,testW,h1,testD,testLM,testTMelt,testTEject,testTCycle,testTC)
    print ("temperature of the mold (",moldmatname1,"):", ATM1)
    ATM2 = ATMfunc(testPP,testCP,testLP,test2KM,testW,h2,testD,testLM,testTMelt,testTEject,testTCycle,testTC)
    print ("temperature of the mold (",moldmatname2,"):", ATM2)
    ATM3 = ATMfunc(testPP,testCP,testLP,test3KM,testW,h3,testD,testLM,testTMelt,testTEject,testTCycle,testTC)
    print ("temperature of the mold (",moldmatname3,"):", ATM3)

elif programfunction == "H" or "h":
    
    ATM1 = ATMfunc(testPP,testCP,testLP,test1KM,testW,h1,testD,testLM,testTMelt,testTEject,testTCycle,testTC)
    print ("temperature of the mold (Ditus-Boelter):", ATM1)
    ATM2 = ATMfunc(testPP,testCP,testLP,test1KM,testW,h2,testD,testLM,testTMelt,testTEject,testTCycle,testTC)
    print ("temperature of the mold (Gnielinski):", ATM2)
    ATM3 = ATMfunc(testPP,testCP,testLP,test1KM,testW,h3,testD,testLM,testTMelt,testTEject,testTCycle,testTC)
    print ("temperature of the mold (Sieder-Tate):", ATM3)
    
elif programfunction == "N" or "n":
    ATM1 = ATMfunc(testPP,testCP,testLP,test1KM,testW,h1,testD,testLM,testTMelt,testTEject,testTCycle,testTC)
    print ("temperature of the mold:", ATM1)
#Average temperature of the mold



def TConstantfunc(PM,CM,LM,KM,W,h,D):
    TConstant = ((PM*CM*LM**2)/KM)*(1+(2.0*W*KM)/(h*D*LM*np.pi))
    return TConstant

if programfunction == "M" or "m":
    TConstant1 = TConstantfunc(test1PM,test1CM,testLM,test1KM,testW,h1,testD)
    TConstant2 = TConstantfunc(test2PM,test2CM,testLM,test2KM,testW,h2,testD)
    TConstant3 = TConstantfunc(test3PM,test3CM,testLM,test3KM,testW,h3,testD)
    print ("time constant (",moldmatname1,"):", TConstant1)
    print ("time constant (",moldmatname2,"):", TConstant2)
    print ("time constant (",moldmatname3,"):", TConstant3)
elif programfunction == "H" or "h":
    TConstant1 = TConstantfunc(test1PM,test1CM,testLM,test1KM,testW,h1,testD)
    TConstant2 = TConstantfunc(test1PM,test1CM,testLM,test1KM,testW,h2,testD)
    TConstant3 = TConstantfunc(test1PM,test1CM,testLM,test1KM,testW,h3,testD)
    print ("time constant (Ditus-Boelter):", TConstant1)
    print ("time constant (Gnielinski):", TConstant2)
    print ("time constant (Sieder-Tate):", TConstant3)
elif programfunction == "N" or "n":
    TConstant1 = TConstantfunc(test1PM,test1CM,testLM,test1KM,testW,h1,testD)
    print ("time constant", TConstant1)

#Time constant




x = np.linspace(0,100)




y1 = ATM1 + ((testTMO-ATM1)*np.e**(-x/TConstant1))
if programfunction == "M" or programfunction == "m" or programfunction == "H" or programfunction == "h":
    y2 = ATM2 + ((testTMO-ATM2)*np.e**(-x/TConstant2))
if programfunction == "M" or programfunction == "m" or programfunction == "H" or programfunction == "h":
    y3 = ATM3 + ((testTMO-ATM3)*np.e**(-x/TConstant3))




if programfunction == "M" or programfunction == "m":
    plt.plot(x,y1,'r', ls=('dotted'), label=moldmatname1)
    plt.plot(x,y2,'black', ls=('dotted'), label=moldmatname2)
    plt.plot(x,y3,'b', ls=('dotted'), label=moldmatname3)

elif programfunction == "H" or programfunction == "h":
    plt.plot(x,y1,'r', ls=('dotted'), label='Ditus-Boelter')
    plt.plot(x,y2,'black', ls=('dotted'), label='Gnielinski')
    plt.plot(x,y3,'b', ls=('dotted'), label='Sieder-Tate')
elif programfunction == "N" or programfunction == "n":
    plt.plot(x,y1,'r', ls=('dotted'), label=moldmatname1)
    
plt.axis([0,25,13,20])
plt.xlabel("Time (s) from beginning of heat cycling")
plt.ylabel("Average heat cycle temperature (C)")
plt.grid('both')
plt.legend()




if savegraphs == "Y" or savegraphs == "y":
    plt.savefig("conformal-cooling-comparison.png")
    plt.savefig("conformal-cooling-comparison.eps")




def pdropfunc(DF,L,D,PC,CVV):
    pdrop = (DF*L/D)*(PC/2)*CVV**2
    return pdrop

if programfunction == "M" or "m":
    pdrop1 = pdropfunc(DF1,testL,testD,testPC,testCVV)
    pdrop2 = pdropfunc(DF2,testL,testD,testPC,testCVV)
    pdrop3 = pdropfunc(DF3,testL,testD,testPC,testCVV)

    print ("coolant pressure drop (",moldmatname1,"):", pdrop1)
    print ("coolant pressure drop (",moldmatname2,"):", pdrop2)
    print ("coolant pressure drop (",moldmatname3,"):", pdrop3)

elif programfunction == "H" or "h" or "N" or "n":
    pdrop1 = pdropfunc(DF1,testL,testD,testPC,testCVV)
    print ("coolant pressure drop:", pdrop1)

#coolant pressure drop




#unit testing:
#def testATM1():
	#global ATM1
	#ATM1Test = ATM1
	#ATM1 = PP*CP*LP*(2.0*KM1*W + h1*D*LM*np.pi)*(TMelt - TEject)
	#ATM1 = (ATM1/(h1*D*KM1*TCycle*np.pi)) + TC
	#assert ATM1Test == ATM1
#def testATM2():
	#global ATM2
	#ATM2Test = ATM2
	#ATM2 = PP*CP*LP*(2.0*KM2*W + h2*D*LM*np.pi)*(TMelt - TEject)
	#ATM2 = (ATM2/(h2*D*KM2*TCycle*np.pi)) + TC
#	assert ATM2Test == ATM2
#def testATM3():
	#global ATM3
	#ATM3Test = ATM3
	#ATM3 = PP*CP*LP*(2.0*KM3*W + h3*D*LM*np.pi)*(TMelt - TEject)
	#ATM3 = (ATM3/(h3*D*KM3*TCycle*np.pi)) + TC
	#assert ATM3Test == ATM3
#testATM1()
#testATM2()
#testATM3()