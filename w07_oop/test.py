class Animal:
    def __init__(self, age, color, race):
        self.__age = age
        self.__color = color
        self.__race = race
        pass
    @property
    def age(self):
        return self.__age
    
    @property
    def color(self):
        return self.__color
    
    @property
    def race(self):
        return self.__race

    
    def changeRace(self, race):
        self.__race = race
        pass
    
class Doggo(Animal):
    def __init__(self, age, color, race, sound):
        super().__init__(age, color, race)
        self.__sound = sound
        
    def makeSound(self):
        print("Delam " + self.sound[::-1])

import pyautogui

pejsanek = Doggo(1, "black", "jezevcik", "stemberk")
pejsanek.makeSound()
print(f'{pejsanek.age}')
