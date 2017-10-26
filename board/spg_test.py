CONNECTIONS = [[1, 10],  [0, 2, 6],    [1, 3],   [2, 4, 8],    [3, 13],   # nod$
               [6, 11],  [1, 5, 7],    [6, 8],   [3, 7, 9],    [8, 12],   # nod$
               [0, 11, 14, 32],    [5, 10, 15],  [9, 13, 16],  [4, 12, 17, 34],
               [10, 18],       [11, 19],     [12, 20],     [13, 21],      # nod$
               [14, 19, 27, 33],   [15, 18, 22], [16, 21, 26], [17, 20, 31, 35],
               [19, 23], [22, 24, 28], [23, 25], [24, 26, 30], [20, 25],  # nod$
               [18, 28], [23, 27, 29], [28, 30], [25, 29, 31], [21, 30],  # nod$
               [10], [18], [13], [21]  # nodes in base, 32-35
               ] 

for i, p in enumerate(CONNECTIONS):
	for j in p:
		if i not in CONNECTIONS[j]:
			print("Error on i=%i, j=%i" % (i,j))
print("Done")
