from view import View


# Global variables

view_choices = {
    1: "PySimpleGUIQt",
    2: "Kivy", 
    3: "Flask",
    4: "briefcase"
    }


# Instantiate a Model object 


# 

if __name__ in ('__main__', '__android__'):

    print(view for view in view_choices.values())
    their_choice = input("Select a view: ")
    this_time_around = View(their_choice, languageModel)
    this_time_around.PySimpleGUI_main_loop()
