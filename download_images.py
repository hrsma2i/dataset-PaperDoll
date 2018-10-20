#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import argparse

import asyncio
import aiohttp
from tqdm import tqdm
import pandas as pd

# get content and write it to file
def write_to_file(file, content):
	with open(file, 'wb') as f:
		f.write(content)


# a helper coroutine to perform GET requests:
async def get(*args, **kwargs):
	async with aiohttp.ClientSession() as session:
		try:
			async with session.get(*args, **kwargs) as res:
				tqdm.write('{}'.format(res.status))
				return await res.content.read()
		except:
			return None


async def download_file(url, file, seconds):
	# this routine is protected by a semaphore
	with await sem:
		timeout = aiohttp.ClientTimeout(total=seconds)
		content = await get(url, timeout=timeout)

		if content is not None:
			write_to_file(file, content)
		else:
			tqdm.write('Error or Time out: {}'.format(file))

'''
make nice progressbar
install it by using `pip install tqdm`
'''
async def wait_with_progressbar(coros):
	coros = [await f 
			 for f in tqdm(asyncio.as_completed(coros), total=len(coros))]
	return await coros


if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'-r', '--num_requests',
		type=int,
		default=100)
	parser.add_argument(
		'-t',
		type=int,
		default=180,
		help='seconds to wait until time out')
	args = parser.parse_args()

	img_dir = './test_images'
	if not os.path.isdir(img_dir):
		os.makedirs(img_dir)

	df = pd.read_json("./labels/paperdoll.json")[['snap_url','snap_id']]
	df['img_file'] = df.apply(lambda row:
			                     os.path.join(
			                     	img_dir,
			                     	'{}.jpg'.format(row['snap_id'])),
		                      axis=1)
	df = df[df['img_file'].apply(lambda file: 
			                        not os.path.exists(file))]
	df = df[['snap_url', 'img_file']]


	# avoid to many requests(coros) the same time.
	# limit them by setting semaphores (simultaneous requests)
	sem = asyncio.Semaphore(args.num_requests)

	coros = [download_file(url, img_file, args.t) 
			 for _, url, img_file in df.itertuples()]
	eloop = asyncio.get_event_loop()
	#eloop.run_until_complete(asyncio.wait(coros))
	eloop.run_until_complete(wait_with_progressbar(coros))
	eloop.close()