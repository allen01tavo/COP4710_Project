'''
Created on Jun 22, 2017

@author: gmaturan
'''

import calculator as cal
import intro as intro

def main():
    
    #introduction only last 10 seconds
    intro.intro().flash_screen()
    cal.calculator('HEALTH-Que')
    print("System is ready to start")
    print("Application is ready")
    
#call main function
main()
