'''
sequences2graph.py - align sequences and put them into a graph
==============================================================

:Author: Andreas Heger
:Release: $Id$
:Date: |today|
:Tags: Python

Purpose
-------

.. todo::
   
   describe purpose of the script.

Usage
-----

Example::

   python sequences2graph.py --help

Type::

   python sequences2graph.py --help

for command line help.

Command line options
--------------------

'''
import os
import sys
import string
import re
import getopt

import CGAT.Experiment as E
import CGAT.Genomics as Genomics
import CGAT.Intervalls as Intervalls
import CGAT.PredictionParser as PredictionParser
import alignlib

param_long_options=["verbose=", "help", "version"]
param_short_options="v:ho:t:"

param_loglevel = 1

param_overlap_residues = 90
param_filename_filter_tokens = None

param_gop = -10.0
param_gep = -2.0

##------------------------------------------------------------
if __name__ == '__main__':

    try:
        optlist, args = getopt.getopt(sys.argv[1:], param_short_options, param_long_options)
    except getopt.error, msg:
        print globals()["__doc__"], msg
        sys.exit(2)
                                                                                                                                                             
    for o,a in optlist:
        if o in ( "-v", "--verbose" ):
            param_loglevel = int(a)
        elif o in ( "--version", ):
            print "version="
            sys.exit(0)
        elif o in ( "-h", "--help" ):
            print globals()["__doc__"]
            sys.exit(0)

    alignator = alignlib.makeAlignatorDPFull( alignlib.ALIGNMENT_LOCAL, param_gop, param_gep )
    map_query2token = alignlib.makeAlignmentVector()
    
    for line in sys.stdin:
        if line[0] == "#": continue

        query_token, sbjct_token, query_sequence, sbjct_sequence = string.split(line[:-1], "\t")

        map_query2token.clear()
        row = alignlib.makeSequence(query_sequence)
        col = alignlib.makeSequence(sbjct_sequence)
        alignator.align( map_query2token, row, col )

        pidentity = 100.0 * alignlib.calculatePercentIdentity( map_query2token, row, col )
        psimilarity = 100.0 * alignlib.calculatePercentSimilarity( map_query2token )        
        print string.join( map(str, (
            query_token, sbjct_token,
            map_query2token.getScore(),
            alignlib.AlignmentFormatEmissions( map_query2token ),
            pidentity,
            psimilarity,
            map_query2token.getNumGaps()) ), "\t" )
            
            
            
        
