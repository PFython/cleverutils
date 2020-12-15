"""
A collection of commonly high level functions based on PysSimpleGUI and tailored to the author's current level and style of Python coding.
"""
import PySimpleGUI as sg

sg_options = {"title": "CleverSession", "keep_on_top": True}

def start_gui(*args, **kwargs):
    """
    Toggles between normal output and routing stdout/stderr to PySimpleGUI

    redirect: send (almost) all stdout/stderr to Debug Window & replace print()
    """
    if kwargs.get("redirect"):
        global print
        old_print = print
        print = sg.Print
        options = {"do_not_reroute_stdout": False, "keep_on_top": True}
        print(**options)
        print("Rerouting stdout/stderr to PySimpleGUI Debug Window...")
    sg.change_look_and_feel("DarkAmber")
    # Redirect stdout and stderr to Debug Window:
    sg.set_options(
        message_box_line_width=80,
        debug_win_size=(100, 30),
        icon = "cleverutils.ico",
        font = "calibri 12",
    )

def button_menu(choices: iter, prompt=None, **kwargs):
    """
    Presents a general purpose button selection menu using PySimpleGUI.
    Returns the text of the selected button (the 'event')
    """
    prompt = prompt or "Please select a website:"
    width = max([len(x) for x in choices]) +2
    layout=[[sg.Text(prompt, font="calibri 14 bold")]]
    layout.extend(
            [[sg.Button(button_text=url, size=(width,1), font="calibri 12")]
                for url in choices])
    layout.extend([[sg.Text("You can use Tab & Space to navigate", font="calibri 11 italic")]])
    title = kwargs.get("title") or "cleversession"
    window = sg.Window(title, layout, keep_on_top=True, element_justification="center")
    event, _ = window.read()
    window.close()
    return event

def text_input(prompt, **kwargs):
    """
    Presents a general purpose prompt for text input using PySimpleGUI.
    Returns the text entered, or None if closed with Cancel or X.
    """
    global sg_options
    kwargs.update(sg_options)
    if "password" in prompt.lower():
        kwargs.update({"password_char": "*"})
    kwargs['default_text'] = kwargs.get('default_text') or ""
    return sg.popup_get_text(prompt, **kwargs)
