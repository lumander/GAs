from GeneticAlgorithm import GA
from Individual import Rectangle, Individual
from PIL import Image, ImageDraw
import numpy as np
import json, sys
             

class ImageLearning(GA):

    def __init__( self, parameters ):

        '''
        Constructor of the Class ImageLearning
        '''

        GA.__init__( self, parameters )
        self.rectangles = 32
        self.bit = 8
        self.alleles = 7 * self.bit
        self.population = []
        self.image = np.asarray( Image.open( parameters[ 'path_to_image' ] ) )
        self.pixel_x = len( self.image[0] )
        self.pixel_y = len( self.image )
       
    def init_population( self ):

        '''
        Population is encoded into a list of n Individual objects
        which represents an image of n semi-transparent rectangles
        '''

        random_string = np.random.randint( 0, 2, ( self.pop_size,  self.rectangles * self.alleles ), dtype = 'uint8' )

        for i in range( self.pop_size ):
            binary_encoding = []
            for j in range( self.rectangles * self.alleles ):
                binary_encoding.append( str( random_string[ i, j ] ) )
            gray_encoding = Individual.toGrayCode( "".join( binary_encoding ) )
            ind = Individual( self.rectangles, gray_encoding, self.pixel_x, self.pixel_y )
            self.population.append( ind )
            self.set_images

    def crossing_over( self ):

        '''
        Genes of the population undergo crossing over
        '''
      
        for individual in range( 0 , self.pop_size - 1 , 2 ):
            child_one = []
            child_two = []
            split_point = np.random.randint( 0, self.rectangles * self.alleles )
            for i in range( 0, split_point ):
                child_one.append( self.population[ individual ].gray_encoding[ i ] ) 
                child_two.append( self.population[ individual + 1 ].gray_encoding[ i ] )
            for i in range( split_point, self.rectangles * self.alleles ):
                child_one.append( self.population[ individual + 1 ].gray_encoding[ i ] )
                child_two.append( self.population[ individual ].gray_encoding[ i ] )
            child_one = "".join( child_one )
            child_two = "".join( child_two )
            brother = Individual( self.rectangles, child_one, self.pixel_x, self.pixel_y )
            sister = Individual( self.rectangles, child_two, self.pixel_x, self.pixel_y )
            self.population.append( brother )
            self.population.append( sister )
        
    def mutation( self ):
        
        '''
        Genes undergo random mutations
        '''

        random_individual = np.random.randint( 0, self.pop_size )
        temp_list = list( self.population[ random_individual ].gray_encoding )
        random_pick = np.random.randint( 0, len( temp_list ) )
        if temp_list[ random_pick ] == '0':
            temp_list[ random_pick ]= '1'
        else:
            temp_list[ random_pick ]= '0'
        
        self.population[ random_individual ].gray_encoding = "".join( temp_list )

    def fitness( self ):

        '''
        Goodness of an individual is evaluated by 
        summing all the absolute errors for a pixel in that
        individual
        '''

        for individual in self.population:

            fitness = np.sum( abs( self.image - individual.image ) )
            individual.fitness = fitness

        self.sort_population()

    def sort_population( self ):

        '''
        Population list is ordered by individuals' fitness
        in ascending order so that the 0th element is always
        the fittest
        '''
        
        for i in range( len( self.population ) - 1 ):
            for j in range( i , len( self.population ) ):
                if self.population[ i ].fitness > self.population[ j ].fitness:
                    tempIndividual = self.population[ j ]
                    self.population[ j ] = self.population[ i ]
                    self.population[ i ] = tempIndividual
                
        self.population = self.population[ 0 : self.pop_size ]
                
    def show_image( self ):

        '''
        Shows the target image
        '''

        img = Image.fromarray( self.image )
        img.show()

    def save_image( self, individual ):

        '''
        Saves the image obtained from the entire
        population
        '''
        
        img = Image.new( 'RGB', ( self.pixel_x, self.pixel_y ) )
        drw = ImageDraw.Draw( img, 'RGBA')
        for rect in individual.rectangles:
           drw.rectangle( [ rect.up_left_vertex, rect.down_right_vertex ], ( rect.red, rect.green, rect.blue, 120 ) )
       
        img.save( 'image-learning/generated-images/image_gencount' + str( self.generation_count ).zfill(6) + '.jpg' )
        del drw

    def gen_image( self, individual ):

        '''
        Generates the image corresponding to an individual
        '''

        img = Image.new( 'RGB', ( self.pixel_x, self.pixel_y ) )
        drw = ImageDraw.Draw( img, 'RGBA' )
        for rect in individual:
            drw.rectangle( [ rect.up_left_vertex,rect.down_right_vertex ], ( rect.red, rect.green, rect.blue, 120 ) )
        
        img_as_array = np.asarray( img , dtype = 'int16' )
                
        del img, drw
        return img_as_array

    def set_images( self ):

        '''
        Updates the images corresponding to the individuals
        '''

        for individual in self.population:
            individual.image = self.gen_image( individual.rectangles ) 

    def update_pop( self ):

        '''
        Updates the population coordinates
        '''

        for individual in self.population:
            individual.update()
        self.set_images()

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
    
    def best ( self ):

        '''
        Returns the best individual in the population which is always
        the 0th by construction
        '''

        return self.population[ 0 ]

    def check( self ):

        '''
        Increments the generation count, prints the status of the iterations,
        blocks the evolution after a fixed number of iterations
        '''

        if self.generation_count % 500 == 0 and self.generation_count != self.max_gen:
            self.print_fitness()
            self.save_image( self.best() )
        self.generation_count += 1
        if self.generation_count == self.max_gen:
            self.save_image( self.best() )
            self.evolution = False
        
    def evolve( self ):

        '''
        Performs the entire evolution cycle of the GA
        '''

        self.show_image()
        self.init_population()
        self.fitness()       

        try:
            while( self.evolution  ):
                
                self.crossing_over()
                self.mutation()
                self.update_pop()                               
                self.fitness()         
                self.check()
                    
        except KeyboardInterrupt:
            print ("\nInterrupted by user\n")
                    
if __name__ == '__main__':

    parameters = json.loads( sys.argv[1] )
    im = ImageLearning( parameters )
    im.evolve()