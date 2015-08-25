#! /usr/bin/env python

import sys
import pickle
import time
from pattern.web import URL, DOM

def extract_data_ML(i):
    url = 'http://macaulaylibrary.org/audio/%s' % i
    page = URL(url).download()
    dom = DOM(page)
    description = dom('meta')[0].attr['content']
    result = [x.content for x in dom('script') if 'jwplayer(' in x.content][0]
    result = [x.strip() for x in result.split('\n') if x.strip().startswith('file')][0]
    path_to_mp3 =  result.split('"')[1]
    return {'index': i, 'desc': description, 'mp3': path_to_mp3}

if __name__ == '__main__':
	start_time = time.time()
	number = int(sys.argv[1])
	collection = []
	for i in range(number):
		try:
			collection.append(extract_data_ML(i+1))
			sys.stdout.write('\r%d/%d' % (i+1, number))
			sys.stdout.flush()
		except:
			continue

		if (i+1) % 1000 == 0:
			pickle.dump(collection, open('snaps/birds-%s.p' % (i+1), 'wb'))

	final_file = 'snaps/birds-final.p'
	pickle.dump(collection, open(final_file, 'wb'))
	total_time = time.time() - start_time
	print '\nDone: Number of entries collected: %s/%s' % (len(collection), number)
	print 'Total time: %s seconds (%s per second)' % (total_time, number/total_time)
	print 'Results saved in %s' % final_file
