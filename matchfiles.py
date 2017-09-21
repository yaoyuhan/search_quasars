#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 31 15:05:27 2017

@author: kburdge
"""
import pandas as pd
import tables
import numpy as np
import glob
from gatspy.periodic import LombScargleFast
import matplotlib.pyplot as plt
n=0
p=0
for f in glob.iglob("/scr2/ptf/variable/matches_ipac/sex/d100043/*.pytable"):
    with tables.open_file(f) as store:
        for tbl in store.walk_nodes("/", "Table"):
            if tbl.name in ["sourcedata", "transientdata"]:
                group = tbl._v_parent
            	break
    	srcdata = pd.DataFrame.from_records(group.sourcedata[:])
    	srcdata.sort_values('matchedSourceID', axis=0, inplace=True)
    	exposures = pd.DataFrame.from_records(group.exposures[:])
    	merged = srcdata.merge(exposures, on="pid")
    	#print(merged.matchedSourceID.unique())
    	for k in merged.matchedSourceID.unique():
        	df = merged[merged['matchedSourceID'] == k]
		fieldID=df['fieldID']
		p=p+1
		if fieldID.values[0]==100043:
        		RA = df.ra
        		Dec = df.dec
        		x = df.mag
			err=df.magErr
        		obsHJD = df.obsHJD
        		if len(x)>1:
            			output=np.column_stack((obsHJD.values, x.values, err.values))
				np.savetxt(str(RA.values[0])+"_"+str(Dec.values[0]),output)
				n=n+1
				print(n)

