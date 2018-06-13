import os
import currentDateTime

currentDateTime = currentDateTime.savedDateTime

class Path:
    root = os.path.dirname(os.path.abspath(__file__))
    currentProject = root+ "/workDir/"+ currentDateTime
