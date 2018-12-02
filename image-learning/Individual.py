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

    def __init__( self, num_rectangles, gray_encoding, pixel_x, pixel_y ):
        self.num_rectangles = num_rectangles
        self.bit = 8
        self.alleles = 7 * self.bit
        self.gray_encoding = gray_encoding 
        self.rectangles = self.decoding()
        self.fitness = 0
        self.image = np.zeros( ( pixel_x, pixel_y, 3 ) , dtype = 'int16' )

    @staticmethod
    def toGrayCode( binary_encoding ):

        '''
        Performs conversion from decimal representation to Gray Code 
        '''

        _xor = {("0", "0"): "0",
        ("0", "1"): "1",
        ("1", "0"): "1",
        ("1", "1"): "0"}

        gray_encoding = []
        gray_encoding.append( binary_encoding[ 0 ] )
        temp = binary_encoding[ 0 ]
        for el in binary_encoding[ 1: ]:
            gray_encoding.append( _xor[ el, temp ] )
            temp = el

        return "".join( gray_encoding)
    
    def fromGrayCode( self, gene ): 

        '''
        Performs conversion from Gray Code to decimal representation
        '''

        _xor = {("0", "0"): "0",
        ("0", "1"): "1",
        ("1", "0"): "1",
        ("1", "1"): "0"}

        binary_encoding = []
        binary_encoding.append( gene[ 0 ] )
        temp = gene[0]
        for el in gene[1:]:
            temp = _xor[temp, el]
            binary_encoding.append( temp )

        decimal_encoding = 0
        for i in range( len( binary_encoding ) ):
            decimal_encoding += 2 ** ( len( binary_encoding ) - i - 1 ) * int( binary_encoding[ i ] )
        return decimal_encoding

    def decoding( self ):
     
        '''
        Population is decoded from binary strings in order
        to form new Individual objects
        '''
        
        rectangles = []
        for i in range( 0, self.num_rectangles * self.alleles, self.alleles ):
            up_left_vertex0 = self.fromGrayCode( self.gray_encoding[ i : i + 8 ] )
            up_left_vertex1 = self.fromGrayCode( self.gray_encoding[ i + 8 : i + 16 ] )
            down_right_vertex0 = self.fromGrayCode( self.gray_encoding[ i + 16 : i + 24 ] )
            down_right_vertex1 = self.fromGrayCode( self.gray_encoding[ i + 24 : i + 32 ] )
            red = self.fromGrayCode( self.gray_encoding[ i + 32 : i + 40 ] )
            green = self.fromGrayCode( self.gray_encoding[ i + 40 : i + 48 ] )
            blue = self.fromGrayCode( self.gray_encoding[ i + 48 : i + 56 ] )
            rectangle = Rectangle( up_left_vertex0, up_left_vertex1, down_right_vertex0, down_right_vertex1, red, green, blue )
            rectangles.append( rectangle )
    
        return rectangles
        
    def update( self ):
        self.rectangles = self.decoding()