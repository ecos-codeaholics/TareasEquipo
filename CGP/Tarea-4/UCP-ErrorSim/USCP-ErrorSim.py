import random
import pylab
import math
import numpy as np

def getDX(deltaX):
    """returns a random int between 1 and deltaX"""
    return random.choice([0,deltaX])
    
def getTFCError(deltaX):
    """returns the estimated TFC error for a trial"""
    weights = [2,1,1,1,1,0.5,0.5,2,1,1,1,1,1]
    sum = 0.0
    for iw in weights:
        de = getDX(deltaX)
        tfDX = iw*de
        sum += (tfDX*tfDX)
    return math.sqrt(sum)

def getECFError(deltaX):
    """returns the estimated EFC error for a trial"""
    weights = [1.5,0.5,1,0.5,1,2,-1,2]
    sum = 0.0
    for iw in weights:
        de = getDX(deltaX)
        ecDX = iw*de
        sum += (ecDX*ecDX)
    return math.sqrt(sum)
    
def geUUCWError(deltaX):
    """returns the estimated UCW error for a trial"""
    weights = [5,10,15]
    sum = 0.0
    for iw in weights:
        de = getDX(deltaX*5)
        ucDX = iw*de
        sum += (ucDX*ucDX)
    return math.sqrt(sum)
    
def getUAWError(deltaX):
    """returns the estimated ACW error for a trial"""
    weights = [1,2,3]
    sum = 0.0
    for iw in weights:
        de = getDX(deltaX)
        acDX = iw*de
        sum += (acDX*acDX)
    return math.sqrt(sum)

def getUUCPError(deltaX):
    error1 = geUUCWError(deltaX)
    error2 = getUAWError(deltaX)
    return math.sqrt( (error1*error1) + (error2*error2) )
    
def getAvg(mylist):
    sum = 0.0
    for iVal in mylist:
        sum += iVal
    return sum/float(len(mylist))

def runSim(ntrials):
    
    results   = []
    pointsPX  = []
    pointsPY  = []
    pointsPY1 = []
    pointsPY2 = []
    pointsPY3 = []
    
    """From the example in the article"""
    TFC = 0.6 + (0.01*47)
    EFC = 1.4 + (-0.03*26)
    UCP = 264
    
    ##All errors ON
    for deltaX in range(0,6):
        results   = []
        for n in range(0,ntrials):
            errorInTFC  = 0.01*getTFCError(deltaX)
            errorInEFC  = 0.03*getECFError(deltaX)
            errorInUUCP = getUUCPError(deltaX)
            cuadrature  = ((errorInTFC/TFC)*(errorInTFC/TFC))+((errorInEFC/EFC)*(errorInEFC/EFC))+((errorInUUCP/UCP)*(errorInUUCP/UCP))     
            totalError = math.fabs(TFC*EFC*UCP)*math.sqrt(cuadrature)            
            results.append(totalError)
            #print(totalError)        

        avgError = getAvg( results )
        
        pointsPX.append(deltaX)
        pointsPY.append(avgError)
        
    # TFC error = 0
    for deltaX in range(0,6):
        results   = []
        for n in range(0,ntrials):
            errorInTFC  = 0.0
            errorInEFC  = 0.03*getECFError(deltaX)
            errorInUUCP = getUUCPError(deltaX)
            cuadrature  = ((errorInTFC/TFC)*(errorInTFC/TFC))+((errorInEFC/EFC)*(errorInEFC/EFC))+((errorInUUCP/UCP)*(errorInUUCP/UCP))     
            totalError = math.fabs(TFC*EFC*UCP)*math.sqrt(cuadrature)            
            results.append(totalError)
            #print(totalError)        

        avgError = getAvg( results )
             
        pointsPY1.append(avgError)
        
    # ECF error = 0
    for deltaX in range(0,6):
    
        results   = []
        for n in range(0,ntrials):
            errorInTFC  = 0.01*getTFCError(deltaX)
            errorInEFC  = 0.0
            errorInUUCP = getUUCPError(deltaX)
            cuadrature  = ((errorInTFC/TFC)*(errorInTFC/TFC))+((errorInEFC/EFC)*(errorInEFC/EFC))+((errorInUUCP/UCP)*(errorInUUCP/UCP))     
            totalError = math.fabs(TFC*EFC*UCP)*math.sqrt(cuadrature)            
            results.append(totalError)
            #print(totalError)        

        avgError = getAvg( results )
        
        pointsPY2.append(avgError)
        
    # UUCP error = 0
    for deltaX in range(0,6):
        
        results   = []
        for n in range(0,ntrials):
            errorInTFC  = 0.01*getTFCError(deltaX)
            errorInEFC  = 0.03*getECFError(deltaX)
            errorInUUCP = 0.0
            cuadrature  = ((errorInTFC/TFC)*(errorInTFC/TFC))+((errorInEFC/EFC)*(errorInEFC/EFC))+((errorInUUCP/UCP)*(errorInUUCP/UCP))     
            totalError = math.fabs(TFC*EFC*UCP)*math.sqrt(cuadrature)            
            results.append(totalError)

        avgError = getAvg( results )
        
        pointsPY3.append(avgError)
        
    pylab.plot(pointsPX, pointsPY,  marker='o', label="All Errors" ,linestyle='--')
    pylab.plot(pointsPX, pointsPY1, marker='o', label="eTFC=0"     ,linestyle='--')
    pylab.plot(pointsPX, pointsPY2, marker='o', label="eECF=0"     ,linestyle='--')
    pylab.plot(pointsPX, pointsPY3, marker='o', label="eUUCP=0"    ,linestyle='--')
    pylab.title('Error estimation')
    pylab.xlabel('delta estimation')
    pylab.ylabel('Total error')
    pylab.legend(loc='upper left')
    pylab.show()
    
