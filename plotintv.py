#!/usr/bin/env python

# 2013-08-11, Georg Sauthoff <mail@georg.so>

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from StringIO import StringIO

import datetime as dt

import logging
import sys


log = logging.getLogger("plotintv")
log.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler .setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s",
                              #'%a, %d %b %Y %H:%M:%S')
                              '%H:%M:%S')
handler.setFormatter(formatter)
log.addHandler(handler)

file1 = StringIO(
    "#cat,sub,from,to,color\n"
    "foo,x,2012-01-01_00:00:00,2012-03-31_23:23:59,red\n"
    "foo,x,2012-04-01_00:00:00,2012-12-12_23:23:59,red\n"
    "foo,y,2012-02-01_00:00:00,2012-04-30_23:23:59,green\n"
    "foo,y,2013-02-01_00:00:00,2016-04-30_23:23:59,green\n"
    "bar,x,2012-01-01_00:00:00,2013-03-31_23:23:59,red\n"
    "bar,y,2012-02-01_00:00:00,2013-04-30_23:23:59,green\n"
    )

def str2dt(s):
  return dt.datetime.strptime(s, '%Y-%m-%d_%H:%M:%S')


def read_data(file1):
  arr = np.genfromtxt(file1, delimiter=',', autostrip=True,
    dtype=('|S20','|S20', dt.datetime, dt.datetime,'|S20'),
    converters={2:str2dt, 3:str2dt}
    )
  return arr

def extract_ticks(arr):
  h = {}
  s = set()
  r = []
  y = 0;
  suby = {}
  h2 = {}
  for i in arr:
    cat = i[0]
    sub = i[1]
    if cat not in s:
      s.add(cat)
      r.append(cat)
      h[cat] = y
      y += 1
      suby[cat] = 0.0
    if (cat, sub) not in h2:
      h2[cat, sub] = suby[cat]
    suby[cat] -= 0.2
  return r, h, h2

# solid_capstyle="projecting"

def plot_intv(arr, pos, spos):
  for i in arr:
    cat = i[0]
    sub = i[1]
    d1 = i[2]
    d2 = i[3]
    col = i[4]
    y = pos[cat] + spos[cat, sub]
    #plt.scatter(np.array([d1, d2]), np.array([y,y]), s=50, c=col, lw=2, edgecolor=col, marker='|')
    plt.scatter(d1, y, s=50, c=col, lw=1, edgecolor=col, marker= 6) #'<' )
    plt.scatter(d2, y, s=50, c=col, lw=1, edgecolor=col, marker= 7) #'>')
    plt.hlines(y, d1, d2, colors=col)


def plot_arr(arr):
  cats, pos, spos = extract_ticks(arr)
  log.debug('%s' % cats)
  #figure, axes = plt.subplots(1)
  figure = plt.figure()
  axes = plt.subplot(111)
  # rotate, align labels
  figure.autofmt_xdate()
  axes.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
  axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
  
  plt.title(options.title)
  plt.yticks(np.arange(len(cats)), cats)
  plt.ylim(-0.5, len(cats)+0.5)

  line = plt.Line2D((0,1), (1,1), color='r', lw=1)
  plt.legend([line], ['Red'], loc=options.legend_pos)

  plt.xlabel(options.xlabel)
  if options.ylabel is not None:
    plt.ylabel(options.ylabel)
  
  plot_intv(arr, pos, spos)


def main(file_obj):
  arr = read_data(file_obj)
  log.debug('%s' % arr)
  
  plot_arr(arr)
 
  if options.output == None:
    plt.show()
  else:
    plt.savefig(options.output, dpi=options.dpi)

def enable_debug_output(option, opt, value, parser):
  log.setLevel(logging.DEBUG)
  handler.setLevel(logging.DEBUG)
  log.debug('Enable DEBUG output')

program_version = "0.5"


if __name__ == '__main__':
  import optparse
  opts = optparse.OptionParser(
    usage =
      'Usage: %prog  (-v)? (-x|input_file) (-o graph.ext)'
      '\n\nInput file format:\n'
      '#cat,sub,from,to,color\n'
      '...,...,YYYY-MM-DD_HH24:MI:SS,...,(red|green|...)'
    ,
    version = program_version,
    description =
      'Turns list of time intervals into plots.',
    epilog =
      '2013-08-11, Georg Sauthoff <mail@georg.so>'
    # by default: add_help_option = True
  )
  opts.add_option('-v', '--verbose',
    action='callback', callback=enable_debug_output)
  opts.add_option('-x', '--example',
    action='store_true', default=False, dest='example')
  opts.add_option('-o', '--output', dest='output')
  opts.add_option('--title', dest='title',
      default='date time intervals')
  opts.add_option('--dpi', type='int', dest='dpi') #, default=72)
  opts.add_option('--legend-pos', dest='legend_pos',
      default='upper right')
  opts.add_option('--xlabel', dest='xlabel',
      default='time')
  opts.add_option('--ylabel', dest='ylabel',
      default=None)
  opts.add_option('-s', dest='subcats', action='append',
      help = 'for display in the legend - supply multiple times'
      )
  opts.add_option('-c', dest='colors', action='append',
      help = 'for display in the legend - supply multiple times')

  (options, args) = opts.parse_args()

  log.debug('%s' % options.subcats)

  if options.example:
    main(file1)
  else:
    if len(args) != 1:
      log.error('Specified %d instead of 1 positional argument' % len(args) )
      sys.exit(1)
    main(file(args[0]))


