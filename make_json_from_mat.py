import os
import json

from tqdm import tqdm
from scipy.io import loadmat
import pandas as pd


def main():
	mat_file = './data/paperdoll_dataset.mat'
	f = loadmat(mat_file)
	labels = f['labels'][0]
	samples = f['samples'][0]

	# make labels/categories.tsv
	sr_ctg = pd.Series([label[0] for label in labels])
	sr_ctg.index = sr_ctg.index+1
	df_ctg = sr_ctg.reset_index()
	df_ctg.columns = ['category_id', 'category']

	out_file = './labels/categories.tsv'
	out_dir = os.path.dirname(out_file)
	if not os.path.isdir(out_dir):
		os.makedirs(out_dir)
	df_ctg.to_csv(out_file, index=False, sep='\t')

	# make labels/paperdoll.json
	d = [{
		"snap_id": int(sample[0][0, 0]),
		"snap_url": sample[1][0],
		"post_url": sample[2][0],
		"items": [
			{
				"category_id": int(tag_id),
				"category": tag
			} 
			for tag_id, tag
			in list(zip(
				sample[3][0].tolist(),
				sr_ctg[sample[3][0]].tolist(),
			))
		]
	} for sample in tqdm(samples)]

	out_file = './labels/paperdoll.json'
	out_dir = os.path.dirname(out_file)
	if not os.path.isdir(out_dir):
		os.makedirs(out_dir)
	with open(out_file, 'w') as f:
		json.dump(d, f, indent=4)


if __name__=="__main__":
	main()