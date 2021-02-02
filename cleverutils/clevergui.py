"""
A collection of commonly high level functions based on PysSimpleGUI and tailored to the author's current level and style of Python coding.
"""
import PySimpleGUI as sg
from .cleverutils import INSTALL_PATH, ICON_PATH

SG_KWARGS = {"title": "CleverUtils", "keep_on_top": True, "icon": "../cleverutils.ico"}

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
    # sg.change_look_and_feel("DarkAmber")
    # sg.change_look_and_feel("DarkGreen")
    sg.change_look_and_feel("Python")
    # Redirect stdout and stderr to Debug Window:
    sg.set_options(
        message_box_line_width=80,
        debug_win_size=(100, 30),
        icon = str(ICON_PATH),
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
    title = kwargs.get("title") or "CleverUtils"
    if kwargs.get("title"):
        del kwargs['title']
    window = sg.Window(title, layout, keep_on_top=True, element_justification="center")
    event, _ = window.read()
    window.close()
    return event

def text_input(prompt, **kwargs):
    """
    Presents a general purpose prompt for text input using PySimpleGUI.
    Returns the text entered, or None if closed with Cancel or X.
    """
    global SG_KWARGS
    kwargs.update(SG_KWARGS)
    if "password" in prompt.lower():
        kwargs.update({"password_char": "*"})
    kwargs['default_text'] = kwargs.get('default_text') or ""
    return sg.popup_get_text(prompt, **kwargs)

def get_folder(prompt, **kwargs):
    """
    Presents a general purpose prompt for folder selection using PySimpleGUI.
    Returns the selected folder, or None if closed with Cancel or X.
    """
    global SG_KWARGS
    kwargs.update(SG_KWARGS)
    return sg.popup_get_folder(prompt, default_path=kwargs.get("default_path"))

def progress_bar(prompt="", **kwargs):
    """ Returns a PySimpleGUI window object that can be dynamically updated e.g.

    window['progress_r'].update(1, 5)
    window['progress_text'].update("Page 1 of 10")
    window['progress_item'].update("Currently working on this")
    """
    global SG_KWARGS
    kwargs.update(SG_KWARGS)
    title = kwargs.get("title") or "CleverUtils"
    del kwargs['title']
    # Bug in PySimpleGUI with proportional fonts means text updates don't
    # always display fully.  size= is therefore required
    layout = [[sg.Text(" "*40, key="progress_text", size=(30,1))],
            [sg.Text(" "*40, key="progress_item", size=(30,1))],
        [sg.ProgressBar(1, orientation=kwargs.get("orientation") or 'h', size=(kwargs.get("height") or 30, kwargs.get("width") or 15), key='progress_bar')],
        ]
    window = sg.Window(title, layout, **kwargs).Finalize()
    window['progress_text'].update(prompt)
    return window


def set_menu_colours(window, foreground = "#fdcb52", background = "#2c2825"):
    """ Sets the colours of MenuButton menu options """
    try:
        for menu in [
            "1) Upversion",
            "3) Publish",
            "Create Accounts",
            "Browse Files",
        ]:
            window[menu].TKMenu.configure(
                fg=foreground,
                bg=background,
            )
    except:
        pass  # This workaround attempts to change a non-existent menu


def prompt_with_choices(group: str, choices: list, selected_choices: list, radio=False, buttons_func=None):
    """
    Creates a scrollable popup using PySimpleGui checkboxes (default) or radio
    buttons.

    Parameters:
        group: Name of the group/category of choices
        choices: All possible options for selection
        selected_choices: Options to show as selected by default
        radio: If true,
        buttons_func: Optional function name to return additional buttons to be
        appended to layout.  For example, context specific Help button.

    Returns:

    True if user clicks "Accept", otherwise False.
    """
    if group in radio_group:
        layout = [
            [
                sg.Radio(
                    text=choice,
                    group_id=group,
                    key=choice,
                    default=choice in selected_choices,
                )
            ]
            for choice in choices
        ]
    else:
        layout = [
            [sg.Checkbox(text=choice, key=choice, default=choice in selected_choices)]
            for choice in choices
        ]
    buttons = [sg.Button("Accept"), sg.Button("Cancel")]
    buttons_dict = {}
    if buttons_func:
        buttons_dict = buttons_func(group)
        # e.g. {sg.Button("Help"): help_func_for_xyz_group}
        buttons.append([button for button in buttons_dict])
    choices_window = sg.Window(
        f"Classifiers for the {group.title()} group",
        [
            "",
            [
                sg.Column(
                    layout + [buttons],
                    scrollable=True,
                    vertical_scroll_only=True,
                    size=(600, 300),
                )
            ],
        ],
        size=(600, 300),
        resizable=True,
        keep_on_top=SG_KWARGS["keep_on_top"],
        icon=SG_KWARGS["icon"],
    )

    while True:
        event, values = choices_window.read(close=False)
        if event is None or event == "Cancel":
            choices_window.close()
            return False
        if event == "Accept":
            selected_choices.clear()
            selected_choices.extend(k for k in choices if values[k])
            choices_window.close()
            return True
        for button, event_func in buttons_dict.items():
            if event == window[button.ButtonText]:
                event_func()
