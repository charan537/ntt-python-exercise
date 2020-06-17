# Determine distinct pairs
def findPairs(a,k):
	freq_map = {}
	for x in a:
		f = freq_map.get(x,0)
		freq_map[x] = f+1

	distinct_a = list(freq_map.keys())
	distinct_a.sort()
	
	k = abs(k)
	n = len(distinct_a)

	distinct_pairs = 0
	for i in range(n):
		na = freq_map[distinct_a[i]]
		nb = freq_map.get(distinct_a[i]+k, 0)
		if k == 0 and na > 1:
			distinct_pairs += 1
			print [distinct_a[i],distinct_a[i]+k],
		elif k>0 and nb > 0:
			distinct_pairs += 1
			print [distinct_a[i],distinct_a[i]+k],
	return distinct_pairs


a = [3,3,3,5,7,9,5,1,2,4,4,5,6]
k = 2
print findPairs(a,k)
a = [1,1,1,2]
k = 0
print findPairs(a,k)
