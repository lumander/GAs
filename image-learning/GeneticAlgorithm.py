from abc import ABCMeta, abstractmethod

class GA( metaclass = ABCMeta ):

    def __init__( self, parameters ):
        self.pop_size = parameters[ 'pop_size' ]
        self.max_gen = parameters[ 'max_gen' ] 
        self.generation_count = 0
        self.evolution = True
        
    @abstractmethod
    def init_population( self ):
        pass

    @abstractmethod
    def sortPopulation( self ):
        pass

    @abstractmethod
    def crossing_over( self ):
        pass
    
    @abstractmethod
    def mutation( self ):
        pass

    @abstractmethod
    def fitness( self ):
        pass
