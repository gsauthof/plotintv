Script for plotting time interval based data.

It uses [matplotlib][1] and is thus written in [Python][2].

The input file format is a simple comma separated one and
matplotlib supports a bunch of output file formats (SVG, PNG,
PDF, ...) - just specify a well known file extension. If no
output file is specified the default matplotlib viewer is displayed,
where the plot can be zoomed, rotated etc. The viewer also provides
a save feature.

2013-08-23, Georg Sauthoff <mail@georg.so>

## Usecases

Some data visualization where the input is inherently tied to
time intervals. Examples:

- Rows from a database table containing pairwise contracting information,
  and each pair may have multiple subcontracts. All contracts have
  an effective date and an enddate. The visualization may make certain
  patterns obvious, e.g. clusters, incomplete overlaps, gaps,
  illegal overlaps ...

- Visualization of process runtimes in a batch environment.

- Visualization of support intervals


## Examples

Create 2D plot, where the x-axis is the time and the y-axis lists
categories:

    $ ./plotintv.py some.inp -s sub_cat_name_a -c color_a \
                             -s sub_cat_name_b -c color_b \
         --legend-pos='upper left' --ylabel main_cat_name

This launches the interactive matplotlib viewer.

For pairs of main categories there is a 3D mode:

    $ ./plotintv.py some.inp -s sub_cat_name_a -c color_a \
                             -s sub_cat_name_b -c color_b \
         --ylabel main_cat_left_name --zlabel main_cat_right_name \
         --3d

See also `--help` for a complete list of options. Graphic files can
be directly created, some default parameters are customizable.

## Basics

Sub-categories are grouped together when displaying the main
categories.

## Input format

See the output of `--help`.

## License

[GPLv3+][gpl]

[1]: http://matplotlib.org/
[2]: http://en.wikipedia.org/wiki/Python_(programming_language)
[gpl]:   http://www.gnu.org/licenses/gpl.html
