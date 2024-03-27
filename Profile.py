from pyswip import Prolog

# Purpose: get user-preferred variables from user

def getProfile(prolog):
    actions=['study', 'movie', 'sleep', 'clean', 'music']

    type = ['light', 'temp', 'wind', 'noise' ]

    f = open("profilevals.txt", "w")

    text=""
    ftext = ""

    for act in actions:
        if act=="movie":
            action="watching a movie "
        elif act=="music":
            action="listening music"
        else: 
            action= act +"ing"

        text = text + "While the user is " + action + ", he/she want: \n"

        for t in type:
            preference = list(prolog.query("preference(" + act + ", " + t + ", V, E)"))
            text = text + t + " " + str(preference[0]['V']) + "\n"
            ftext += act + "," + t + "," + str(preference[0]['V']) + "\n"

        text = text +"\n\n"

    f.write(ftext)
    f.close()
    
    return text

#function that changes the user preference values
def update_preference(new_profile):
    activity = new_profile['action']
    print(f"activity: {activity}")
    prolog = Prolog()
    prolog.consult('facts.pl')  # Replace 'your_prolog_file.pl' with your Prolog file name

    #different variables and their associated effectors based on different action
    #value[0]: study
    #value[1]: sleep
    #value[2]: movie
    #value[3]: clean
    #value[4]: music
    variableLists = {'light': [['l2', 'rs1'], ['l1', 'l2', 'l3', 'l4', 'rs1', 'rs2'], ['l3', 'l4', 'rs1', 'rs2'], ['l1', 'rs1', 'rs2'], ['l1', 'l2', 'l3', 'l4', 'rs1', 'rs2']],
                    'temp': [['ac', 'r', 'w1', 'w2'], ['ac', 'r', 'w1', 'w2'], ['r', 'w1', 'w2', 'ac'], ['r', 'ac', 'w1', 'w2'], ['ac', 'r', 'w1', 'w2']],
                    'wind': [['w1', 'w2'], ['w1', 'w2'], ['w1', 'w2'], ['w1', 'w2'], ['w1', 'w2']],
                    'noise': [['ac', 'w1', 'w2'], ['ac', 'w1', 'w2'], ['ac', 'w1', 'w2'], ['ac', 'w1', 'w2'], ['ac', 'w1', 'w2']]
                    }

    for variable in variableLists.keys():

        # Retract old preference facts
        query_retract = f"retract(preference({activity}, {variable}, _, _))"
        list(prolog.query(query_retract))

        # Assert new preference facts
        #use the same list of effectors from the orignal preference
        if (activity == 'study'):
            query_assert = f"assertz(preference({activity}, {variable}, {new_profile[variable]}, {variableLists.get(variable)[0]}))"
        
        elif (activity == 'sleep'):
            query_assert = f"assertz(preference({activity}, {variable}, {new_profile[variable]}, {variableLists.get(variable)[1]}))"
        
        elif (activity == 'movie'):
            query_assert = f"assertz(preference({activity}, {variable}, {new_profile[variable]}, {variableLists.get(variable)[2]}))"
        
        elif (activity == 'clean'):
            query_assert = f"assertz(preference({activity}, {variable}, {new_profile[variable]}, {variableLists.get(variable)[3]}))"
        
        else: #if option is music
            query_assert = f"assertz(preference({activity}, {variable}, {new_profile[variable]}, {variableLists.get(variable)[4]}))"
    
        list(prolog.query(query_assert))
        print(f"Preference updated: {activity}, {variable} set to {new_profile[variable]}")