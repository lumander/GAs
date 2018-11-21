from abc import ABCMeta, abstractmethod

class GA( metaclass = ABCMeta ):

   def __init__( self, parameters ):
        self.pop_size = parameters[ 'pop_size' ] 
        self.generation_count = 0
        
    @abstractmethod
    def init_population( self ):
        pass

    @abstractmethod
    def sortPopulation( self ):
        pass

    #@abstractmethod
    #def encoding( self ):
    #    pass

    #@abstractmethod
    #def decoding( self ):
    #    pass

    @abstractmethod
    def crossing_over( self ):
        pass
    
    @abstractmethod
    def mutation( self ):
        pass


    @abstractmethod
    def fitness( self ):
        pass
