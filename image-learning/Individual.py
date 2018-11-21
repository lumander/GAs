import numpy as np

class Rectangle():

    def __init__( self, x1, y1, x2, y2, red, green, blue ):
        
        self.up_left_vertex = ( x1, y1 )
        self.down_right_vertex = ( x2, y2 )
        self.red = red
        self.green = green
        self.blue = blue
    
    def toString( self ):
        print( 'up left vertex ',self.up_left_vertex , '\n' ,
               'down right vertex ', self.down_right_vertex , '\n' ,
               'red ', self.red , '\n' ,
               'green ', self.green , '\n' ,
               'blue ', self.blue , '\n' )
    
class Individual():



    def __init__( self, num_rectangles, binary_encoding, pixel_x, pixel_y ):
        self.num_rectangles = num_rectangles
        self.bit = 8
        self.alleles = 7 * self.bit
        self.binary_encoding = binary_encoding
        self.rectangles = self.decoding()
        self.fitness = 0
        self.image = np.zeros( ( pixel_x, pixel_y, 3 ) , dtype='int16' )

    def decoding( self ):
     
        '''
        Population is decoded from binary strings in order
        to form new Individual objects
        '''
        rectangles = []
        for i in range( 0, self.num_rectangles * self.alleles, self.alleles ):
            up_left_vertex0 = self.string_decoding( self.binary_encoding[ i : i+8 ] )
            up_left_vertex1 = self.string_decoding( self.binary_encoding[ i+8 : i+16 ] )
            down_right_vertex0 = self.string_decoding( self.binary_encoding[ i+16 : i+24 ] )
            down_right_vertex1 = self.string_decoding( self.binary_encoding[ i+24 : i+32 ] )
            red = self.string_decoding( self.binary_encoding[ i+32 : i+40 ] )
            green = self.string_decoding( self.binary_encoding[ i+40 : i+48 ] )
            blue = self.string_decoding( self.binary_encoding[ i+48 : i+56 ] )
            rectangle = Rectangle( up_left_vertex0, up_left_vertex1, down_right_vertex0, down_right_vertex1, red, green, blue )
            rectangles.append( rectangle )
    
        return rectangles

    def string_decoding( self, genes ): 

        '''
        Performs binary to decimal conversion of the genes
        '''

        

        _xor = {("0", "0"): "0",
        ("0", "1"): "1",
        ("1", "0"): "1",
        ("1", "1"): "0"}

        result = prec = genes[0]
        for el in genes[1:]:
            prec = _xor[prec, el]
            result += prec

        decimals = []
        nmbr = 0
                   
        for i in range( len( result ) ):
            nmbr += 2 ** ( len( result ) - i - 1 ) * int( result[ i ] )
        decimals.append( nmbr )
        return decimals[0]
        

    def update( self ):
        self.rectangles = self.decoding()

    def toGrayCode( self ):
        _xor = {("0", "0"): "0",
        ("0", "1"): "1",
        ("1", "0"): "1",
        ("1", "1"): "0"}


        result = prec = self.binary_encoding[0]
        for el in self.binary_encoding[1:]:
            result += _xor[el, prec]
            prec = el

        self.binary_encoding = result


             