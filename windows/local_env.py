import platform
import os


projectName = '26032020'

vsCommandPromptX64    = "C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC"
shareLib                 = "C:\\winShareLib"
windowsCmd              = 'C:\\Windows\\system32\\cmd.exe'
signingPasswordRoot = 'C:\\signing'
bitrockInstallation = 'C:\\installBuilder'
projectFileName = 'PGInstaller.xml'

""" Some general variables should not be modified in any case """
root = os.path.dirname(os.path.abspath(__file__))
