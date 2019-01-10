# -*- coding: utf-8 -*-

"""
Script which builds a .jsx file, sends it to After Effects and then waits for data to be returned. 
"""
import os, sys, subprocess, time, _winreg, ctypes

# Tool to get existing windows, usefull here to check if AE is loaded
class CurrentWindows():
    def __init__(self):
        self.EnumWindows = ctypes.windll.user32.EnumWindows
        self.EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
        self.GetWindowText = ctypes.windll.user32.GetWindowTextW
        self.GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
        self.IsWindowVisible = ctypes.windll.user32.IsWindowVisible

        self.titles = []
        self.EnumWindows(self.EnumWindowsProc(self.foreach_window), 0)

    def foreach_window(self, hwnd, lParam):
        if self.IsWindowVisible(hwnd):
            length = self.GetWindowTextLength(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            self.GetWindowText(hwnd, buff, length + 1)
            self.titles.append(buff.value)
        return True

    def getTitles(self):
        return self.titles

# A Mini Python wrapper for the JS commands...
class AE_JSWrapper(object):
    def __init__(self, aeVersion = "", returnFolder = ""):
        self.aeVersion = aeVersion

        # Try to find last AE version if value is not specified
        if not len(self.aeVersion):
            self.aeVersion = str(int(time.strftime("%Y")[2:]) - 3) + ".0"

        # Get the AE_ exe path from the registry. 
        try:
            self.aeKey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Adobe\\After Effects\\" + self.aeVersion)
        except:
            print "ERROR: Unable to find After Effects version " + self.aeVersion + " on this computer\nTo get correct version number please check https://en.wikipedia.org/wiki/Adobe_After_Effects\nFor example, \"After Effect CC 2019\" is version \"16.0\""
            sys.exit()

        self.aeApp = _winreg.QueryValueEx(self.aeKey, 'InstallPath')[0] + 'AfterFX.exe'          

        # Get the path to the return file. Create it if it doesn't exist.
        if not len(returnFolder):
            returnFolder = os.path.join(os.path.expanduser('~'), "Documents", "temp", "AePyJsx")
        self.returnFile = os.path.join(returnFolder, "ae_temp_ret.txt")
        if not os.path.exists(returnFolder):
            os.mkdir(returnFolder)
        
        # Ensure the return file exists...
        with open(self.returnFile, 'w') as f:
                f.close()  
            
        # Establish the last time the temp file was modified. We use this to listen for changes. 
        self.lastModTime = os.path.getmtime(self.returnFile)         
        
        # Temp file to store the .jsx commands. 
        self.tempJsxFile = os.path.join(returnFolder, "ae_temp_com.jsx")
        
        # This list is used to hold all the strings which eventually become our .jsx file. 
        self.commands = []    

    def openAE(self):
        """Pass the commands to the subprocess module."""    
        target = [self.aeApp]
        ret = subprocess.Popen(target)
    
    # This group of helper functions are used to build and execute a jsx file.
    def jsNewCommandGroup(self):
        """clean the commands list. Called before making a new list of commands"""
        self.commands = []

    def jsExecuteCommand(self):
        """Pass the commands to the subprocess module."""
        self.compileCommands()        
        target = [self.aeApp, "-ro", self.tempJsxFile]
        ret = subprocess.Popen(target)
    
    def addCommand(self, command):
        """add a command to the commands list"""
        self.commands.append(command)

    def compileCommands(self):
        with open(self.tempJsxFile, "wb") as f:
            for command in self.commands:
                f.write(command)

    def jsWriteDataOut(self, returnRequest):
        """ An example of getting a return value"""
        com = (
            """
            var retVal = %s; // Ask for some kind of info about something. 
            
            // Write to temp file. 
            var datFile = new File("[DATAFILEPATH]"); 
            datFile.open("w"); 
            datFile.writeln(String(retVal)); // return the data cast as a string.  
            datFile.close();
            """ % (returnRequest)
        )

        returnFileClean = "/" + self.returnFile.replace("\\", "/").replace(":", "").lower()
        com = com.replace("[DATAFILEPATH]", returnFileClean)

        self.commands.append(com)
        
        
    def readReturn(self):
        """Helper function to wait for AE to write some output for us."""
        # Give time for AE to close the file...
        time.sleep(0.1)        
        
        self._updated = False
        while not self._updated:
            self.thisModTime = os.path.getmtime(self.returnFile)
            if str(self.thisModTime) != str(self.lastModTime):
                self.lastModTime = self.thisModTime
                self._updated = True
        
        f = open(self.returnFile, "r+")
        content = f.readlines()
        f.close()

        res = []
        for item in content:
            res.append(str(item.rstrip()))
        return res
    
    
# An interface to actually call those commands. 
class AE_JSInterface(object):
    
    def __init__(self, aeVersion = "", returnFolder = ""):
        self.aeWindowName = "Adobe After Effects"
        self.aeCom = AE_JSWrapper(aeVersion, returnFolder) # Create wrapper to handle JSX

    def openAE(self):
        self.aeCom.openAE()

    def waitingAELoading(self):
        loading = True
        attempts = 0
        while loading and attempts < 60:
            for t in CurrentWindows().getTitles():
                if self.aeWindowName.lower() in t.lower():
                    loading = False
                    break

            attempts += 1
            time.sleep(0.5)

        return not loading

    def jsAlert(self, msg):
        self.aeCom.jsNewCommandGroup() # Clean JSX command list

        # Write new JSX commands
        jsxTodo =  "alert(\"" + msg + "\");"
        self.aeCom.addCommand(jsxTodo)

        self.aeCom.jsExecuteCommand() # Execute command list

    def jsOpenScene(self, path):
        self.aeCom.jsNewCommandGroup() # Clean JSX command list

        # Write new JSX commands
        jsxTodo =  "var aepFile = new File(\"" + path + "\");"
        jsxTodo += "app.open(aepFile);"
        self.aeCom.addCommand(jsxTodo)

        self.aeCom.jsExecuteCommand() # Execute command list

    def jsGetActiveDocument(self):
        self.aeCom.jsNewCommandGroup() # Clean JSX command list

        # Write new JSX commands
        resultVarName = "aeFilePath"
        jsxTodo = ("var %s = app.project.file.fsName;" % resultVarName)
        self.aeCom.addCommand(jsxTodo)
        self.aeCom.jsWriteDataOut(resultVarName) # Add JSX commands to write result in temp file

        self.aeCom.jsExecuteCommand() # Execute command list

        return self.aeCom.readReturn()[0] # Read the temp file to get the JSX returned value

if __name__ == '__main__':
    # Create the wrapper
    aeApp = AE_JSInterface(aeVersion = "16.0", returnFolder = os.path.join(os.path.expanduser('~'), "Documents", "temp"))

    # Open AE if needed
    aeApp.openAE()
    if aeApp.waitingAELoading():
        # Launch function if AE is ready
        aeApp.jsOpenScene("‪C:/Users/winuser8/Desktop/test.aep")
