from view import View


# Global variables

view_choices = {
    0: "PySimpleGUIQt",
    1: "Kivy",
    2: "Flask",
    3: "briefcase"
    }


# Instantiate a Model object 


# 

if __name__ in ('__main__', '__android__'):

    for i, choice in enumerate(view_choices.values()):
        print(f"{i}: {choice}")
    their_choice = view_choices[int(input("Select a view: "))]
    this_time_around = View(their_choice)
    this_time_around.PySimpleGUI_main_loop()
