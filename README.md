# Paper Doll Dataset

This dataset is proposed in the paper, [(K. Yamaguchi, M. Hadi Kiapour, & T. L. Berg. 2013) Paper Doll Parsing: Retrieving Similar Styles to Parse Clothing Items.](http://vision.is.tohoku.ac.jp/~kyamagu/papers/yamaguchi2013paper.pdf).

https://github.com/kyamagu/paperdoll


## Dataset Schema

- `data/paperdoll_dataset.mat`: 568,340 snap image urls with categories
	- 53 categories
- `data/fashionista_v0.2.mat`: 685 snap images and segmentation maps
	- `truths` (struct array): ground truth annotatation
	- `predictions` (struct array): predicted parsing results
	- `test_index`: samples used for training


See the [official page](http://vision.is.tohoku.ac.jp/~kyamagu/ja/research/paperdoll/)'s **Data foramt** for the original schema of the mat files.

Our json schema is the followings.

- `labels/paperdoll.json`
	- 568,340 samples
	- `snap_id` (int): starts from 1
	- `snap_url` (str): image url
	- `post_url` (str): post page url including the snap
	- `items`
		- `category_id` (int): 1 to 53
		- `category` (str)
- `labels/categories.tsv`	
	- `category_id` (int): 1 to 53
	- `category` (str)


## Setup

```
pipenv sync
```

or

```
pip install -r requirements.txt
```

```
cd $DATASET_ROOT/raw
wget http://vision.cs.stonybrook.edu/~kyamagu/paperdoll/data-v1.0.tar
tar xvf data-v1.0.tar
```

```
wget https://github.com/kyamagu/paperdoll/raw/master/data/chictopia/chictopia.sql.gz
gunzip -c chictopia.sql.gz | sqlite3 chictopia.sqlite3
```

```
python mat2json_paperdoll.py
```

the followings will be made from `data/paperdoll_dataset.mat`.

- `labels/paperdoll.json`
- `labels/categories.tsv`	

```
python download_images.py
```

If time out occurs,

- increase `-r` (the number of requests) more than 100 (default)
- increase `-t` (the time to wait until time out) more than 180\[s\] (default)