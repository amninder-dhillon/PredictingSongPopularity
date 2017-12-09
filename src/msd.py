import os
import glob
import json
import numpy as np
import pandas as pd
import lib.hdf5_getters as hdf5_getters

def get_available_methods():
	methods = [i for i in dir(hdf5_getters)]
	return [i for i in methods if (("get_" in i) and ("get_num_songs"!=i))]

def read_metadata(h5):
	hdf5_file = hdf5_getters.open_h5_file_read(h5)
	methods = get_available_methods()
	metadata = {}
	for method in methods:
		result = hdf5_getters.__getattribute__(method)(hdf5_file)
		if isinstance(result,np.ndarray):
			result = json.dumps(result.tolist())
		metadata[method[4:]] = result 

	hdf5_file.close()
	return metadata

def create_summary_csv(rootdir,csv_file):
	first_run = True
	ext = "h5"
	df = None
	df_temp = None;
	for root,dirs,files in os.walk(rootdir):
		files = glob.glob(os.path.join(root,"*"+ext))
		for f in files:
			metadata = read_metadata(f)
			if first_run:
				df = pd.DataFrame.from_dict(metadata,orient='index').transpose()
				first_run = False
			else:
				df_temp = pd.DataFrame.from_dict(metadata,orient='index').transpose()
				df = df.append(df_temp)
	df.reset_index(drop=True,inplace=True)
	df.to_csv(csv_file)
	return df