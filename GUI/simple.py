import PySimpleGUI as sg

def about():
    sg.popup("This is a simple GUI for reading chess games. It was created using PySimpleGUI. You can download it from https://github.com/YourName/ChessProject")

def create_file(file_path, content):
    """Function that creates a file with the given file path and content."""
    with open(file_path, "w") as f:
        f.write(content)

def main():
    layout = [
        [sg.Text("Please choose an option:")],
        [sg.Radio("Input a local PGN file", "input", default=True), sg.FileBrowse()],
        [sg.Radio("Write a URL from chessgames.com website", "input"), sg.InputText()],
        [sg.Radio("Input a local text file containing a list of URLs from chessgames.com website", "input"), sg.FileBrowse()],
        [sg.Text("Please choose a color:")],
        [sg.Radio("White", "color", default=True), sg.Radio("Black", "color"), sg.Radio("Both", "color")],
        [sg.Button("Help"), sg.Button("About"), sg.Button("Generate"), sg.Button("OK")]
    ]

    window = sg.Window("Chess Game Input", layout)

    while True:
        event, values = window.read()
        file_path = None
        content = None
        url = None
        
        if event == "OK":
            input_type = values[0]
            file_path = None
            content = None
            if input_type == "Input a local PGN file":
                file_path = values[1]
                content = file_path
            elif input_type == "Write a URL from chessgames.com website":
                url = values[2]
                content = url
            elif input_type == "Input a local text file containing a list of URLs from chessgames.com website":
                file_path = values[3]
                content = file_path
            color = values[4]
            content += "\n" + color
        elif event == "Generate":
            if (file_path is None) and (url is None):
                sg.popup("You must select an input option and provide a file path or a url before generating a file.")
            else:
                create_file(file_path + ".txt", content)
                sg.popup(f"File {file_path}.txt created with success.")
        elif event == "Help":
            sg.popup("This GUI allows you to input chess games in various forms. You can input a local PGN file, a single URL from chessgames.com website, or a local text file containing a list of URLs from chessgames.com website. You can also choose a color for the games you input.")
        elif event == "About":
            about()
        elif event in (None, "Cancel"):
            break
    window.close()

if __name__ == '__main__':
    main()
