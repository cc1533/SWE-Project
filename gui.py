#####################################################################################################
# 	CSE 4214, Intro to Software Engineering, Fall 2016
# 	Lab Section 2, Group 3, Next Top Model
#
#####################################################################################################
# 	Contributors:
# 			Alex Palacio, Christopher Cole, Jia Zhao,
# 			Nathan Frank, Reid Montague, Titus Dillon
#
#####################################################################################################
#  TODO:
#       1.  Add Call Mallet button functionality
#       2.  Test to make sure it runs and works correctly on Windows
#       3.  Figure out how to get the graphing stuff to work?
#       4.  MINOR:  Get rid of global variables
#
#####################################################################################################
# 	Program info:
# 			- This is the GUI that the user will interface with and drive the program.
#
#####################################################################################################
# !/usr/bin/python

# README!
# If you need help writing code for Gtk, please watch this playlist:  https://www.youtube.com/playlist?list=PL6gx4Cwl9DGBBnHFDEANbv9q8T4CONGZE
# This is the online documentation for Gtk:  https://python-gtk-3-tutorial.readthedocs.io/en/latest/install.html
# Download PyGObject from:  https://wiki.gnome.org/action/show/Projects/PyGObject

# Imports here
import gi
from subprocess import call
gi.require_version('Gtk', '3.0')    # This is here because this program requires Gtk 3.0 or higher
from gi.repository import Gtk

# Create mallet and excel location string variables
# I couldn't figure out how to get these to work without being globals
# I'd much rather prefer that they be local variables instead
malletLoc = ""
excelLoc = ""


class GUI(Gtk.Window):
    def __init__(self):
        # Initialize window, set title of the window
        Gtk.Window.__init__(self, title="Next Top Model")
        # Sets the borders between all objects inside the window and the window's edge
        self.set_border_width(10)
        # Sets "requested" initial size of the window
        self.set_size_request(300, 80)
        # I honestly don't know what this does...
        self.timeout_id = None

        # Layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.add(vbox)

        # horizontal box, allows things to be side-by-side
        hbox = Gtk.Box(spacing=5)
        vbox.pack_start(hbox, True, True, 0)

        # Get the location of the mallet program from the user
        self.mLoc = Gtk.Entry()
        self.mLoc.set_text("Mallet Program Location Printed Here")
        self.mLoc.set_editable(False)  # not editable so they can't type in and screw stuff up
        vbox.pack_start(self.mLoc, True, True, 0)

        # Get excel file location from the user (what will be sent to the parser)
        self.inputFileLoc = Gtk.Entry()
        self.inputFileLoc.set_text("Excel File Location Printed Here")
        self.inputFileLoc.set_editable(False)
        vbox.pack_start(self.inputFileLoc, True, True, 0)

        # Submit button that gets the mallet location from the user
        self.getMal = Gtk.Button(label="Get Mallet Location")
        self.getMal.connect("clicked", self.getMal_clicked)
        hbox.pack_start(self.getMal, True, True, 0)

        # Submit button that gets the excel file location from the user
        self.getXL = Gtk.Button(label="Get Excel File Location")
        self.getXL.connect("clicked", self.getXL_clicked)
        hbox.pack_start(self.getXL, True, True, 0)

        # Button that calls the parser
        self.callParser = Gtk.Button(label="Submit to Parser")
        self.callParser.connect("clicked", self.callParser_clicked)
        vbox.pack_start(self.callParser, True, True, 0)

        # Button that calls Mallet
        self.callMallet = Gtk.Button(label="Call Mallet")
        self.callMallet.connect("clicked", self.callMallet_clicked)
        vbox.pack_start(self.callMallet, True, True, 0)

    # What happens when the getMal button is clicked by the user...
    def getMal_clicked(self, widget):
        global malletLoc

        # Create a window that allows a user to choose a file
        dialog = Gtk.FileChooserDialog("Mallet Location", self, Gtk.FileChooserAction.OPEN,
                                       ("Submit", Gtk.ResponseType.OK,
                                        "Cancel", Gtk.ResponseType.CANCEL
                                        ))
        # The "submit" and "cancel" arguments above actually creates buttons inside the file window

        # Run / Show the file explorer window
        response = dialog.run()

        # If the user presses "submit" or clicks on a file in the file window
        if response == Gtk.ResponseType.OK:
            # Whatever the user submits or clicks on will be in dialog.get_filename()
            malletLoc = dialog.get_filename()

            # Test to make sure that the mallet program is actually in what the user gave
            # This isn't a "correct" or true test but it'll work for now
            # This is probably a security concern... The user could rename any program to "mallet" and this program will attempt to run it
            if "mallet" in malletLoc:
                # set the entry text box to whatever the user clicked on
                self.mLoc.set_text(malletLoc)
            else:
                self.mLoc.set_text("Mallet not found, Please try again")
            # Closes the file window
            dialog.destroy()

        # If the user closes the window without selecting a file or presses the "cancel" button
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

    # This is what happens when the getXL button is clicked by the user
    def getXL_clicked(self, widget):
        global excelLoc

        dialog = Gtk.FileChooserDialog("Excel File Location", self, Gtk.FileChooserAction.OPEN,
                                       ("Submit", Gtk.ResponseType.OK,
                                        "Cancel", Gtk.ResponseType.CANCEL
                                        ))

        # Run / Show the file explorer window
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            excelLoc = dialog.get_filename()
            # The given file must be .xls or .xlsx, this should work for both
            if ".xls" in excelLoc:
                self.inputFileLoc.set_text(excelLoc)

            else:
                self.inputFileLoc.set_text("File not .xls or .xlsx, Please try again")

            dialog.destroy()

        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

    def callParser_clicked(self, widget):
        global excelLoc
        print("Submitting " + excelLoc + " to ExcelParser.py")
        # It's hard to tell whether or not this works... I'm pretty sure this call is correct but does ExcelParser.py work with this kind of argument passing?
        call(["python3.5", "ExcelParser.py", excelLoc])

    def callMallet_clicked(self, widget):
        global malletLoc
        print("Submitting file to " + malletLoc)
        # I forgot the command to run mallet... Like I have no idea what-so-ever


# creates the initial class
win = GUI()
# This makes the 'x' button at the top of the page terminate the program
win.connect("delete-event", Gtk.main_quit)
# Shows all the objects in the window
win.show_all()
# This is basically the "loop" that makes the GUI continually run until termination
Gtk.main()
