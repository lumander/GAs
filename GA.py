#%matplotlib inline
#import matplotlib
import numpy as np
#import matplotlib.pyplot as plt

def initPopulation( populationRange, individuals ):
    '''initializes randomly a given number of indivuduals within the interval given'''
    
    ##TO DO


    pop = []
    for i in range( individuals ):
        flag = True
        rndm = np.random.randint( 0, populationRange )
        while(flag):
            if rndm not in pop:
                pop.append(rndm)
                flag = False
            else:
                rndm = np.random.randint( 0, populationRange + 1 )
                
    population = np.array( pop )
    return population

def reverse( string ):
    '''inverts the order of the character in a string and return the new string'''

    ## TO DO
    ## CANCEL THIS FUNCTION
    
    number = ""
    for i in range( len( string ) ):
        number += str( string[ len( string )- 1 - i ] )
    return int( number )
    
def encoding( numbers ):
    '''encodes the decimal numbers into binary strings'''
    
    ## TO DO
    ## USE bin FUNCTION

    integerStrings = []
    for nmbr in numbers:
        if nmbr == 0 or nmbr == 1:
            integerStrings.append( nmbr )
        else:
            remainders = ""
            dividendum = nmbr
            flag = True
            while( flag ):
                remainders += str( dividendum % 2 )
                dividendum = dividendum // 2
                if dividendum == 1:
                    remainders += str( dividendum % 2 )
                    break
            integerStrings.append( reverse ( remainders ) )
    chromosomes = len( str( max( integerStrings ) ) )
    binaryStrings = []
    for string in integerStrings:
        binaryStrings.append( str( string ).zfill( chromosomes ) )
    return binaryStrings

def decoding( binaryStrings ): # TO DO
    '''decodes the binary strings into decimal numbers'''
    
    decimals = []
    for string in binaryStrings:
        if string == '0' or string == '1':
            decimals.append( int( string ) )
        else:
            nmbr = 0
            for i in range( len( string ) ):
                nmbr += 2 ** ( len( string ) - i - 1 ) * int( string[ i ] )
            decimals.append( nmbr )
    return np.array( decimals )

def selection( fitnessPop ):
    '''selects the indexes of the best, the second best and the worst in the entire population'''
    
    best = int( fitnessPop.argmax() )
    worst = int( fitnessPop.argmin() )
    secondbest = 0
    maximum = fitnessPop.max()
    otherMaximum = 0
    for fit in fitnessPop:
        if fit > otherMaximum:
            if fit < maximum:
                otherMaximum = fit
                    
    for i in range( len( fitnessPop ) ):
        if otherMaximum == fitnessPop[i]:
            secondbest = i
    
    return np.array( [ best, int( secondbest ), worst ] )

def fitness( population ):
    ''''''
    
    return np.exp( - ( population - 10 )**( 2 ) )

def crossingover( best, secondbest, genes ):
    '''PROVA'''
    
    chromosomes = len( genes[ 0 ] )
    split = int( np.random.randint( 0, chromosomes ) )
    newbest = ""
    newsecondbest = ""
    fittest = []
    for i in range( chromosomes ):
        if i < split:
            newbest += genes[ best ][ i ] 
            newsecondbest += genes[ secondbest ][ i ] 
        else:
            newbest += genes[ secondbest ][ i ]
            newsecondbest += genes[ best ][ i ]
    fittest.append( newbest )
    fittest.append( newsecondbest )
    return np.array( fittest )

def changegenes( fittest, genes, worst ):
    bestFitness = 0
    nmbrs = decoding( fittest )
    choose = fitness( nmbrs )
    if choose[ 0 ] > choose[ 1 ]:
        bestFitness = fittest[ 0 ] 
    else:
        bestFitness = fittest[ 1 ] 
   
    genes[ worst ] = bestFitness
    return genes

population = initPopulation( 20 , 15 )
fitnessPop = fitness( population )
generationCount = 0
while( True ):
    selected = selection( fitnessPop )
    genes = encoding( population )
    fittest = crossingover( selected[ 0 ], selected[ 1 ], genes )
    genes = changegenes( fittest, genes, selected[ 2 ] )
    population = decoding( genes )
    fitnessPop = fitness( population )
    generationCount += 1
    if len( set( population ) ) == 1:
        break
    else:
        print ( "POPULATION: ", population )
        #print "FITNESS:", fitnessPop
        
print ( "POPULATION: ",population )
#print "FITNESS:", fitnessPop
print ( "\nGENERATION COUNT: ", generationCount )
    
