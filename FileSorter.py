from pathlib import *
from tkinter import filedialog
from tkinter import *
import shutil



defaultPath = Path("C:/Users/Richard/Documents/Productivity/Photography and Videography/Photoshoots")
defaultRAWType = ".ARW"


def selectPhotoshoot():
    root = Tk()
    root.withdraw()
    directory_selected = filedialog.askdirectory(initialdir=defaultPath)
    selectedPath = Path(directory_selected)
    return selectedPath

def createRawFolder(photoshootDirectory: Path):
    raw_path = photoshootDirectory.joinpath("RAW")
    if raw_path.exists():
        print("RAW Folder Exists")
    else:
        raw_path.mkdir(parents= True, exist_ok= True)
        print("RAW Folder Created")
    return raw_path

def createJPEGFolder(photoshootDirectory: Path):
    jpeg_path = photoshootDirectory.joinpath("JPEG")
    if jpeg_path.exists():
        print("JPEG Folder Exists")
    else:
        jpeg_path.mkdir(parents= True, exist_ok= True)
        selections_path = jpeg_path.joinpath("Selections")
        selections_path.mkdir(parents= True, exist_ok= True)
        print("JPEG and Selections Folder Created")
    return jpeg_path

def sortFiles(photoshootDirectory: Path, rawDirectory, jpegDirectory):
    for f in photoshootDirectory.iterdir():
        if f.suffix == defaultRAWType:
            shutil.move(f, rawDirectory.joinpath(f.name))
        elif f.suffix == ".JPG":
            shutil.move(f, jpegDirectory.joinpath(f.name))

def selectSelectionsDirectory(photoshootDirectory: Path):
    root = Tk()
    root.withdraw()
    directory_selected = filedialog.askdirectory(initialdir=photoshootDirectory.joinpath("JPEG"))
    selectedPath = Path(directory_selected)
    return selectedPath

def createSelectionsInRaw(selectionsDirectory: Path, rawDirectory: Path):
    selectionsName = selectionsDirectory.stem
    selections_in_raw = rawDirectory.joinpath(selectionsName)
    selections_in_raw.mkdir(parents= True, exist_ok= True)

    raws_not_found = []
    for p in selectionsDirectory.iterdir():
        raw_equivalent = p.stem + (".ARW")
        if selections_in_raw.joinpath(raw_equivalent).exists() == False:
            try:
                shutil.move(rawDirectory.joinpath(raw_equivalent), selections_in_raw.joinpath(raw_equivalent))
            except FileNotFoundError:
                raws_not_found.append(raw_equivalent)

    return raws_not_found


if __name__ == "__main__":
    photoshootDirectory = selectPhotoshoot()
    raw_path = createRawFolder(photoshootDirectory)
    jpeg_path = createJPEGFolder(photoshootDirectory)
    sortFiles(photoshootDirectory, raw_path, jpeg_path)
    createAndSortSelections = input("Create and sort selections Y/N: ")
    while createAndSortSelections != "Y" and createAndSortSelections != "N":
        createAndSortSelections = input("Createa and sort selections Y/N: ")
    if createAndSortSelections == "N":
        pass
    else:
        selectionsDirectory = selectSelectionsDirectory(photoshootDirectory)
        raws_not_found = createSelectionsInRaw(selectionsDirectory, raw_path)
        if len(raws_not_found) == 0:
            pass
        else:
            print("RAW Files not found:")
            for r in raws_not_found:
                print(r)

    input("Press any key to finish and exit")
