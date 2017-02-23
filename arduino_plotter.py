"""
Display analog data from Arduino using Python (matplotlib)

Code editted by J. Sganga for Bioe123
Date: 2/20/2017

Original:
Author: Mahesh Venkitachalam
Website: electronut.in
git: https://gist.github.com/electronut/d5e5f68c610821e311b0
"""

import sys, serial
import numpy as np
from collections import deque
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

    
# plot class
class AnalogPlot(object):
  # constr
    def __init__(self, strPort, maxLen, baud_rate):
      # open serial port
      self.arduino = serial.Serial(strPort, baud_rate)
      self.maxLen  = maxLen
      # grab a printed line to check length
      stream = self.arduino.readline()
      stream_values = [float(val) for val in stream.split()]
      # plot nothing, but want handle to line object
      self.n_lines = len(stream_values)
      self.lines = []
      for i in range(self.n_lines):
        line, = plt.plot([], [])
        self.lines.append(line)
      self.data    = []
      for i in range(self.n_lines):
        self.data.append(deque([0.0]*maxLen))

    # add data
    def add_to_plot(self, stream_values):
        for i in range(self.n_lines):
            print(i, stream_values)
            val    = stream_values[i]
            line   = self.lines[i]
            data_q = self.data[i]
            data_q.popleft()
            data_q.append(val)
            line.set_data(np.linspace(-self.maxLen,0,self.maxLen), data_q)

    # update plot
    def update(self, frameNum):
      try:
          stream = self.arduino.readline()
          # while self.arduino.inWaiting() > 0: # clears buffer
          #     stream = self.arduino.readline()
          stream_values = [float(val) for val in stream.split()]
          self.add_to_plot(stream_values)
      except KeyboardInterrupt:
          print('exiting')
      
    # clean up
    def close(self):
      # close serial
      self.arduino.flush()
      self.arduino.close()    

# main() function
def main(port, baud_rate):

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

    

    analogPlot = AnalogPlot(port, data_length, baud_rate)
    print('plotting data...')

    anim = animation.FuncAnimation(fig, analogPlot.update, 
                                 interval=50)

    # show plot
    plt.show()

    # clean up
    analogPlot.close()

    print('exiting.')
  

# call main, CHANGE THESE VALUES!!!
if __name__ == '__main__':
    main('COM6', 9600)