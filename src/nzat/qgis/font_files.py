import glob
import os


def font_files(paths):
    found = []
    for path in paths:
        if os.path.isdir(path):
            found.extend(sorted(glob.glob(os.path.join(path, "*.otf"))))
            found.extend(sorted(glob.glob(os.path.join(path, "*.ttf"))))
        elif os.path.isfile(path):
            found.append(path)
    return found
