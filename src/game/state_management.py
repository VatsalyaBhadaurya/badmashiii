class GameState:
    def __init__(self):
        self.__level = 1
        self.__running = True
        self.__fps = 60
        self.__direction = "r"

    @property
    def direction(self):
        return self.__direction
    
    @direction.setter
    def direction(self, value):
        if value not in ['r','l','u','d']:
            raise ValueError("Unknown direction")
        self.__direction = value
        
    @property
    def level(self):
        return self.__level
    
    @level.setter
    def level(self, value):
        self.__level = value

    @property
    def running(self):
        return self.__running
    
    @running.setter
    def running(self, value):
        self.__running = value

    @property
    def fps(self):
        return self.__fps
    
    @fps.setter
    def fps(self, value):
        self.__fps = value