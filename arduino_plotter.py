"""
Display analog data from Arduino using Python (matplotlib)

Code editted by J. Sganga for Bioe123
Date: 2/20/2017

Original:
Author: Mahesh Venkitachalam
Website: electronut.in
"""

import sys, serial, argparse
import numpy as np
from time import sleep
from collections import deque

import matplotlib.pyplot as plt 
import matplotlib.animation as animation

    
# plot class
class AnalogPlot(object):
  # constr
    def __init__(self, strPort, maxLen, baud_rate, lines):
      # open serial port
      self.ser     = serial.Serial(strPort, baud_rate)
      self.maxLen  = maxLen
      self.n_lines = len(lines)
      self.lines   = lines
      self.data    = []
      for i in range(n_lines):
        self.data.append(deque([0.0]*maxLen))

    # add data
    def add_to_plot(self, stream_values, lines):
        for i in range(self.n_lines):
            val    = stream_values[i]
            line   = self.lines[i]
            data_q = self.data[i]
            data_q.popleft()
            data_q.append(val)
            line.set_data(np.linspace(-self.maxLen,0,self.maxLen), data_q)


    # update plot
    def update(self, frameNum, lines):
      try:
          stream = self.ser.readline()
          stream_values = [float(val) for val in stream.split()]
          self.add_to_plot(stream_values, lines)
      except KeyboardInterrupt:
          print('exiting')
      
    # clean up
    def close(self):
      # close serial
      self.ser.flush()
      self.ser.close()    

# main() function
def main(port, baud_rate, n_lines):

    print('reading from serial port ' + port + '...')

    # plot parameters
    data_length = 100 # number of points shown in window
    
    # set up figure
    fig = plt.figure()
    plt.xlabel('Time History')
    plt.ylabel('Value')
    plt.title('Real Time Plot for Port ' + port)
    x_min, x_max = -data_length, 5
    plt.xlim([x_min, x_max])
    y_min, y_max = 0, 1023
    plt.ylim([y_min, y_max])

    # plot nothing, but want handle to line object
    lines = []
    for i in range(n_lines):
        line, = plt.plot([], [])
        lines.append(line)

    analogPlot = AnalogPlot(port, data_length, baud_rate, lines)
    print('plotting data...')

    anim = animation.FuncAnimation(fig, analogPlot.update, 
                                 interval=50)

    # show plot
    plt.show()

    # clean up
    analogPlot.close()

    print('exiting.')
  

# call main
if __name__ == '__main__':
    main('COM6', 9600, 2)