#!/usr/bin/env python

# 2013-08-11, Georg Sauthoff <mail@georg.so>

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from mpl_toolkits.mplot3d import Axes3D

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
    "foo,x,2012-01-01_00:00:00,2012-03-31_23:23:59,red,\n"
    "foo,x,2012-04-01_00:00:00,2012-12-12_23:23:59,red,\n"
    "foo,y,2012-02-01_00:00:00,2012-04-30_23:23:59,green,\n"
    "foo,y,2013-02-01_00:00:00,2016-04-30_23:23:59,green,\n"
    "bar,x,2012-01-01_00:00:00,2013-03-31_23:23:59,red,\n"
    "bar,y,2012-02-01_00:00:00,2013-04-30_23:23:59,green,\n"
    )

def str2dt(s):
  return dt.datetime.strptime(s, '%Y-%m-%d_%H:%M:%S')


def read_data(file1):
  arr = np.genfromtxt(file1, delimiter=',', autostrip=True,
    dtype=('|S20','|S20', dt.datetime, dt.datetime,'|S20','|S20'),
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
    suby[cat] -= -options.displace
  return r, h, h2

def extract3d_ticks(arr):
  h_y = {}
  h_z = {}
  s_y = set()
  s_z = set()
  r_y = []
  r_z = []
  y = 0
  z = 0
  subyz = {}
  h2 = {}
  for i in arr:
    cat = i[0]
    [cat_y, cat_z] = cat.split('_')
    sub = i[1]
    if cat_y not in s_y:
      s_y.add(cat_y)
      r_y.append(cat_y)
      h_y[cat_y] = y
      y += 1
    if cat_z not in s_z:
      s_z.add(cat_z)
      r_z.append(cat_z)
      h_z[cat_z] = z
      z += 1
    if (cat_y, cat_z, sub) not in h2:
      if (cat_y, cat_z) not in subyz:
        h2[cat_y, cat_z, sub] = 0.0
        subyz[cat_y, cat_z] = 0.0
      else:
        h2[cat_y, cat_z, sub] = subyz[cat_y, cat_z]
    subyz[cat_y, cat_z] -= -options.displace
  return (r_y, r_z), (h_y, h_z), h2

# solid_capstyle="projecting"

def plot_intv(arr, pos, spos):
  for i in arr:
    cat = i[0]
    sub = i[1]
    d1 = i[2]
    d2 = i[3]
    col = i[4]
    info = i[5]
    y = pos[cat] + spos[cat, sub]
    #plt.scatter(np.array([d1, d2]), np.array([y,y]), s=50, c=col, lw=2, edgecolor=col, marker='|')
    plt.scatter(d1, y, s=50, c=col, lw=1, edgecolor=col, marker= 6) #'<' )
    plt.scatter(d2, y, s=50, c=col, lw=1, edgecolor=col, marker= 7) #'>')
    plt.hlines(y, d1, d2, colors=col)
    if info != '':
      plt.annotate(info, xy=(d1+dt.timedelta(days=10), y+0.02), fontsize=8)


def plot_legend():
  lines = []
  for color in options.colors:
    line = plt.Line2D((0,1), (1,1), color=color, lw=1)
    lines.append(line)
  plt.legend(lines, options.subcats, loc=options.legend_pos)

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

  plot_legend()

  plt.xlabel(options.xlabel)
  if options.ylabel is not None:
    plt.ylabel(options.ylabel)
  
  plot_intv(arr, pos, spos)

def plot3d_intv(axes, arr, (pos_y, pos_z), spos):
  for i in arr:
    cat = i[0]
    [cat_y, cat_z] = cat.split('_')
    sub = i[1]
    d1 = i[2]
    d2 = i[3]
    col = i[4]
    info = i[5]
    y = pos_y[cat_y]
    z = pos_z[cat_z]
    if options.reverse_pkg:
      z += spos[cat_y, cat_z, sub]
    else:
      y += spos[cat_y, cat_z, sub]

    axes.plot([mdates.date2num(d1), mdates.date2num(d2)], [y,y], zs=[z, z],
              color=col)
    axes.scatter(mdates.date2num(d1), y, z, s=50, c=col, lw=1, edgecolor=col,
              marker= 6) #'<' )
    axes.scatter(mdates.date2num(d2), y, z, s=50, c=col, lw=1, edgecolor=col,
              marker= 7) #'>')

    if info != '':
      axes.text(mdates.date2num(d1+dt.timedelta(days=10)), y+0.02, z, info,
              fontsize=8)

def plot3d_arr(arr):
  (cats_y, cats_z), (pos_y, pos_z), spos = extract3d_ticks(arr)
  log.debug('%s' % cats_y)
  log.debug('%s' % cats_z)
  figure = plt.figure()
  axes = figure.add_subplot(111, projection='3d')
  #axes = figure.add_subplot(1,1,1, projection='3d')
  #axes = figure.gca(projection='3d')

  # rotate, align labels
  figure.autofmt_xdate()
  axes.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
  axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

  plt.title(options.title)
  axes.set_yticks(np.arange(len(cats_y)))
  axes.set_yticklabels(cats_y)
  axes.set_ylim3d(-0.5, len(cats_y)+0.5)

  axes.set_zticks(np.arange(len(cats_z)))
  axes.set_zticklabels(cats_z)
  axes.set_zlim3d(-0.5, len(cats_z)+0.5)

  plot_legend()

  axes.set_xlabel(options.xlabel)
  if options.ylabel is not None:
    axes.set_ylabel(options.ylabel)
  if options.zlabel is not None:
    axes.set_zlabel(options.zlabel)

  plot3d_intv(axes, arr, (pos_y, pos_z), spos)


def main(file_obj):
  arr = read_data(file_obj)
  log.debug('%s' % arr)

  if options.ddd:
    plot3d_arr(arr)
  else:
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
      '...,...,YYYY-MM-DD_HH24:MI:SS,...,(red|green|...),marker\n'
      'or for --3d:\n'
      'cata_catb,...,YYYY-MM-DD_HH24:MI:SS,...,(red|green|...),marker\n'
    ,
    version = program_version,
    description =
      'Turns list of time intervals into plots.',
    epilog =
      '2013-08-23, Georg Sauthoff <mail@georg.so>'
    # by default: add_help_option = True
  )
  opts.add_option('-v', '--verbose',
    action='callback', callback=enable_debug_output)
  opts.add_option('-x', '--example',
    action='store_true', default=False, dest='example')
  opts.add_option('--3d',
    action='store_true', default=False, dest='ddd')
  opts.add_option('--reverse-pkg',
    action='store_true', default=False, dest='reverse_pkg',
    help = 'use other dimension for grouping of sub-cats (in 3d)'
    )
  opts.add_option('--displace', type='float', dest='displace',
      default=0.1, help='space between sub cats')
  opts.add_option('-o', '--output', dest='output')
  opts.add_option('--title', dest='title',
      default='date time intervals')
  opts.add_option('--dpi', type='int', dest='dpi') #, default=72)
  opts.add_option('--legend-pos', dest='legend_pos',
      default='upper right')
  opts.add_option('--xlabel', dest='xlabel', default='time')
  opts.add_option('--ylabel', dest='ylabel', default=None)
  opts.add_option('--zlabel', dest='zlabel', default=None)
  opts.add_option('-s', dest='subcats', action='append',
      help = 'for display in the legend - supply multiple times'
      )
  opts.add_option('-c', dest='colors', action='append',
      help = 'for display in the legend - supply multiple times')

  (options, args) = opts.parse_args()

  log.debug('%s' % options.subcats)
  log.debug('%s' % options.colors)

  if options.example:
    main(file1)
  else:
    if len(args) != 1:
      log.error('Specified %d instead of 1 positional argument' % len(args) )
      sys.exit(1)
    main(file(args[0]))


