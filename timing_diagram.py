import os
import sys
import string

_cur_dir = os.path.dirname(__file__)
TARANA_ROOT_PARENT = os.path.join(_cur_dir, "../../../../../..")
sys.path.append(TARANA_ROOT_PARENT)
sys.path.append(os.path.join(TARANA_ROOT_PARENT, "tarana/tools/ctl/src/python/ctl"))
sys.path.append(os.path.join(TARANA_ROOT_PARENT, "tarana/tools/lib/python"))
sys.path.append(os.path.join(TARANA_ROOT_PARENT, "tarana/tools/utils/testing"))
from tarana.tools.utils.testing import stub_component

stub_component("syc", "0.660.000.01", "E1.xxx.xxx")
stub_component("fsp", "0.660.000.04", "E1.xxx.xxx")
stub_component("frf", "0.660.001.00", "E1.xxx.xxx")

import ctl.frame_config as frame_config
from tarana.tools.twshell.subcmds.en import config
from tarana.tools.twshell.settings import TARANA_ROOT

class TimingDiagram(object):
  """Class that contains all required functions to plot a timing diagram.

  1. Each function contains "outputfile" as a parameter. This points to the .ps file that we are writing postscript code to
  2. Must be incorporated into handler_trace_data.py to produce all the output files.
  Handler_trace_data.py parses the data coming out of the statmonitor and will feed the inputs to this timing diagram.

  """

   #72 points in postscript = 1 inch
  arrow_counter = 0
  arrow_countercn = 0
  POINTS_PER_INCH = 72

   #DIMENSION OF PAPER (IN INCHES)
  X_DIMENSION = 40
  Y_DIMENSION = 50

  #CONFIGURE MARGINS
  X_MARGIN = 72.0 #one inch x-margin on left and right
  x_framelength = (X_DIMENSION - (2 * X_MARGIN/POINTS_PER_INCH)) * 72/4
  y_framelength = (Y_DIMENSION * POINTS_PER_INCH - 2 * X_MARGIN) / 2.3
  Y_MARGIN = -1.0 * y_framelength / 2.0 - (POINTS_PER_INCH * Y_DIMENSION/10)
  SPACE_BETWEEN = 72 * 3 #leaves a vertical gap of 3 inches between EN and CN plot

  #CAN CONFIGURE RTG, TTG, AND NUMBER OF SYMBOLS IN UPLINK AND DOWNLINK HERE...
  DL = 35
  UL = 13
  TTG = 100.0
  RTG = 300.0
  SYM_DURATION = (5000 - RTG - TTG) / (DL + UL)

  X_OFFSET = ((SYM_DURATION * UL + RTG) / 5000.0) * x_framelength;

  #Should you want to add another module you could change this number
  NUMBER_OF_MODULES = 8

  listofmodulenames = ["PRU", "PCD", "TFS", "AXD", "AXE", "BFW", "MFSM", "CAL"]

  modules = {"PRU": 0, "PCD":1, "TFS":2, "AXD":3, "AXE":4, "BFW":5, "MFSM":6, "CAL": 7}
  # Used to determine the vertical offset for each of the modules...
  moduleverticality = {"PRU": 0, "PCD":1, "TFS":2, "AXD":3, "AXE":4, "BFW":5, "MFSM":6, "CAL": 7}
  # Used to set the color of each module
  modulecolor = {"PRU": "0.58 0.42 0.58", "PCD": "1.00 0.83 0.83", "TFS": "1.00 0.5 0.00",
                 "AXD": "1.00 1.00 0.5","AXE": "0.0 1.00 1.00", "BFW": "0.67 1.00 0.33",
                 "MFSM": "0.83 1.00 1.00", "CAL": "0.83 0.83 0.83"}
  # Used to set the color of processes that occur on each module

  processcolor = {"PRU": "0.33 0.00 0.33", "PCD": "1.00 0.5 0.5", "TFS": "0.3 0.0 0.0",
                  "AXD": "0.83 0.83 0.17", "AXE": "0.42 0.58 0.58", "BFW": "0.0 0.33 0.0",
                  "MFSM": "0.0 0.33 0.67", "CAL": "0.17 0.17 0.17"}

  # Used to set the color of arrows from module to module
  arrowcolor = {"PRU": "0.75 0.25 0.75", "PCD": "1.00 0.5 0.5", "TFS": "0.63 0.32 0.18",
                "AXD": "0.86 0.8 0.24","AXE": "0.25 0.25 0.75", "BFW": "0.13 0.55 0.13",
                "MFSM": "0.25 0.75 0.75", "CAL": "0.5 0.5 0.5"}
  # Used to keep track of comment boxes on the EN plot
  commenttracker = {"PRU0": 0, "PRU1" : 0, "PRU2" : 0, "PRU3": 0, "PRU": 0, "PRUFACTOR": 0,
                    "PCD0": 0, "PCD1" : 0, "PCD2" : 0, "PCD3" : 0, "PCD": 0, "PCDFACTOR": 0,
                    "TFS0": 0, "TFS1" : 0, "TFS2" : 0, "TFS3" : 0, "TFS": 0, "TFSFACTOR": 0,
                    "AXD0": 0, "AXD1" : 0, "AXD2" : 0, "AXD3" : 0, "AXD": 0, "AXDFACTOR": 0,
                    "AXE0": 0, "AXE1" : 0, "AXE2" : 0, "AXE3" : 0, "AXE": 0, "AXEFACTOR": 0,
                    "BFW0": 0, "BFW1" : 0, "BFW2" : 0, "BFW3" : 0, "BFW": 0, "BFWFACTOR": 0,
                    "MFSM0": 0, "MFSM1" : 0, "MFSM2" : 0, "MFMS3" : 0, "MFSM": 0, "MFSMFACTOR": 0,
                    "CAL0": 0, "CAL1" : 0, "CAL2" : 0, "CAL3" : 0, "CAL": 0, "CALFACTOR": 0,
                    "commentcount": 0}
  #Used to keep track of comment boxes on the CN plot
  commenttrackercn = {"PRU0": 0, "PRU1" : 0, "PRU2" : 0, "PRU3": 0, "PRU": 0, "PRUFACTOR": 0,
                    "PCD0": 0, "PCD1" : 0, "PCD2" : 0, "PCD3" : 0, "PCD": 0, "PCDFACTOR": 0,
                    "TFS0": 0, "TFS1" : 0, "TFS2" : 0, "TFS3" : 0, "TFS": 0, "TFSFACTOR": 0,
                    "AXD0": 0, "AXD1" : 0, "AXD2" : 0, "AXD3" : 0, "AXD": 0, "AXDFACTOR": 0,
                    "AXE0": 0, "AXE1" : 0, "AXE2" : 0, "AXE3" : 0, "AXE": 0, "AXEFACTOR": 0,
                    "BFW0": 0, "BFW1" : 0, "BFW2" : 0, "BFW3" : 0, "BFW": 0, "BFWFACTOR": 0,
                    "MFSM0": 0, "MFSM1" : 0, "MFSM2" : 0, "MFMS3" : 0, "MFSM": 0, "MFSMFACTOR": 0,
                    "CAL0": 0, "CAL1" : 0, "CAL2" : 0, "CAL3" : 0, "CAL": 0, "CALFACTOR": 0,
                      "commentcountcn": 0}

  priority = {"PRU": 40, "PCD": 60, "TFS": 80, "AXD": 70, "AXE": 50, "BFW": 85, "MFSM": 90,
              "CAL": 100}

  def __init__(self, link_name):
    self.en_config = config.load_cfg_from_db(link_name)
    self.fc = frame_config.FrameConfigMGTRF(self.en_config)

  def font_initialization (self, outputfile, font_size):
    """Changes font to desired font size"""
    outputfile.write("/Times-Bold findfont\n")
    outputfile.write(str(font_size) + " scalefont\n")
    outputfile.write("setfont\n")

  def landscape_initialization(self, outputfile):
    """Set the page to landscape format"""
    outputfile.write("%%Orientation: Landscape\n")
    outputfile.write("%%DocumentMedia: a4 595 842 80 () ()\n")
    outputfile.write("%%Pages: 2\n")
    outputfile.write("%%EndComments\n")
    outputfile.write("%%EndProlog\n")
    outputfile.write("%%BeginSetup\n")
    outputfile.write("% A4, rotated 90 degrees ACW\n")
    outputfile.write ("<< /PageSize [%lf %lf] /Orientation 3 >> setpagedevice\n"
             % (TimingDiagram.Y_DIMENSION * 72.0,
                TimingDiagram.X_DIMENSION * 72.0 + TimingDiagram.X_OFFSET))
    outputfile.write("%%EndSetup\n")
    outputfile.write("%%Page: 1 1\n")
    outputfile.write("%%BeginPageSetup\n")
    outputfile.write("90 rotate 0 -595 translate\n")
    outputfile.write("%%EndPageSetup\n")

  def title (self, outputfile, font_size, node):
    """Takes in desired font_size to draw the title for the EN frame and CN frame"""
    if (("en" or "EN") in node):
      moveto_x = 250
      moveto_y = 550
      tag = "EN"
    if (("cn" or "CN") in node):
      moveto_x = 250
      moveto_y = -1200
      tag = "CN"
    self.font_initialization (outputfile, font_size)
    outputfile.write("0 0 0 setrgbcolor\n")
    outputfile.write("%lf %lf  moveto\n" % (moveto_x, moveto_y))
    outputfile.write("10 setlinewidth\n")
    outputfile.write("(%s: 2x-Frame 16-Antenna Sequence Diagram) show\n" % (tag))
    outputfile.write("1 setlinewidth\n")

  def draw_rectangles(self, outputfile, right_left, bottom_top):
    """Accepts x and y axes lengths so as to draw a rectangle with those specifications
    Args:

    1. right_left --> length of rectangle on x axis
    2. bottom_top --> length of rectangle on y axis
    """

    outputfile.write("%lf 0.0 rlineto\n" %  (right_left))
    outputfile.write("0.0 %lf rlineto\n" % (bottom_top))
    outputfile.write("%lf 0.0 rlineto\n" % (right_left * -1))
    outputfile.write("0.0 %lf rlineto\n" % (bottom_top * -1))

  def legend(self, outputfile, font_size, node):
    """Takes in desired font_size to draw the legend for the EN or CN frame"""
    if (("en" or "EN") in node):
      moveto_x = TimingDiagram.X_MARGIN + TimingDiagram.X_OFFSET + TimingDiagram.x_framelength*2.0
      moveto_y = TimingDiagram.Y_MARGIN + TimingDiagram.y_framelength

    if (("cn" or "CN") in node):
      moveto_x = TimingDiagram.X_MARGIN + TimingDiagram.X_OFFSET + TimingDiagram.x_framelength*2.0
      moveto_y = TimingDiagram.Y_MARGIN - TimingDiagram.SPACE_BETWEEN


    self.font_initialization (outputfile, font_size)
    outputfile.write("%lf %lf %s" % (moveto_x, moveto_y + 80, "moveto\n"))
    self.draw_rectangles (outputfile,15,30)
    outputfile.write("0.25 0.88 0.82 setrgbcolor\n")
    outputfile.write("fill\n")
    outputfile.write("%lf %lf %s" % (moveto_x + 20, moveto_y + 95, "moveto\n"))
    outputfile.write("0 0 0 setrgbcolor\n")
    outputfile.write("(UL even ref symbol) show\n")
    outputfile.write("%lf %lf %s" % (moveto_x + 20, moveto_y + 140, "moveto\n"))
    self.draw_rectangles (outputfile,15,30)
    outputfile.write("0.00 0.00 0.55 setrgbcolor\n")
    outputfile.write("fill\n")
    outputfile.write("%lf %lf %s" % (moveto_x + 20, moveto_y + 155, "moveto\n"))
    outputfile.write("0 0 0 setrgbcolor\n")
    outputfile.write("(UL odd ref symbol) show\n")
    outputfile.write("%lf %lf %s" % (moveto_x - 140, moveto_y + 80, "moveto\n"))
    self.draw_rectangles (outputfile,15,30)
    outputfile.write("0.55 0.00 0.00 setrgbcolor\n")
    outputfile.write("fill\n")
    outputfile.write("%lf %lf %s" % (moveto_x - 120, moveto_y + 95, "moveto\n"))
    outputfile.write("0 0 0 setrgbcolor\n")
    outputfile.write("(DL even ref symbol) show\n")
    outputfile.write("%lf %lf %s" % (moveto_x - 140, moveto_y + 140, "moveto\n"))
    self.draw_rectangles (outputfile,15,30)
    outputfile.write("1.00 0.41 0.71 setrgbcolor\n")
    outputfile.write("fill\n")
    outputfile.write("%lf %lf %s" % (moveto_x - 120, moveto_y + 155, "moveto\n"))
    outputfile.write("0 0 0 setrgbcolor\n")
    outputfile.write("(DL odd ref symbol) show\n")
    outputfile.write( "%lf %lf %s" % (moveto_x + 140, moveto_y + 80, "moveto\n"))
    self.draw_rectangles (outputfile,15,30)
    outputfile.write("1.00 0.8 0.00 setrgbcolor\n")
    outputfile.write("fill\n")
    outputfile.write( "%lf %lf %s" % (moveto_x + 160, moveto_y + 95, "moveto\n"))
    outputfile.write("0 0 0 setrgbcolor\n")
    outputfile.write("(UL ranging symbol) show\n")


  def overhead_rect (self, outputfile, node):
    """Responsible for creating the long blue rectangle immediately above the CN or EN frame"""

    draw_y = 30.0

    if (("en" or "EN") in node):
      moveto_x = TimingDiagram.X_MARGIN + TimingDiagram.X_OFFSET
      moveto_y = TimingDiagram.Y_MARGIN + TimingDiagram.y_framelength +10
      draw_x = TimingDiagram.x_framelength*4

    if (("cn" or "CN") in node):
      moveto_x = TimingDiagram.X_MARGIN
      moveto_y = TimingDiagram.Y_MARGIN - TimingDiagram.SPACE_BETWEEN +10
      draw_x = TimingDiagram.x_framelength*4 + TimingDiagram.X_OFFSET

    outputfile.write("newpath\n")
    outputfile.write("0.9 0.9 0.98 setrgbcolor\n")
    outputfile.write("0 0 moveto\n")
    outputfile.write("%lf %lf moveto\n" % (moveto_x, moveto_y))
    self.draw_rectangles (outputfile, draw_x, 30.0)
    outputfile.write("fill\n")

  def two_headed_black_arrow(self, outputfile, delta_x, node):
    """Draws a two headed black arrow before the start of each frame for either the EN or CN frame

    Note: the parameter delta_x is fed with the x values that indicate the start of each frame
    """
    if (("en" or "EN") in node):
      moveto_x = TimingDiagram.X_OFFSET + TimingDiagram.X_MARGIN + TimingDiagram.x_framelength * delta_x
      moveto_y = TimingDiagram.Y_MARGIN

    if (("cn" or "CN") in node):
      moveto_x = TimingDiagram.X_MARGIN + TimingDiagram.x_framelength * delta_x
      moveto_y = TimingDiagram.Y_MARGIN - TimingDiagram.y_framelength - TimingDiagram.SPACE_BETWEEN

    outputfile.write("newpath\n")
    outputfile.write("0 0 0 setrgbcolor\n")
    outputfile.write("%lf %lf moveto\n" % (moveto_x, moveto_y))
    outputfile.write("5 0 rlineto\n")
    outputfile.write("-5 -10 rlineto\n")
    outputfile.write("-5 10 rlineto\n")
    outputfile.write("5 0 rlineto\n")
    outputfile.write("2 setlinewidth\n")
    outputfile.write("0 %lf rlineto\n" % (TimingDiagram.y_framelength))
    outputfile.write("5 0 rlineto\n")
    outputfile.write("-5 10 rlineto\n")
    outputfile.write("-5 -10 rlineto\n")
    outputfile.write("5 0 rlineto\n")
    outputfile.write("gsave 0 0 0 setrgbcolor fill grestore stroke\n")

  def draw_template (self, outputfile):
    """Draws the EN superframe

    Details:
    1. Uses a for loop to draw 4 frames (each preceded by a two headed blackarrow)
    2. Nested for loops are able to plot uplink and downlink symbols while also numbering them
    3. The frames can be configured by the user to display the desired number of symbols
    and the desired amount of RTG and TTG
    4. We are also numbering and coloring specific symbol numbers on the overhead rectangle in
    this function. It is possible to configure which symbols are uplink and downlink reference
    symbols
    """

    frame_count = 4
    rectangle_width = (TimingDiagram.x_framelength * (TimingDiagram.SYM_DURATION / 5000.0))
    for x in range (0, frame_count):
      # Overlaying for loop that draws 4 frames

      for i in range (0,TimingDiagram.DL):
        #Draws downlink symbols for each frame
        outputfile.write( "%lf %lf %s" % (TimingDiagram.X_MARGIN + TimingDiagram.X_OFFSET
                                 + x* TimingDiagram.x_framelength + (rectangle_width * i),
                                 TimingDiagram.Y_MARGIN, "moveto\n"))
        self.draw_rectangles(outputfile, rectangle_width, TimingDiagram.y_framelength)
        if (i % 2):
          outputfile.write("0.93 0.93 0.93 setrgbcolor\n")
          outputfile.write("fill\n")
        else:
          outputfile.write("0.85 0.85 0.85 setrgbcolor\n")
          outputfile.write("stroke\n")
        outputfile.write("0.6 0.6 0.6 setrgbcolor\n")

        #Draws downlink symbols on the overhead rectangle and colors in the downlink reference symbols
        for dlsym in range (0, self.fc.dl_ref_syms):
          if ((x%2 != 0) and  (i == dlsym)):
            outputfile.write("1.00 0.41 0.71 setrgbcolor\n")
          if ((x%2 == 0) and (i == dlsym)):
            outputfile.write("0.55 0.00 0.00 setrgbcolor\n")

        outputfile.write( "%lf %lf %s" % (TimingDiagram.X_MARGIN + TimingDiagram.X_OFFSET
                                 + x * TimingDiagram.x_framelength + (rectangle_width * i),
                                 TimingDiagram.Y_MARGIN
                                 + TimingDiagram.y_framelength+14.5, "moveto\n"))
        self.draw_rectangles(outputfile, rectangle_width, rectangle_width+5)
        outputfile.write("fill\n")
        outputfile.write("1 1 1 setrgbcolor\n")
        #Displays the numbers on the center of the rectangles
        outputfile.write("%lf %lf %s" % (TimingDiagram.X_MARGIN + TimingDiagram.X_OFFSET
                                + x * TimingDiagram.x_framelength + (rectangle_width * i)
                                +rectangle_width/2.0, TimingDiagram.Y_MARGIN
                                +TimingDiagram.y_framelength+14.5+rectangle_width/2.0, "moveto\n"))
        outputfile.write("(%d)" "%s" % (i + 1, "show\n"))
        for a in range (0,TimingDiagram.NUMBER_OF_MODULES - 1):
          outputfile.write("0.9 0.8 0.1 setrgbcolor\n")
          outputfile.write("%lf %lf %s" % (TimingDiagram.X_MARGIN + TimingDiagram.X_OFFSET
                                  + x * TimingDiagram.x_framelength + rectangle_width * i
                                  + rectangle_width / 5.0, TimingDiagram.Y_MARGIN
                                  + ((a + 1) * TimingDiagram.y_framelength)
                                  / TimingDiagram.NUMBER_OF_MODULES, "moveto\n"))
    #move to the center of rectangle
          outputfile.write("(%d)" "%s" % (i + 1, "show\n"))    #then put the number in the center of the rectangle
      for w in range (TimingDiagram.DL, TimingDiagram.DL + TimingDiagram.UL):
        #Draws uplink symbols for each frame
        outputfile.write("%lf %lf %s" % (TimingDiagram.X_MARGIN + TimingDiagram.X_OFFSET
                                + x * TimingDiagram.x_framelength +(rectangle_width * w)
                                + TimingDiagram.x_framelength * (TimingDiagram.TTG / 5000.0),
                                TimingDiagram.Y_MARGIN, "moveto\n"))
        self.draw_rectangles(outputfile, rectangle_width, TimingDiagram.y_framelength)
        if (w % 2):
          outputfile.write("0.9 0.9 0.9 setrgbcolor\n")
          outputfile.write("fill\n")
        else:
          outputfile.write("0.8 0.85 0.8 setrgbcolor\n")
          outputfile.write("fill\n")

        outputfile.write("0.6 0.6 0.6 setrgbcolor\n")

        #Draws uplink symbols on the overhead rectangle and colors in the uplink reference symbols
        for ulsym in range (0, self.fc.ul_ref_syms):
          if (x%2 != 0 and (w - TimingDiagram.DL == ulsym)):
            outputfile.write("0.00 0.00 0.55 setrgbcolor\n")
          if (x%2 == 0 and (w - TimingDiagram.DL == ulsym)):
            outputfile.write("0.25 0.88 0.82 setrgbcolor\n")
        for ulrangesym in range (self.fc.ul_ref_syms, self.fc.ul_ref_syms+self.fc.ul_dan_ranging_syms):
          if (w - TimingDiagram.DL == ulrangesym):
            outputfile.write("1.00 0.8 0.00 setrgbcolor\n")
        outputfile.write("%lf %lf %s" % (TimingDiagram.X_MARGIN + TimingDiagram.X_OFFSET
                                + x * TimingDiagram.x_framelength + (rectangle_width * w)
                                + TimingDiagram.x_framelength * (TimingDiagram.TTG / 5000.0),
                                TimingDiagram.Y_MARGIN+TimingDiagram.y_framelength+14.5, "moveto\n"))
        self.draw_rectangles(outputfile, rectangle_width, rectangle_width+5)
        outputfile.write("fill\n")

        outputfile.write("1 1 1 setrgbcolor\n")

        #Displays the numbers on the center of the rectangles
        outputfile.write( "%lf %lf %s" % (TimingDiagram.X_MARGIN + TimingDiagram.X_OFFSET
                                 + x * TimingDiagram.x_framelength + (rectangle_width * w)
                                 +rectangle_width/2.0
                                 + TimingDiagram.x_framelength * (TimingDiagram.TTG / 5000.0),
                                 TimingDiagram.Y_MARGIN+TimingDiagram.y_framelength+14.5
                                 +rectangle_width/2.0, "moveto\n"))
        outputfile.write("(%d)" "%s" % (w + 1 - TimingDiagram.DL, "show\n"))

        for a in range (0, TimingDiagram.NUMBER_OF_MODULES - 1):
          outputfile.write("0.9 0.8 0.1 setrgbcolor\n")
          outputfile.write( "%lf %lf %s" % (TimingDiagram.X_MARGIN + TimingDiagram.X_OFFSET
                                   + x * TimingDiagram.x_framelength + TimingDiagram.x_framelength
                                   * (TimingDiagram.TTG / 5000.0) + rectangle_width * w
                                   + rectangle_width / 5.0, TimingDiagram.Y_MARGIN
                                   + ((a + 1) * TimingDiagram.y_framelength)
                                   / TimingDiagram.NUMBER_OF_MODULES, "moveto\n"))
          outputfile.write( "(%d)" "%s" % (w + 1 - TimingDiagram.DL, "show\n"))       #then put the number in the center of the rectangle
      outputfile.write("0 0 0 setrgbcolor\n")
      self.two_headed_black_arrow(outputfile, x, "en")
      outputfile.write("1 setlinewidth\n")


  def draw_template_cn (self, outputfile):
    """The exact same as the 'drawtemplate' function
    The only thing different is that it draws the CN superframe which is on the bottom of the pdf
    Also, the frame starts with uplink symbols

    """
    rectangle_width = (TimingDiagram.x_framelength * (TimingDiagram.SYM_DURATION / 5000.0))
    frame_count = 4
    for w in range (TimingDiagram.DL, TimingDiagram.DL + TimingDiagram.UL):
      #Draws the uplink symbols that start off the CN superframe
      outputfile.write("%lf %lf %s" % (TimingDiagram.X_MARGIN + (rectangle_width * (w-TimingDiagram.DL)),
                              TimingDiagram.Y_MARGIN - TimingDiagram.SPACE_BETWEEN
                              - TimingDiagram.y_framelength, "moveto\n"))
      self.draw_rectangles(outputfile, rectangle_width, TimingDiagram.y_framelength)
      if (w % 2):
        outputfile.write("0.9 0.9 0.9 setrgbcolor\n")
        outputfile.write("fill\n")
      else:
        outputfile.write("0.8 0.85 0.8 setrgbcolor\n")
        outputfile.write("fill\n")

      outputfile.write("0.6 0.6 0.6 setrgbcolor\n")
#####
      for ulsyms in range (0,self.fc.ul_ref_syms):
        if (ulsyms == w-TimingDiagram.DL):
          #outputfile.write("0.00 0.00 0.55 setrgbcolor\n")
          outputfile.write("0.25 0.88 0.82 setrgbcolor\n")
      for ulrangesym in range (self.fc.ul_ref_syms, self.fc.ul_ref_syms+self.fc.ul_dan_ranging_syms):
        if (w - TimingDiagram.DL == ulrangesym):
          outputfile.write("1.00 0.8 0.00 setrgbcolor\n")

#####

      outputfile.write("%lf %lf %s" % (TimingDiagram.X_MARGIN + (rectangle_width * (w-TimingDiagram.DL)),
                              TimingDiagram.Y_MARGIN - TimingDiagram.SPACE_BETWEEN
                              + 14.5, "moveto\n"))
      self.draw_rectangles(outputfile, rectangle_width, rectangle_width+5)
      outputfile.write("fill\n")

      outputfile.write("1 1 1 setrgbcolor\n")
      outputfile.write( "%lf %lf %s" % (TimingDiagram.X_MARGIN + (rectangle_width * (w-TimingDiagram.DL))
                               +rectangle_width/2.0, TimingDiagram.Y_MARGIN
                               - TimingDiagram.SPACE_BETWEEN +14.5+rectangle_width/2.0, "moveto\n"))
      outputfile.write("(%d)" "%s" % (w + 1 - TimingDiagram.DL, "show\n"))

      for a in range (0, TimingDiagram.NUMBER_OF_MODULES - 1):
        outputfile.write("0.9 0.8 0.1 setrgbcolor\n")
        outputfile.write( "%lf %lf %s" % (TimingDiagram.X_MARGIN
                                 + rectangle_width * (w - TimingDiagram.DL) + rectangle_width / 5.0,
                                 TimingDiagram.Y_MARGIN - TimingDiagram.SPACE_BETWEEN
                                 - TimingDiagram.y_framelength
                                 + ((a + 1) * TimingDiagram.y_framelength)
                                 / TimingDiagram.NUMBER_OF_MODULES, "moveto\n"))     #move to the center of rectangle
        outputfile.write( "(%d)" "%s" % (w + 1 - TimingDiagram.DL, "show\n"))       #then put the number in the center of the rectangle

    for x in range (0, frame_count):
      #Overlaying for loop that draws four frames
      for i in range (0,TimingDiagram.DL):
        #Draws the downlink symbols for each frame
        outputfile.write( "%lf %lf %s" % (TimingDiagram.X_MARGIN + TimingDiagram.X_OFFSET
                                 + x* TimingDiagram.x_framelength + (rectangle_width * i),
                                 TimingDiagram.Y_MARGIN - TimingDiagram.y_framelength
                                 - TimingDiagram.SPACE_BETWEEN, "moveto\n"))
        self.draw_rectangles (outputfile, rectangle_width, TimingDiagram.y_framelength)
        if (i % 2):
          outputfile.write("0.93 0.93 0.93 setrgbcolor\n")
          outputfile.write("fill\n")
        else:
          outputfile.write("0.85 0.85 0.85 setrgbcolor\n")
          outputfile.write("stroke\n")
        outputfile.write("0.6 0.6 0.6 setrgbcolor\n")


        for dlsym in range (0, self.fc.dl_ref_syms):
          if ((x%2 != 0) and  (i == dlsym)):
            outputfile.write("1.00 0.41 0.71 setrgbcolor\n")
          if ((x%2 == 0) and (i == dlsym)):
            outputfile.write("0.55 0.00 0.00 setrgbcolor\n")





        #Puts the number of each symbol in the middle of the rectangle
        outputfile.write( "%lf %lf %s" % (TimingDiagram.X_MARGIN + TimingDiagram.X_OFFSET
                                 + x * TimingDiagram.x_framelength + (rectangle_width * i),
                                 TimingDiagram.Y_MARGIN - TimingDiagram.SPACE_BETWEEN
                                 +14.5, "moveto\n"))
        self.draw_rectangles (outputfile, rectangle_width, rectangle_width+5)
        outputfile.write("fill\n")
        outputfile.write("1 1 1 setrgbcolor\n")
        outputfile.write("%lf %lf %s" % (TimingDiagram.X_MARGIN + TimingDiagram.X_OFFSET
                                + x * TimingDiagram.x_framelength + (rectangle_width * i)
                                +rectangle_width/2.0, TimingDiagram.Y_MARGIN
                                - TimingDiagram.SPACE_BETWEEN +14.5
                                +rectangle_width/2.0, "moveto\n"))
        outputfile.write("(%d)" "%s" % (i + 1, "show\n"))
        for a in range (0,TimingDiagram.NUMBER_OF_MODULES - 1):
          outputfile.write("0.9 0.8 0.1 setrgbcolor\n")
          outputfile.write("%lf %lf %s" % (TimingDiagram.X_MARGIN + TimingDiagram.X_OFFSET
                                  + x * TimingDiagram.x_framelength + rectangle_width * i
                                  + rectangle_width / 5.0, TimingDiagram.Y_MARGIN
                                  - TimingDiagram.y_framelength - TimingDiagram.SPACE_BETWEEN
                                  + ((a + 1) * TimingDiagram.y_framelength)
                                  / TimingDiagram.NUMBER_OF_MODULES, "moveto\n"))
    #move to the center of rectangle
          outputfile.write("(%d)" "%s" % (i + 1, "show\n"))    #then put the number in the center of the rectangle
      for w in range (TimingDiagram.DL, TimingDiagram.DL + TimingDiagram.UL):
        #Draws the uplink symbols for each frame
        outputfile.write("%lf %lf %s" % (TimingDiagram.X_MARGIN + TimingDiagram.X_OFFSET
                                + x * TimingDiagram.x_framelength +(rectangle_width * w)
                                + TimingDiagram.x_framelength * (TimingDiagram.TTG / 5000.0),
                                TimingDiagram.Y_MARGIN - TimingDiagram.y_framelength
                                - TimingDiagram.SPACE_BETWEEN, "moveto\n"))
        self.draw_rectangles(outputfile, rectangle_width, TimingDiagram.y_framelength)
        if (w % 2):
          outputfile.write("0.9 0.9 0.9 setrgbcolor\n")
          outputfile.write("fill\n")
        else:
          outputfile.write("0.8 0.85 0.8 setrgbcolor\n")
          outputfile.write("fill\n")
        #Puts the number of each symbol in the middle of the rectangle
        outputfile.write("0.6 0.6 0.6 setrgbcolor\n")

        for ulsym in range (0, self.fc.ul_ref_syms):
          if (x%2 != 0 and (w - TimingDiagram.DL == ulsym)):
            outputfile.write("0.00 0.00 0.55 setrgbcolor\n")
          if (x%2 == 0 and (w - TimingDiagram.DL == ulsym)):
            outputfile.write("0.25 0.88 0.82 setrgbcolor\n")
        for ulrangesym in range (self.fc.ul_ref_syms, self.fc.ul_ref_syms+self.fc.ul_dan_ranging_syms):
          if (w - TimingDiagram.DL == ulrangesym):
            outputfile.write("1.00 0.8 0.00 setrgbcolor\n")

        outputfile.write("%lf %lf %s" % (TimingDiagram.X_MARGIN + TimingDiagram.X_OFFSET
                                + x * TimingDiagram.x_framelength + (rectangle_width * w)
                                + TimingDiagram.x_framelength * (TimingDiagram.TTG / 5000.0),
                                TimingDiagram.Y_MARGIN - TimingDiagram.SPACE_BETWEEN
                                +14.5, "moveto\n"))
        self.draw_rectangles(outputfile, rectangle_width, rectangle_width+5)
        outputfile.write("fill\n")

        outputfile.write("1 1 1 setrgbcolor\n")
        outputfile.write( "%lf %lf %s" % (TimingDiagram.X_MARGIN + TimingDiagram.X_OFFSET
                                 + x * TimingDiagram.x_framelength + (rectangle_width * w)
                                 +rectangle_width/2.0
                                 + TimingDiagram.x_framelength * (TimingDiagram.TTG / 5000.0),
                                 TimingDiagram.Y_MARGIN - TimingDiagram.SPACE_BETWEEN
                                 +14.5+rectangle_width/2.0, "moveto\n"))
        outputfile.write("(%d)" "%s" % (w + 1 - TimingDiagram.DL, "show\n"))
        for a in range (0, TimingDiagram.NUMBER_OF_MODULES - 1):
          outputfile.write("0.9 0.8 0.1 setrgbcolor\n")
          outputfile.write( "%lf %lf %s" % (TimingDiagram.X_MARGIN + TimingDiagram.X_OFFSET
                                   + x * TimingDiagram.x_framelength
                                   + TimingDiagram.x_framelength * (TimingDiagram.TTG / 5000.0)
                                   + rectangle_width * w + rectangle_width / 5.0,
                                   TimingDiagram.Y_MARGIN - TimingDiagram.y_framelength
                                   - TimingDiagram.SPACE_BETWEEN
                                   + ((a + 1) * TimingDiagram.y_framelength)
                                   / TimingDiagram.NUMBER_OF_MODULES, "moveto\n"))     #move to the center of rectangle
          outputfile.write( "(%d)" "%s" % (w + 1 - TimingDiagram.DL, "show\n"))       #then put the number in the center of the rectangle
      outputfile.write("0 0 0 setrgbcolor\n")
      self.two_headed_black_arrow(outputfile, x, "cn")
      outputfile.write("1 setlinewidth\n")



  def draw_modules (self, outputfile, node):
    """Function that draws the modules (8 intersecting rectangles) on the EN or CN superframe
    The order of how the modules display on the frame can be configured
    """
    if (("en" or "EN") in node):
      y_factor = 0
    if (("cn" or "CN") in node):
      y_factor = -1 * TimingDiagram.SPACE_BETWEEN  - TimingDiagram.y_framelength


    for x in range (0, TimingDiagram.NUMBER_OF_MODULES):
      #Draws and fills a rectangle for each module ... The vertical order of the rectangles depends upon the variable 'x'
      outputfile.write("0 %lf moveto\n" % (TimingDiagram.Y_MARGIN + y_factor + (x + 1)
                                  * (TimingDiagram.y_framelength /TimingDiagram.NUMBER_OF_MODULES)
                                  - (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES)
                                  * 0.6666))
      self.draw_rectangles(outputfile, TimingDiagram.X_MARGIN + TimingDiagram.X_OFFSET + 4
                           * TimingDiagram.x_framelength, 0.33 * TimingDiagram.y_framelength
                           / TimingDiagram.NUMBER_OF_MODULES)
      outputfile.write (TimingDiagram.modulecolor[str(TimingDiagram.listofmodulenames[x])] + " setrgbcolor\n")
      outputfile.write ("fill\n")
      #Draws the name of the module on the left ends of each rectange ... The vertical order of the naming depends upon the variable 'x'
      outputfile.write("2.0 %lf moveto\n" % (TimingDiagram.Y_MARGIN + y_factor
                                    + (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES)
                                    * (x+1) - 0.5
                                    * (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES)))
      outputfile.write("0 0 0 setrgbcolor\n")
      self.font_initialization(outputfile, 25)
      outputfile.write ("(" + str(TimingDiagram.priority[str(TimingDiagram.listofmodulenames[x])])
               + " " + str(TimingDiagram.listofmodulenames[x]) + ")" + " show\n")

  def find_xposition(self, ms):
    """Takes in a time in milliseconds and translates that into an x coordinate on the EN superframe"""
    xposition = TimingDiagram.X_MARGIN + TimingDiagram.X_OFFSET + (TimingDiagram.x_framelength / 5.0) * ms
    return xposition

  def find_xposition_cn (self, ms):
    """Takes in a time in milliseconds and translates that into an x coordinate on the CN superframe"""
    xposition = TimingDiagram.X_MARGIN + (TimingDiagram.x_framelength / 5.0) * ms
    return xposition

  def rect_on_top(self, outputfile, rectangle, start_time, end_time, node):
    """Draws shaded rectangles on the desired module for the desired duration which is indicative of a process (on the EN or CN superframe)
    Args:
    1. 'rectangle' is the name of the module
    2. 'start_time' is the time that the process starts at
    3. 'endttime' is the time that the process ends at
    4. 'node' is whether en or cn
    """
    draw_y = 0.33 * (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES)

    if (("en" or "EN") in node):
      moveto_x = self.find_xposition(start_time)
      draw_x = self.find_xposition(end_time) - self.find_xposition(start_time)
      ydistance = TimingDiagram.Y_MARGIN + (TimingDiagram.moduleverticality[str(rectangle)]+1) *\
          (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES) -\
          (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES) * 0.6666
    if (("cn" or "CN") in node):
      moveto_x = self.find_xposition_cn(start_time)
      draw_x = self.find_xposition_cn(end_time) - self.find_xposition_cn(start_time)
      ydistance = TimingDiagram.Y_MARGIN - TimingDiagram.y_framelength - TimingDiagram.SPACE_BETWEEN\
          + (TimingDiagram.moduleverticality[str(rectangle)]+1) *\
          (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES) -\
          (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES) * 0.6666

    outputfile.write (TimingDiagram.processcolor[str(rectangle)] + " setrgbcolor\n")


    outputfile.write( "%lf %lf moveto\n" % (moveto_x, ydistance))
    self.draw_rectangles(outputfile, draw_x, draw_y)
    outputfile.write ("save\n")
    outputfile.write ("1 1 1 setrgbcolor\n")
    outputfile.write("stroke\n")
    outputfile.write( "grestore fill\n")


  def one_head_red_arrow(self, outputfile, start, finish, text, ms, node):
    """Draws an arrow on the EN superframe indicative of a signal transferred between two modules at a particular time
    Args:
    1. 'start' is the module that the signal originates from
    2. 'end' is the module where the signal goes to
    3. 'text' is the name of the signal
    4. 'ms'is the time at which the signal occurs
    5. 'node' is whether en or cn

    """
    starting = (TimingDiagram.moduleverticality[str(start)]+1)
    ending = (TimingDiagram.moduleverticality[str(finish)] + 1)
    outputfile.write (TimingDiagram.arrowcolor[str(finish)] + " setrgbcolor\n")

    difference = abs(starting - ending)

   # TimingDiagram.arrow_counter+=1
    rline1 = (difference * (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES))
    rline2 = (difference * (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES) * -1)



    if (("en" or "EN") in node):
      TimingDiagram.arrow_counter+=1

      moveto_x = self.find_xposition(ms)
      moveto_y = TimingDiagram.Y_MARGIN + (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES) * starting -\
          0.5 * (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES)
      arrowpos1x = self.find_xposition(ms) - 0.5 * (TimingDiagram.x_framelength * (TimingDiagram.SYM_DURATION / 5000.0))
      arrowpos2x = self.find_xposition(ms) + 0.5 * (TimingDiagram.x_framelength * (TimingDiagram.SYM_DURATION / 5000.0))
      arrowpos3x = self.find_xposition(ms) - 0.5 * (TimingDiagram.x_framelength * (TimingDiagram.SYM_DURATION / 5000.0))
      arrowpos4x = self.find_xposition(ms) + 0.5 * (TimingDiagram.x_framelength * (TimingDiagram.SYM_DURATION / 5000.0))

      arrowpos1y = TimingDiagram.Y_MARGIN + (TimingDiagram.y_framelength/ TimingDiagram.NUMBER_OF_MODULES) *\
          starting - 0.5 * (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES) +\
          difference * (0.5) * (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES)
      arrowpos2y = TimingDiagram.Y_MARGIN + (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES) *\
          starting - 0.5 * (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES) + difference *\
          (0.5) * (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES)
      arrowpos3y = TimingDiagram.Y_MARGIN + (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES) *\
          starting - 0.5 * (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES) + (difference) *\
          (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES) * -1 +\
          (difference * 0.5 * TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES)
      arrowpos4y = TimingDiagram.Y_MARGIN + (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES) *\
          starting - 0.5 * (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES) + (difference) *\
          (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES) * -1 +\
          (difference * 0.5 * TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES)
      arrow_tracker = TimingDiagram.arrow_counter

    if (("cn" or "CN") in node):
      TimingDiagram.arrow_countercn+=1

      moveto_x = self.find_xposition_cn(ms)
      moveto_y =  TimingDiagram.Y_MARGIN - TimingDiagram.y_framelength - TimingDiagram.SPACE_BETWEEN +\
          (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES) * starting - 0.5 *\
          (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES)
      arrowpos1x = self.find_xposition_cn(ms) - 0.5 * (TimingDiagram.x_framelength *\
                                                         (TimingDiagram.SYM_DURATION / 5000.0))
      arrowpos2x = self.find_xposition_cn(ms) + 0.5 * (TimingDiagram.x_framelength *\
                                                         (TimingDiagram.SYM_DURATION / 5000.0))
      arrowpos3x = self.find_xposition_cn(ms) - 0.5 * (TimingDiagram.x_framelength *\
                                                         (TimingDiagram.SYM_DURATION / 5000.0))
      arrowpos4x = self.find_xposition_cn(ms) + 0.5 * (TimingDiagram.x_framelength *\
                                                         (TimingDiagram.SYM_DURATION / 5000.0))
      arrowpos1y = TimingDiagram.Y_MARGIN - TimingDiagram.y_framelength - TimingDiagram.SPACE_BETWEEN +\
          (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES) * starting - 0.5 *\
          (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES) + difference * (0.5) *\
          (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES)
      arrowpos2y = TimingDiagram.Y_MARGIN - TimingDiagram.y_framelength - TimingDiagram.SPACE_BETWEEN +\
          (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES) * starting - 0.5 *\
          (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES) + difference * (0.5) *\
          (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES)
      arrowpos3y = TimingDiagram.Y_MARGIN - TimingDiagram.SPACE_BETWEEN - TimingDiagram.y_framelength +\
          (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES) * starting - 0.5 *\
          (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES) + (difference) *\
          (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES) * -1 +\
          (difference * 0.5 * TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES)
      arrowpos4y = TimingDiagram.Y_MARGIN - TimingDiagram.SPACE_BETWEEN - TimingDiagram.y_framelength +\
          (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES) * starting - 0.5 *\
          (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES) + (difference) *\
          (TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES) * -1 +\
          (difference * 0.5 * TimingDiagram.y_framelength / TimingDiagram.NUMBER_OF_MODULES)
      arrow_tracker = TimingDiagram.arrow_countercn


    outputfile.write("%lf %lf moveto\n" % (moveto_x, moveto_y))
    outputfile.write("2.0 setlinewidth\n")

    if (ending > starting):
      outputfile.write("5 0 rlineto\n")
      outputfile.write("-10 0 rlineto\n")
      outputfile.write("5 0 rlineto\n")
      outputfile.write( "0 %lf rlineto\n" % (rline1))
      outputfile.write("5 0 rlineto\n")
      outputfile.write("-5 10 rlineto\n")
      outputfile.write("-5 -10 rlineto\n")
      outputfile.write("5 0 rlineto\n")
      outputfile.write("gsave fill\n")
      outputfile.write("newpath\n")
      if (arrow_tracker % 2):
        outputfile.write( "%lf %lf moveto\n" % (arrowpos1x, arrowpos1y))
        outputfile.write( "10 setlinewidth\n")
        self.font_initialization(outputfile, 18)
        outputfile.write("90 rotate\n")
      else:
        outputfile.write( "%lf %lf moveto\n" % (arrowpos2x, arrowpos2y))
        outputfile.write("10 setlinewidth\n")
        self.font_initialization(outputfile, 18)
        outputfile.write("270 rotate\n")
      if ("NONE" in text):
        outputfile.write("( ) show\n")
      else:
        outputfile.write( "(%s) show\n" % (text))
      outputfile.write( "grestore stroke\n")

    if (starting > ending):
      outputfile.write("5 0 rlineto\n")
      outputfile.write("-10 0 rlineto\n")
      outputfile.write("5 0 rlineto\n")
      outputfile.write("0 %lf rlineto\n" % (rline2))
      outputfile.write("5 0 rlineto\n")
      outputfile.write("-5 -10 rlineto\n")
      outputfile.write("-5 10 rlineto\n")
      outputfile.write("5 0 rlineto\n")
      outputfile.write("gsave fill\n")
      outputfile.write("newpath\n")
      if ((arrow_tracker) % 2):
        outputfile.write( "%lf %lf moveto\n" % (arrowpos3x, arrowpos3y))
        outputfile.write( "10 setlinewidth\n")
        self.font_initialization(outputfile, 18)
        outputfile.write( "90 rotate\n")
      else:
        outputfile.write( "%lf %lf moveto\n" % (arrowpos4x, arrowpos4y))
        outputfile.write( "10 setlinewidth\n")
        self.font_initialization(outputfile, 18)
        outputfile.write( "270 rotate\n")
      if ("NONE" in text):
        outputfile.write("( ) show\n")
      else:
        outputfile.write("(%s) show\n" % (text))
      outputfile.write("grestore stroke\n")

  def comment_box(self, outputfile, rectangle, text, start_time, end_time):
    """ Creates a comment box for a corresponding process on the EN superframe
    Args:
    1. 'rectangle' indicates what module the process currently is on
    2. 'text' is the text that describes the process and goes into the module
    3. 'start_time' is the start time of the process
    4. 'end_time' is the end time of the process
    5. 'TimingDiagram.Y_MARGIN' is just fed with the value TIMINGDIAGRAM.Y_MARGIN -- used for positioning the comment box vertically
    """

    vertical = 1
    factor = 0
    x_frame = 4 * TimingDiagram.x_framelength

    if ("NONE" in text):
      bs = "garbage"
      #If the 'text' parameter is fed with the word NONE there will be no comment box created (in the case you didn't want the process to have a name)
    else:
      #All the if then statements and global variables utilized below are part of the method I use to keep comment boxes inside their process' corresponding
      #frames ... it also ensures that it is geometrically impossible for comment boxes to coincide

      vertical = (TimingDiagram.moduleverticality[str(rectangle)])+1
      (TimingDiagram.commenttracker[str(rectangle)]) += 1

      if (start_time >= 0.0 and end_time < 5.0):
        TimingDiagram.commenttracker[str(rectangle+'0')] += 1
        TimingDiagram.commenttracker[str(rectangle)]  = TimingDiagram.commenttracker[str(rectangle+'0')]
        TimingDiagram.commenttracker[str(rectangle+'FACTOR')] = 0
      if (start_time >= 5.0 and end_time < 10.0):
        TimingDiagram.commenttracker[str(rectangle+'1')] += 1
        TimingDiagram.commenttracker[str(rectangle)]  = TimingDiagram.commenttracker[str(rectangle+'1')]
        TimingDiagram.commenttracker[str(rectangle+'FACTOR')] = 1
      if (start_time >= 10.0 and end_time < 15.0):
        TimingDiagram.commenttracker[str(rectangle+'2')] += 1
        TimingDiagram.commenttracker[str(rectangle)]  = TimingDiagram.commenttracker[str(rectangle+'2')]
        TimingDiagram.commenttracker[str(rectangle+'FACTOR')] = 2
      if (start_time >= 15.0 and end_time < 20.0):
        TimingDiagram.commenttracker[str(rectangle+'3')] += 1
        TimingDiagram.commenttracker[str(rectangle)]  = TimingDiagram.commenttracker[str(rectangle+'3')]
        TimingDiagram.commenttracker[str(rectangle+'FACTOR')] = 3

      TimingDiagram.commenttracker["commentcount"] = TimingDiagram.commenttracker[str(rectangle)] + 7 *\
          TimingDiagram.commenttracker[str(rectangle+'FACTOR')]

    x = TimingDiagram.X_MARGIN + TimingDiagram.X_OFFSET + (0.03 * x_frame + (1.0 / 28.0) *\
	 ((x_frame - 0.06 * x_frame) * TimingDiagram.commenttracker["commentcount"]))

    y = TimingDiagram.Y_MARGIN + (1.0 / TimingDiagram.NUMBER_OF_MODULES) * TimingDiagram.y_framelength * vertical
    box_length = 0.025 * x_frame
    box_height = 0.0325 * TimingDiagram.y_framelength #TODO(kavin): find a way to eliminate these two weird constants using a geometric proportion constructed by existing variables
    outputfile.write("newpath\n")
    outputfile.write("%lf %lf moveto\n" % (x, y))
    outputfile.write("2 setlinewidth\n")
    outputfile.write("%lf %lf  lineto\n" % ((self.find_xposition(start_time) + self.find_xposition(end_time)) / 2, TimingDiagram.Y_MARGIN + (1.0 / TimingDiagram.NUMBER_OF_MODULES) * TimingDiagram.y_framelength * vertical - 0.33 * (1.0 / TimingDiagram.NUMBER_OF_MODULES) * TimingDiagram.y_framelength))
    outputfile.write("1 setlinewidth\n")
    outputfile.write("stroke\n")
    outputfile.write("newpath\n")
    outputfile.write("%lf %lf moveto\n" % (x, y))
    outputfile.write("%lf %lf moveto\n" % (x - (0.5 * box_length), y))
    outputfile.write("0 %lf rlineto\n" % (0.5 * box_height))
    outputfile.write("%lf %lf\n" % (x - 0.5 * box_length + 0.33 * box_length,y + 0.6 * box_height))
    outputfile.write("%lf %lf\n" % (x - 0.5 * box_length + 0.66 * box_length, y + 0.6 * box_height))
    outputfile.write("%lf %lf\n" % (x - 0.5 * box_length + box_length, (y * 0.99) + (0.5) * box_height))
    outputfile.write("curveto\n")
    outputfile.write("0 %lf rlineto\n" % (box_height * -1))
    outputfile.write("%lf %lf\n" % (x + 0.5 * box_length - 0.33 * box_length, y - 0.6 * box_height))
    outputfile.write("%lf %lf\n" % (x + 0.5 * box_length - 0.66 * box_length, y - 0.6 * box_height))
    outputfile.write("%lf %lf\n" % (x + 0.5 * box_length - box_length, (y * 0.99) - (0.5) * box_height))
    outputfile.write("curveto\n")
    outputfile.write("0 %lf rlineto\n" % (0.5 * box_height))
    outputfile.write("fill\n")
    self.font_initialization(outputfile, 5)
    outputfile.write("newpath\n")
    outputfile.write("0 0 0 setrgbcolor\n")
    outputfile.write("%lf %lf moveto\n" % (x, y))
    outputfile.write("%lf %lf moveto\n" % (x - (0.5 * box_length), y))
    outputfile.write("3 setlinewidth\n")
    outputfile.write("1 1 1 setrgbcolor\n")
    outputfile.write("(%s) show\n" % (text))


  def comment_box_cn (self, outputfile, rectangle, text, start_time, end_time):
    #Analogous to 'comment_box' except it draws comment_boxes for the CN superframe ...
    vertical = 1
    factor = 0
    x_frame = 4 * TimingDiagram.x_framelength
    if ("NONE" in text):
      bs = "garbage"
      #If the 'text' parameter is fed with the word NONE there will be no comment box created (in the case you didn't want the process to have a name)
    else:
      vertical = (TimingDiagram.moduleverticality[str(rectangle)])+1
      (TimingDiagram.commenttrackercn[str(rectangle)]) += 1

      if (start_time >= 0.0 and end_time < 5.0):
        TimingDiagram.commenttrackercn[str(rectangle+'0')] += 1
        TimingDiagram.commenttrackercn[str(rectangle)]  = TimingDiagram.commenttrackercn[str(rectangle+'0')]
        TimingDiagram.commenttrackercn[str(rectangle+'FACTOR')] = 0
      if (start_time >= 5.0 and end_time < 10.0):
        TimingDiagram.commenttrackercn[str(rectangle+'1')] += 1
        TimingDiagram.commenttrackercn[str(rectangle)]  = TimingDiagram.commenttrackercn[str(rectangle+'1')]
        TimingDiagram.commenttrackercn[str(rectangle+'FACTOR')] = 1
      if (start_time >= 10.0 and end_time < 15.0):
        TimingDiagram.commenttrackercn[str(rectangle+'2')] += 1
        TimingDiagram.commenttrackercn[str(rectangle)]  = TimingDiagram.commenttrackercn[str(rectangle+'2')]
        TimingDiagram.commenttrackercn[str(rectangle+'FACTOR')] = 2
      if (start_time >= 15.0 and end_time < 20.0):
        TimingDiagram.commenttrackercn[str(rectangle+'3')] += 1
        TimingDiagram.commenttrackercn[str(rectangle)]  = TimingDiagram.commenttrackercn[str(rectangle+'3')]
        TimingDiagram.commenttrackercn[str(rectangle+'FACTOR')] = 3

      TimingDiagram.commenttrackercn["commentcountcn"] = TimingDiagram.commenttrackercn[str(rectangle)] +\
          7 * TimingDiagram.commenttrackercn[str(rectangle+'FACTOR')]

    x = TimingDiagram.X_MARGIN + (0.03 * x_frame + (1.0 / 28.0) * ((x_frame - 0.06 * x_frame) *\
                                                                     TimingDiagram.commenttrackercn["commentcountcn"])) #a method to keep one comment box away from another
    y = TimingDiagram.Y_MARGIN - TimingDiagram.SPACE_BETWEEN - \
        TimingDiagram.y_framelength + (1.0 / TimingDiagram.NUMBER_OF_MODULES) *\
        TimingDiagram.y_framelength * vertical
    box_length = 0.025 * x_frame
    box_height = 0.0325 * TimingDiagram.y_framelength
    outputfile.write("newpath\n")
    outputfile.write("%lf %lf moveto\n" % (x, y))
    outputfile.write("2 setlinewidth\n")
    outputfile.write("%lf %lf  lineto\n" % ((self.find_xposition_cn(start_time)
                                    + self.find_xposition_cn(end_time)) / 2,
                                   TimingDiagram.Y_MARGIN -TimingDiagram.SPACE_BETWEEN
                                   - TimingDiagram.y_framelength
                                   + (1.0 / TimingDiagram.NUMBER_OF_MODULES)
                                   * TimingDiagram.y_framelength * vertical
                                   - 0.33 * (1.0 / TimingDiagram.NUMBER_OF_MODULES)
                                   * TimingDiagram.y_framelength)) # draws a line from the center of the process to the center of the comment box
    outputfile.write("1 setlinewidth\n")
    outputfile.write("stroke\n")
    outputfile.write("newpath\n")
    outputfile.write("%lf %lf moveto\n" % (x, y))
    outputfile.write("%lf %lf moveto\n" % (x - (0.5 * box_length), y))
    outputfile.write("0 %lf rlineto\n" % (0.5 * box_height))
    outputfile.write("%lf %lf\n" % (x - 0.5 * box_length + 0.33 * box_length,y + 0.6 * box_height))
    outputfile.write("%lf %lf\n" % (x - 0.5 * box_length + 0.66 * box_length, y + 0.6 * box_height))
    outputfile.write("%lf %lf\n" % (x - 0.5 * box_length + box_length, (y * 0.99) + (0.5) * box_height))
    outputfile.write("curveto\n")
    outputfile.write("0 %lf rlineto\n" % (box_height * -1))
    outputfile.write("%lf %lf\n" % (x + 0.5 * box_length - 0.33 * box_length, y - 0.6 * box_height))
    outputfile.write("%lf %lf\n" % (x + 0.5 * box_length - 0.66 * box_length, y - 0.6 * box_height))
    outputfile.write("%lf %lf\n" % (x + 0.5 * box_length - box_length, (y * 0.99) - (0.5) * box_height))
    outputfile.write("curveto\n")
    outputfile.write("0 %lf rlineto\n" % (0.5 * box_height))
    outputfile.write("fill\n")
    self.font_initialization(outputfile, 5)
    outputfile.write("newpath\n")
    outputfile.write("0 0 0 setrgbcolor\n")
    outputfile.write("%lf %lf moveto\n" % (x, y))
    outputfile.write("%lf %lf moveto\n" % (x - (0.5 * box_length), y))
    outputfile.write("3 setlinewidth\n")
    outputfile.write("1 1 1 setrgbcolor\n")
    outputfile.write("(%s) show\n" % (text))

  def reset_global_dict(self):
    TimingDiagram.commenttracker = {"PRU0": 0, "PRU1" : 0, "PRU2" : 0, "PRU3": 0, "PRU": 0, "PRUFACTOR": 0,
                    "PCD0": 0, "PCD1" : 0, "PCD2" : 0, "PCD3" : 0, "PCD": 0, "PCDFACTOR": 0,
                    "TFS0": 0, "TFS1" : 0, "TFS2" : 0, "TFS3" : 0, "TFS": 0, "TFSFACTOR": 0,
                    "AXD0": 0, "AXD1" : 0, "AXD2" : 0, "AXD3" : 0, "AXD": 0, "AXDFACTOR": 0,
                    "AXE0": 0, "AXE1" : 0, "AXE2" : 0, "AXE3" : 0, "AXE": 0, "AXEFACTOR": 0,
                    "BFW0": 0, "BFW1" : 0, "BFW2" : 0, "BFW3" : 0, "BFW": 0, "BFWFACTOR": 0,
                    "MFSM0": 0, "MFSM1" : 0, "MFSM2" : 0, "MFMS3" : 0, "MFSM": 0, "MFSMFACTOR": 0,
                    "CAL0": 0, "CAL1" : 0, "CAL2" : 0, "CAL3" : 0, "CAL": 0, "CALFACTOR": 0,
                      "commentcount": 0}

    TimingDiagram.commenttrackercn = {"PRU0": 0, "PRU1" : 0, "PRU2" : 0, "PRU3": 0, "PRU": 0, "PRUFACTOR": 0,
                    "PCD0": 0, "PCD1" : 0, "PCD2" : 0, "PCD3" : 0, "PCD": 0, "PCDFACTOR": 0,
                    "TFS0": 0, "TFS1" : 0, "TFS2" : 0, "TFS3" : 0, "TFS": 0, "TFSFACTOR": 0,
                    "AXD0": 0, "AXD1" : 0, "AXD2" : 0, "AXD3" : 0, "AXD": 0, "AXDFACTOR": 0,
                    "AXE0": 0, "AXE1" : 0, "AXE2" : 0, "AXE3" : 0, "AXE": 0, "AXEFACTOR": 0,
                    "BFW0": 0, "BFW1" : 0, "BFW2" : 0, "BFW3" : 0, "BFW": 0, "BFWFACTOR": 0,
                    "MFSM0": 0, "MFSM1" : 0, "MFSM2" : 0, "MFMS3" : 0, "MFSM": 0, "MFSMFACTOR": 0,
                    "CAL0": 0, "CAL1" : 0, "CAL2" : 0, "CAL3" : 0, "CAL": 0, "CALFACTOR": 0,
                        "commentcountcn": 0}

  def generate_timing_diagram (self, outputfile):
    """Main function which calls all the other functions to produce the two frames, the overlaying rectangles, and the legends"""
    self.landscape_initialization (outputfile)
    self.title (outputfile, 32, "en")
    self.title (outputfile, 32, "cn")
    self.legend (outputfile, 12, "en")
    self.legend (outputfile, 12, "cn")
    self.overhead_rect (outputfile, "en")
    self.overhead_rect (outputfile, "cn")
    self.font_initialization (outputfile,6)
    self.draw_template(outputfile)
    self.draw_template_cn(outputfile)
    self.draw_modules (outputfile, "en")
    self.draw_modules (outputfile, "cn")
