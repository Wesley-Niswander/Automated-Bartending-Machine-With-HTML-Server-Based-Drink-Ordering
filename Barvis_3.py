#This code relies on a sh script to apply certain overlays (Desktop/Overlays.sh)
#This runs at startup after adding it to crontab
#crontab -e
#@reboot sh /home/wesniswander/Desktop/Overlays.sh

import json
from GPIO_class import gpioGet
from Stepper_class import step
from Dispensing_Class import dispenser

def runBarvis(drink):
    ingredientNumber = 0
    # states = ['Load','Home','GetNext','Move','Dispense','Recenter']
    keys = ["vodka","gin","light rum","dark rum","tequila","triple sec","cranberry juice","orange juice","pineapple juice","passion fruit juice","lime juice","sour mix"]
    
    def SP(num):
            s = 30
            o = 120
            return s + o*num
    positions = [SP(0),SP(2),SP(3),SP(3),SP(4),SP(5),SP(6),SP(7),SP(8),SP(9),SP(10),SP(11)] #order of positions must match order of keys
    valves = [0,2,3,3,4,5,6,7,8,9,10,11]
    #Note: valve 1 seems to be not working. Moving gin to valve 2 and throwing both dark and light rum on valve 3
    print("Variables initialized")
    #initialize key variables

    motor = step(1,84,1,86,"/sys/class/pwm/pwmchip0/pwm0",5000000,2500000)
    print("Motor initialized")
    #initialize step class for motor

    pour = dispenser('/dev/ttyAML6',115200,1.26847)
    print("Dispensing controller initialized")

    limitSwitch = gpioGet(1,98)
    print("Limit switch initialized")
    #Initialize limit switch used during homing

    state = "Load"
    print("state => Load")
    #Create states enum for controlling states in the state machine. Initialize to load

    stop = False
    try: #If the code hangs for any reason we need to exit and make sure moving components are set to off!
        while stop == False: #State machine flow: Load > Home > GetNext > Move > Dispense > GetNext > 
            # Move > Dispense ... > GetNext > "exits loop"
            if state == "Load":  #Load JSON recipe file based on 'drink' input to function runBarvis
                try:
                    print("Loading JSON recipe file for "+drink)
                    f = open("recipes/"+drink+".json")
                    recipe = json.load(f)
                    f.close()
                    print("JSON recipe file loaded")
                    #Open recipe file and extract json data

                    print('Drink '+drink+' recipe:')
                    for ii in recipe:
                        print(ii + ":"+str(recipe[ii]))
                    #Print recipe to terminal for diagnostics

                    state = "Home"
                    print("state => Home")
                    #change state to home
                except:
                    stop = True
                    print("Error loading JSON recipe file for "+drink)
                    #Error loading json recipe. Print error message to termnal and exit state machine

            elif state == "Home": #Perform homing routine. Motor moves left until limit switch is hit. 
            
                print('Begin homing routine...')

                motor.enable("on")
                print('Motor enabbled')
                #Enable motor. Motor should be disabled between runs to avoid overheating

                homingSteps = 0
                for jj in range(1000):
                    #for loop so it doesn't run until infinity if something fails

                    motor.move("cw",1,False)
                    homingSteps = homingSteps + 1
                    print("Homing step: "+str(homingSteps))
                    #Move motor one step

                    homed = limitSwitch.get()
                    print("Homing switch value = "+str(homed))
                    #Get the value of the limit switch

                    if homed == 1:
                        motor.move("off",0,False)
                        motor.zero()
                        print("Motor zeroed")
                        motorPosition = 0
                        print("Homing completed successfully!")
                        break
                        #motor hit limit switch, set motor postion to zero and exit the for loop

                if homed == 0:
                    #check that homing completed successfully, exit if not
                    print("Homing unsuccessful, exiting")
                    stop = True
                else:
                    #Homing is finished, transition to GetNext state
                    state = "GetNext"
                    print("state => GetNext")
                    
            elif state == "GetNext": #Pulls the next ingredient from the recipe  
                print('Getting next ingredient...')

                if ingredientNumber >= len(keys):
                    #Stop conditions, all keys values have been iterated through
                    state = "Recenter"
                    print("No more ingredients")
                    print("Recipe completed successfully!")
                    print("state => Recenter")
                else:
                    if keys[ingredientNumber] in recipe:
                        #The current key was found in the recipe

                        ingredient = keys[ingredientNumber]
                        volume = recipe[keys[ingredientNumber]]
                        positionIndex = ingredientNumber
                        #index for the positions array to tell the motor where to go. Converting to zero indexing because
                        #numpy arrays zero index while enums do not ("that's fun" *he said sarcastically...*)
                        print(str(ingredient+" volume = "+str(volume)))
                        #Pull ingredient and volume out of recipe

                        state = "Move"
                        print("state => Move")
                        #Transition to move state
                    else:
                        #The recipe does not contain the current key, skip and try the next key
                        print(keys[ingredientNumber]+": ingredient not in recipe, skipping")
                        state = "GetNext"
                        print("state => GetNext")


                    ingredientNumber = ingredientNumber + 1

            elif state == "Move": #Moves the motor to the ingredient's valve position
                print('Starting motor move to '+str(ingredient)+ ' at position '+ str(positions[positionIndex]))
                print('Current motor position = '+str(motorPosition))
                steps2move = positions[positionIndex]-motorPosition
                print('Steps to move ' + str(steps2move))
                #Calculate steps to move to hit target position

                if steps2move > 0: #positive move to the right, turn motor ccw
                    motorPosition = motor.move("ccw",steps2move,True)
                else: #negative move to the left, turn motor cw (same as homing)
                    motorPosition = motor.move("cw",abs(steps2move),True)
                print('Move completed successfully')
                #Move the motor cw or ccw depending on the direction of the move

                state = "Dispense"
                startDispensing = True
                print('state => Dispense')
                #State is set to Dispense. startDispensing is set True. This variable triggers the sending of the command
                #to dispense to the Arduino
           
            elif state == "Dispense":
                if startDispensing == True:
                    print('Starting dispensing')
                    pour.pour(int(valves[positionIndex]),volume)
                    startDispensing = False
                # The first iteration of this state sends the command to pour the volume/weight from the valve.
                # The variable startDispensing is set false so that it doesn't spam the command.

                pourStatus = pour.done()

                if pourStatus == "DONE":
                    state = "GetNext"

                if pourStatus == "TIMEOUT":
                    print("Failed to dispense " +str(volume) + "oz of "+str(ingredient))
                    print("Check cup is on platform and that liquid is in the source vessel")
                    stop = True
                #An error occured where the scale did not recieve the correct volume in a 2 minute
                #timeout period. Exiting...
            
            elif state == "Recenter":
                #Recipe is done, recentering the platform
                print("Recentering platform...")

                steps2move = positions[5]-motorPosition
                print('Steps to move ' + str(steps2move))
                #Calculate steps to move to hit target position

                if steps2move > 0: #positive move to the right, turn motor ccw
                    motorPosition = motor.move("ccw",steps2move,True)
                else: #negative move to the left, turn motor cw (same as homing)
                    motorPosition = motor.move("cw",abs(steps2move),True)
                print('Recenter move completed successfully')

                stop = True #stop condition of main loop
                
    except Exception as e: #Error occured in main loop, main loop exited, displaying message...
        print('Exiting: recipe completed unsuccessfully')
        print('Error message: ',end='')
        print(e)
    motor.enable("off")
    print("Motor disabled")
    print("Done")