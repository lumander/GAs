#%matplotlib inline
#import matplotlib
import numpy as np
#import matplotlib.pyplot as plt

def init_population( population_range, individuals ):
    '''initializes randomly a given number of indivuduals within the interval given'''
    
    ##TO DO


    pop = []
    for i in range( individuals ):
        flag = True
        rndm = np.random.randint( 0, population_range + 1 )
        while( flag ):
            if rndm not in pop:
                pop.append( rndm )
                flag = False
            else:
                rndm = np.random.randint( 0, population_range + 1 )
                
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
    
def encoding( population ):
    '''encodes the decimal population into binary strings'''
    
    ## TO DO
    ## USE bin FUNCTION

    integer_strings = []
    for nmbr in population:
        if nmbr == 0 or nmbr == 1:
            integer_strings.append( nmbr )
        else:
            remainders = ""
            dividendum = nmbr
            flag = True
            while( flag ):
                remainders += str( dividendum % 2 )
                dividendum = dividendum // 2 # diff from python 2.x
                if dividendum == 1:
                    remainders += str( dividendum % 2 )
                    break
            integer_strings.append( reverse ( remainders ) )
    chromosomes = len( str( max( integer_strings ) ) )
    genes = []
    for string in integer_strings:
        genes.append( str( string ).zfill( chromosomes ) )
    return genes

def decoding( genes ): # TO DO

    '''decodes the binary strings into decimal population'''
    
    decimals = []
    for string in genes:
        if string == '0' or string == '1':
            decimals.append( int( string ) )
        else:
            nmbr = 0
            for i in range( len( string ) ):
                nmbr += 2 ** ( len( string ) - i - 1 ) * int( string[ i ] )
            decimals.append( nmbr )
    return np.array( decimals )

def selection( fitness_pop ):
    '''selects the indexes of the best, the second best and the worst in the entire population'''
    
    selected = {}
    selected[ 'best' ] = int( fitness_pop.argmax() )
    selected[ 'worst' ] = int( fitness_pop.argmin() )
    second_best = 0
    maximum = fitness_pop.max()
    other_maximum = 0
    for fit in fitness_pop:
        if fit > other_maximum:
            if fit < maximum:
                other_maximum = fit
                    
    for i in range( len( fitness_pop ) ):
        if other_maximum == fitness_pop[i]:
            second_best = i
        
    
    selected[ 'second_best' ] = int( second_best )
    
    return selected

def fitness( population ):
    ''''''
    
    return np.exp( - ( population - 10 )**( 2 ) )

def crossing_over( best, second_best, genes ):
    '''PROVA'''
    
    chromosomes = len( genes[ 0 ] )
    split_point = int( np.random.randint( 0, chromosomes ) )
    new_best = ""
    new_second_best = ""
    fittest = []
    for i in range( chromosomes ):
        if i < split_point:
            new_best += genes[ best ][ i ] 
            new_second_best += genes[ second_best ][ i ] 
        else:
            new_best += genes[ second_best ][ i ]
            new_second_best += genes[ best ][ i ]
    fittest.append( new_best )
    fittest.append( new_second_best )
    return np.array( fittest )

def change_genes( fittest, genes, worst ):
    best_fitness = 0
    nmbrs = decoding( fittest )
    choose = fitness( nmbrs )
    if choose[ 0 ] > choose[ 1 ]:
        best_fitness = fittest[ 0 ] 
    else:
        best_fitness = fittest[ 1 ] 
   
    genes[ worst ] = best_fitness
    return genes

population = init_population( 20 , 20 )
fitness_pop = fitness( population )
generation_count = 0

def print_status( population, generation_count ):
    print ( "POPULATION: ", population )
    print ( "\nGENERATION COUNT: ", generation_count )

try:
    while( True ):
        selected = selection( fitness_pop )
        genes = encoding( population )
        fittest = crossing_over( selected[ 'best' ], selected[ 'second_best' ], genes )
        genes = change_genes( fittest, genes, selected[ 'worst' ] )
        print (genes)
        population = decoding( genes )
        fitness_pop = fitness( population )
        generation_count += 1
        if len( set( population ) ) == 1:
            print_status( population, generation_count )
            break
        else:
            print ( "POPULATION: ", population )
            if generation_count > 20:
                if len( set( population ) ) < 3:
                    print_status( population, generation_count )
                    break

except KeyboardInterrupt:
    print ("\nInterrupted by user\n")
        

    
