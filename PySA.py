
from math import exp
from random import random, seed

class PySA:
    """
    Simulated Annealling Class v0.1
    http://acm.zhihua-lai.com
    """

    """
        private atrributes
    """
    __coolingfactor = 0.05
    __temp = 28.0
    __stab = 28.0
    __freztemp = 0.0
    __stabfact = 1.005
    __curenergy = 0.0

    """
        method pointers
    """
    generateNew = None
    generateNB = None
    acceptNB = None

    """
        properties wrappers
    """
    def __gettemp(self):
        return self.__temp

    def __settemp(self, temp):
        self.__temp = temp

    def __getcoolf(self):
        return self.__coolingfactor

    def __setcoolf(self, coolingf):
        self.__coolingfactor = coolingf

    def __getstab(self):
        return self.__stab

    def __setstab(self, stab):
        self.__stab = stab

    def __getfreztemp(self):
        return self.__freztemp

    def __setfreztemp(self, freztemp):
        self.__freztemp = freztemp

    def __getstabfact(self):
        return self.__stabfact

    def __setstabfact(self, stabfact):
        self.__stabfact = stabfact

    def __getenergy(self):
        return self.__curenergy

    def __setenergy(self, energy):
        self.__curenergy = energy

    """
        properties
    """
    Temperature = property(__gettemp, __settemp)
    CoolingFactor = property(__getcoolf, __setcoolf)
    Stabilizer = property(__getstab, __setstab)
    FreezingTemperature = property(__getfreztemp, __setfreztemp)
    StabilizingFactor = property(__getstabfact, __setstabfact)
    CurrentEnergy = property(__getenergy, __setenergy)
    
    """
        constructor
    """
    def __init__(self):
        seed()        

    """
        probability function
    """
    @staticmethod
    def ComputeProb(temp, delta):
        if delta < 0:
            return True
        else:
            return random() < exp(-delta / temp)

    """
        prepare
    """
    def Prepare(self):
        assert(self.generateNew != None)
        assert(self.generateNB != None)
        assert(self.acceptNB != None)
        self.CurrentEnergy = self.generateNew()        

    """
        do one step and return if finished
    """
    def Step(self):
        if self.Temperature > self.FreezingTemperature:
            i = 0
            while i < self.Stabilizer:
                energy = self.generateNB()
                delta = energy - self.CurrentEnergy
                if PySA.ComputeProb(self.Temperature, delta):
                    self.acceptNB()
                    self.CurrentEnergy = energy
                i += 1
            self.Temperature -= self.CoolingFactor
            self.Stabilizer *= self.StabilizingFactor
            return False
        self.Temperature = self.FreezingTemperature
        return True
    
    
