#!/usr/bin/env python3

import math


'''
Channel type constants
'''
class ChannelTypes:
    voltage = 0
    resistor = 1
    inamp = 2
    photo = 3

'''
    Converter functions
'''
class Edaq530Converters(object):
    ADC_RES = 0.001220703
    PULLUP_RESISTANCE = 10000
    THERM_R_25 = 10000
    THERM_B = 3977

    '''
    Converts A/D converter code to voltage
    '''
    def adcCodeToVoltage(self,d):
        return d * self.ADC_RES

    '''
    Converts A/D converter code to voltage, and the voltage to resistance
    '''
    def adcCodeToResistance(self,d):
        u = self.adcCodeToVoltage(d)
        u /= 5.0
        return u * (self.PULLUP_RESISTANCE / (1.0 - u))

    '''
    Converts A/D converter code to temperature in Kelvin (Thermistor resistance)
    '''
    def adcCodeToTempKelvin(self,d):
        r = self.adcCodeToResistance(d)
        return 1.0 / ((1.0 / 298.16) + ((1.0 / self.THERM_B) * math.log(r / self.THERM_R_25)))

    '''
    Converts A/D converter code to temperature in Celsius (Thermistor resistance)
    '''
    def adcCodeToTempCelsius(self,d):
        return self.adcCodeToTempKelvin(d) - 273.16
