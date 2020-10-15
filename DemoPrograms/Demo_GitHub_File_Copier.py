import os.path
import shutil
import subprocess
import sys

import PySimpleGUI as sg

"""
    Demo - GitHub File Management
    
    A program that helps manage the demo programs on a local PC.  This is done by copying files from your working folder to a folder that is kept in sync with GitHub.
    It works well when used in conjunction with the GUI version of GitHub.  
    
    Two folders are shown... 
        * the left side is your local "working copy"
        * the right side is the GitHub folder
    
    The basic file operations are
        * Copy from working folder to GitHub folder
        * Edit a file in PyCharm
        * Run a file (in either folder)
    
    Additional operations
        * Edit this file in PyCharm
        * Launch GitHub GUI program
                
    Copyright 2020 PySimpleGUI.org
"""

DEMO_PATH = r'C:\Python\PycharmProjects\PSG\DemoPrograms'
GIT_DEMO_PATH = r'C:\Python\PycharmProjects\GitHub\PySimpleGUI\DemoPrograms'
GITHUB_PROGRAM = r'C:/Users/mike/AppData/Local/GitHubDesktop/GitHubDesktop.exe'
PYCHARM_BATCHFILE = r"C:\Program Files\JetBrains\PyCharm Community Edition 2019.1.1\bin\pycharm.bat"
ML_KLEY = '-ML-'

# --------------------------------- Main Program Layout ---------------------------------

def main():

    # First the window layout...2 columns

    demo_files = os.listdir(DEMO_PATH)

    left_col = [
        [sg.Text('Demo Programs', font='Any 20')],
        [sg.Listbox(values=demo_files, select_mode=sg.SELECT_MODE_EXTENDED, size=(40, 20), key='-DEMO LIST-')],
        [sg.Text('Filter:'), sg.Input(size=(15, 1), enable_events=True, key='-FILTER-')],

        [sg.Button('Run'),sg.Button('Copy'), sg.B('Edit')]
    ]

    git_demo_files = os.listdir(GIT_DEMO_PATH)

    right_col = [
        [sg.Text('GitHub Demo Programs', font='Any 20')],
        [sg.Listbox(values=git_demo_files, select_mode=sg.SELECT_MODE_EXTENDED, size=(40, 20), key='-GIT DEMO LIST-')],
        [sg.Button('Run', key='Run Git Version')],
    ]

    # ----- Full layout -----
    layout = [[sg.vtop(sg.Column(left_col, element_justification='c')), sg.VSeperator() ,sg.vtop(sg.Column(right_col, element_justification='c'))],
              [sg.HorizontalSeparator()],
              [sg.Multiline(size=(90, 10), write_only=True, key=ML_KLEY, reroute_stdout=True)],
              [ sg.Button('Edit Me (this program) in PyCharm'), sg.B('Launch GitHub', button_color=(sg.theme_input_background_color(), sg.theme_input_text_color())), sg.Button('Exit')],
              ]

    # --------------------------------- Create Window ---------------------------------
    window = sg.Window('GitHub Demo Copier', layout, icon=icon)

    sg.cprint_set_output_destination(window, ML_KLEY)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        if event == 'Copy':
            confirm = sg.popup_yes_no('Are you sure you want to copy:', *values['-DEMO LIST-'], keep_on_top=True)
            if confirm == 'Yes':
                sg.cprint('Copying....', c='white on red')
                for file in values['-DEMO LIST-']:
                    sg.cprint(f'{os.path.join(DEMO_PATH, file)}', text_color='blue')
                    sg.cprint('TO', text_color='red', background_color='white')
                    sg.cprint(f'{os.path.join(GIT_DEMO_PATH, file)}', text_color='green')
                    shutil.copyfile(os.path.join(DEMO_PATH, file), os.path.join(GIT_DEMO_PATH, file))
                sg.cprint('Copy complete', background_color='red', text_color='white')
        elif event == 'Edit':
            for file in values['-DEMO LIST-']:
                sg.cprint(f'opening (in PyCharm)', text_color='white', background_color='red', end='')
                sg.cprint(f' {os.path.join(DEMO_PATH, file)}', text_color='purple')
                execute_command_subprocess(f'{PYCHARM_BATCHFILE}', os.path.join(DEMO_PATH, file))
        elif event == 'Run':
            sg.cprint('Running local program....', c='white on green')
            for file in values['-DEMO LIST-']:
                sg.cprint(os.path.join(DEMO_PATH, file))
                run_py(os.path.join(DEMO_PATH, file))
        elif event == 'Run Git Version':
            sg.cprint('Running GitHub version of program....', c='white on green')
            for file in values['-GIT DEMO LIST-']:
                sg.cprint(os.path.join(GIT_DEMO_PATH, file))
                run_py(os.path.join(GIT_DEMO_PATH, file))
        elif event.startswith('Edit Me'):
            execute_command_subprocess(f'{PYCHARM_BATCHFILE}', __file__)
        elif event == 'Launch GitHub':
            run(GITHUB_PROGRAM)
        elif event == '-FILTER-':
            new_list = [i for i in demo_files if values['-FILTER-'].lower() in i.lower()]
            window['-DEMO LIST-'].update(values=new_list)

    window.close()


def run(app_name, parm=''):
    execute_command_subprocess(app_name, parm)


def run_py(pyfile, parms=None):
    if parms is not None:
        execute_command_subprocess('python', pyfile, parms)
    else:
        execute_command_subprocess('python', pyfile)


def execute_command_subprocess(command, *args, wait=False):

    if sys.platform == 'linux':
        arg_string = ''
        for arg in args:
            arg_string += ' ' + str(arg)
        sp = subprocess.Popen(['python3' + arg_string, ], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        expanded_args = ' '.join(args)
        sp = subprocess.Popen([command, expanded_args], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if wait:
        out, err = sp.communicate()
        if out:
            print(out.decode("utf-8"))
        if err:
            print(err.decode("utf-8"))


if __name__ == '__main__':
    icon = b'iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAMAAAD04JH5AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAMAUExURQAAAB69LymqOSm6LSq2OTSrOjS2Ox28RjqdQC6qSiy3Riu3UTisRzirVDi1STq0UiuyYz6pYz62ZCjDNyjQPzTAOxrIQinARTXDRzXBVEWsP1ieZ0OrSUaqV0S0SkOzVFKnSVKrWlK0W0iqZUWmcEe0a1eoZ1apclW0Z1uzd2G8X2W8Z2i3dXStdnS/ZHW7dkXCTEnCWVnDbF3Gc1zUc2bGbGjId2fRbWjQfnLFbnTGeHfReXu6hWzFgWzRgXfGhn3Jk3bShHvWkd5HPNhYJ9RWPtRbPdxVOtlbM9xdPM5iPNRjO9VsMtNoOttiPOFVNOVUPeNZNOJbPelVPelZN+pcO/ZYPeNjPeFqPOlgNOpiPfBkO8xcR85ZUtZOUNJXQdNcQtNcTNpTRdxVT9xdQ95cSdlbUsBgR8xkRctkTc1oQ81pS8tmVMtxTsx3XtVjQdRjStRoQtNqStxiRNtjSdxpQ9toS9NkU9diWdFqUtVsW9xiU9xlXN5uVtZzWsptZ8Z3Y8p2ddBuY9duat1qY9Nvcdh3Z+VOQ+NUROJcQ+NcSutTROlcQ+pdSuhdVPJcQ/FbS/heQvZbVuFhReJjSeJpRORpTOpiRepiS+toTeVlU/RhRfJhUuZnYeBvaeR4aoPCfN+Hb9eHfNmQfeaIbOKIeOWSefaHbP+Ia/CMffCSePigeoTHhovJmIjWiYXXl5HMnpbYmY3bp4fes5PHoJnapJzUspDhnozjpo3lspnjqaLTm6HOsaPYp7XOuLbduajkqavpuLTpt7f2uKvbwbLYw7nmx7f1ybjw1tqIhtiThtiSkNasnNuimeSLhOWPkOWThuicl/mdiPKbku6fouWjl+Oinuaom+ynl+yjmuqpl+qqm/OllfOlmPSqnf6mkvqhneekoPOho8buuNPtvtbd08bpyMro1cT2ysj109XozNXo2NHzydT52M/45tvs4tj8497+8eD6y+b82+bq6Of+5+n+9fnq7f/p//b96fv7+gAAAAAAAAAAAAAAAAAAAFSfM6AAAAEAdFJOU////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////wBT9wclAAAACXBIWXMAAA7DAAAOwwHHb6hkAAAMlUlEQVR4Xu2Zf5gbRRnHtd5Fm+Z2FUQOuWQplXI+oAVqA0RrAKUlRGINlkCpei2b2EI1187eFUitBfFgc0nah5m7pFsFnvJD1FIseoDFk1/agj+wpz5gBX8geu31ODmtqb39J76zO5vb/Lzsnjw8Pt7nLpfZmcnMd99533dmc28rvMXMCJgRMCNgRsCMgP9tAQdv23jDTYm72JU9piPg5U29W8OB1O2Jl1mFHaYh4I+dS7NAbkeg8yCrsoF9AS9Ge6++Ik6k4BV9qVW/ZJXWsS3gwf4ORDAWZYQwRsqDrNoydgUc7EcwP8KEEEyQiJQh1mAVmwJeIaKI+5EoUiMggpbYVmBPwFDmk0QiWBaxjCmEoCsz9hTYE/D8J65FGIl0AegawGqQCE7YigWbS9DTK4LvYSwDhMjgiShIEnZsYNcJt9DVJ7Iowy8toQ4cxHZWwa6AAiEwM5HJdpm6AZGVDhTptaHAsoDvdr6gF76WvDqckqT1KJ3GCsnIEJNItJ4PrAoYikc3MgWbU6l+HN+AUql0HEFM2MsHFgUMZe7oiq86oF8kRImaPxtAUpdoNx9YEzCUuTIb6pNjTMHdq6Srli3PdgWxGKYxYScfWBJwMIEjIo5Eigq23JpQYitFBefAIe3lAysChhIkiNbnwsFcb2wnqwNe+OYd27YHtZiwkQ8sCBjKQKh3EEgAKEfE+1kt5bZLUdBuPmhcAKx/BHUoadKZjl8euqqXxYLG5kDKbj5oWMCDCpJgkfXNB0DdzA8oQ6uWs2rYnazlg0YFHFRg/4WtH8ysE+k03+W6LKuGPtbyQYMChjIQ4jAwmwWIJFiTxrrPsGrAWj5oTMBQZhlE2KT9gbDC2jTWrWDVOhbyQUMCaPzDmHTg4hKs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'


    main()

