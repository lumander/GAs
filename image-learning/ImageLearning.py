from GeneticAlgorithm import GA
from Individual import Rectangle, Individual
from PIL import Image, ImageDraw
import numpy as np
             

class ImageLearning(GA):

    def __init__( self, parameters ):

        '''
        Constructor of the Class ImageLearning
        '''

        GA.__init__( self, parameters )
        self.rectangles = 32
        self.bit = 8
        self.alleles = 7 * self.bit
        self.generation_count = 0
        self.population=[]
        self.image = np.asarray( Image.open('image-learning/LaNascitaDiVenere.jpg') )
        self.pixel_x = len( self.image[0] )
        self.pixel_y = len( self.image )
       
    def init_population( self ):

        '''
        Population is encoded into a list of n Image objects
        '''
        random_string = np.random.randint( 0, 2, ( self.pop_size,  self.rectangles * self.alleles ), dtype='uint8' )

        for i in range( self.pop_size ):
            binary_encoding = ""
            for j in range( self.rectangles * self.alleles ):
                binary_encoding += str( random_string[ i, j ] )
            ind = Individual( self.rectangles, binary_encoding, self.pixel_x, self.pixel_y )
            ind.toGrayCode()
            self.population.append( ind )

    def crossing_over( self ):

        '''
        Genes of the population undergo Crossing Over
        '''

        child_one = ""
        child_two = ""
        #random_pick = np.random.randint( 1, self.pop_size )       
        for individual in range( 0 , self.pop_size - 1 , 2 ):
            child_one=""
            child_two=""
            split_point = np.random.randint( 0, self.rectangles * self.alleles )
            for i in range( 0, split_point ):
                child_one += self.population[ individual ].binary_encoding[ i ] 
                child_two += self.population[ individual + 1 ].binary_encoding[ i ]
            for i in range( split_point, self.rectangles * self.alleles ):
                child_one += self.population[ individual + 1 ].binary_encoding[ i ] 
                child_two += self.population[ individual ].binary_encoding[ i ]
            #self.population[individual].binary_encoding = child_one
            #self.population[individual + 1].binary_encoding = child_two
            brother = Individual( self.rectangles, child_one, self.pixel_x, self.pixel_y )
            sister = Individual( self.rectangles, child_two, self.pixel_x, self.pixel_y )
            self.population.append( brother )
            self.population.append( sister )
        
    def mutation( self ):
        
        '''
        Genes undergo random mutations
        '''

        random_pick = np.random.randint( 0, self.pop_size )
        temp_list = list( self.population[ random_pick ].binary_encoding )
        random_pick_2 = np.random.randint( 0, len( temp_list ) )
        if temp_list[ random_pick_2 ] == '0':
            temp_list[ random_pick_2 ]= '1'
        else:
            temp_list[ random_pick_2 ]= '0'
        
        self.population[ random_pick ].binary_encoding = "".join(temp_list)

                

        
        #for individual in self.population:
        #    random_pick = np.random.randint( 0, self.pop_size )
        #    temp_list = list( individual.binary_encoding )
        #    if random_pick % 2 == 0:
        #        for i in range( random_pick, 56 ):
        #            if temp_list[ i ] == '1':
        #                temp_list[ i ] = '0'
        #    else:
        #        for i in range( 0, random_pick ):
        #            if temp_list[ i ] == '0':
        #                temp_list[ i ] = '1'
        #    individual.binary_encoding = "".join( temp_list )

    def fitness( self ):

        '''
        Goodness of an individual is evaluated by 
        summing all the absolute errors for a pixel in that
        individual
        '''

        for individual in self.population:

            fitness = np.sum( abs( self.image - individual.image ) )
            individual.fitness = fitness
        
        #self.print_fitness()

        self.sortPopulation()

    def sortPopulation( self ):

        '''
        Population list is ordered by individuals' fitness
        in ascending order so that the 0th element is always
        the fittest
        '''
        
        for i in range( len(self.population) - 1):
            for j in range( i , len(self.population) ):
                if self.population[ i ].fitness > self.population[ j ].fitness:
                    tempIndividual = self.population[ j ]
                    self.population[ j ] = self.population[ i ]
                    self.population[ i ] = tempIndividual
        
 
        
        self.population = self.population[ 0 : self.pop_size ]
                
    def encoding( self ):

        '''
        Population is encoded into binary strings obtained by
        concatenation of 8bit long substrings representing 
        the relevant attributes of an individual  
        '''
        
        for individual in self.population:
            binary_encoding = ""
            for rect in individual.rectangles:                
                binary_encoding += bin( rect.up_left_vertex[0] ).split('0b')[ 1 ].zfill( self.bit )
                binary_encoding += bin( rect.up_left_vertex[1] ).split('0b')[ 1 ].zfill( self.bit )
                binary_encoding += bin( rect.down_right_vertex[0] ).split('0b')[ 1 ].zfill( self.bit )
                binary_encoding += bin( rect.down_right_vertex[1] ).split('0b')[ 1 ].zfill( self.bit )
                binary_encoding += bin( rect.red ).split('0b')[ 1 ].zfill( self.bit )
                binary_encoding += bin( rect.green ).split('0b')[ 1 ].zfill( self.bit )
                binary_encoding += bin( rect.blue ).split('0b')[ 1 ].zfill( self.bit )
            individual.binary_encoding =  binary_encoding 

    def show_image( self ):

        '''
        Shows the target image
        '''

        #DONE - Other system for showing an image
        #TO DO - THE IMAGE REMAINS PENDING
        
        img = Image.fromarray( self.image )
        img.show()

    def save_image( self, individual ):

        '''
        Saves the image obtained from the entire
        population
        '''

        #TO DO - THE IMAGE REMAINS PENDING
        
        img = Image.new('RGB', ( self.pixel_x, self.pixel_y ) )
        drw = ImageDraw.Draw(img, 'RGBA')
        for rect in individual.rectangles:
           drw.rectangle( [ rect.up_left_vertex, rect.down_right_vertex ], ( rect.red, rect.green, rect.blue, 120) )
       
        img.save( 'image-learning/generated-images/image_gencount' + str( self.generation_count ) + '.jpg' )
        del drw

    def genImage( self, individual ):

        img = Image.new( 'RGB', ( self.pixel_x, self.pixel_y ) )
        drw = ImageDraw.Draw( img, 'RGBA' )
        for rect in individual:
            drw.rectangle( [rect.up_left_vertex,rect.down_right_vertex], ( rect.red, rect.green, rect.blue, 120 ) )
        
        img_as_array = np.asarray( img , dtype='int16')
                
        del img, drw
        return img_as_array

    def gen_image( self ):

        '''
        Generates an image starting from the population
        '''

        #IMPROVE OOP REPRESENTATION

        for individual in self.population:
            individual.image = self.genImage( individual.rectangles ) 


    def update_pop( self ):

        for individual in self.population:
            individual.update()

    def print_fitness( self ):

        '''
        Prints the details of each individual in the population
        '''

        print('POPULATION FITNESS at ' + str( self.generation_count ) + '\n')
        i=0
        for individual in self.population:
           print( 'FITNESS ' + str(i), individual.fitness )
           i += 1
        print()

    def evolve( self ):

        '''
        Performs the entire evolution cycle of the
        GA
        '''

        self.init_population()
        
        try:
            while( True ):
                self.gen_image()
                self.fitness()
                #self.print_fitness()           
                self.crossing_over()
                self.mutation()
                self.update_pop()         
                self.gen_image()                      
                self.fitness()         
                if self.generation_count % 1000 == 0 :
                    self.print_fitness()
                    self.save_image( self.population[0] )
                self.generation_count += 1
                if self.generation_count == 400000:
                    self.save_image( self.population[0] )
                    break
                    
        except KeyboardInterrupt:
            print ("\nInterrupted by user\n")
            self.print_fitness()
            self.save_image( self.population[0] )
            

if __name__ == '__main__':

    im = ImageLearning( {'pop_size':10} )
    im.show_image()
    im.evolve()