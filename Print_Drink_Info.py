import json
from enum import Enum

def printInfo(drink):
    try:
        print("Loading JSON recipe file for "+drink)
        f = open("recipes/"+drink+".json")
        recipe = json.load(f)
        f.close()
        print("JSON recipe file loaded")
        #Open recipe file and extract json data
    except:
        print("Failed to load json file for" + drink)
        recipe = {"message":"","note":""}
    try:
        Message = recipe["message"]
        Note = recipe["note"]
        Ingredients = ""
        keys = Enum('keys',["vodka","gin","light rum","dark rum","tequila","triple sec","cranberry juice","orange juice","pineapple juice","passion fruit juice","lime juice","sour mix"])
        
        for ii in keys:
            if keys(ii).name in recipe:
                Ingredients = Ingredients + "-" + keys(ii).name + ", " + str(recipe[keys(ii).name]) + " oz\n"
        return Message+"\n"+Ingredients+Note
    except:
        print("Failed to return drink info for " + drink)
        return("")