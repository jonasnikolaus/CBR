
i = 0
while i < 1:
    case1 = arrayzerlegt1[i]  
    case2 = case1 - min
    case = case2 / maxmin

    nbrs = NearestNeighbors(n_neighbors=1, algorithm='auto').fit(arraynorm1)
    distances, indices = nbrs.kneighbors(case)

    sens[i] = distances

i += 1

neu 


print(sens[0])
print('-----------')

nbrs = NearestNeighbors(n_neighbors=1, algorithm='auto').fit(arraynorm1[[15]])
distances, indices = nbrs.kneighbors(case)
print(distances)

sens[466]= distances

print(float(sens[0]))
print(sens)
print(distances)

funkt:


 while i < 467:
        case= arraynorm1[[i]]
        nbrs = NearestNeighbors(n_neighbors=1, algorithm='auto').fit(arraynorm1[[j]])
        distances, indices = nbrs.kneighbors(case)
        sens[i]= distances
        i += 1


while i < 467:
        case= arraynorm1[[i]]
        nbrs = NearestNeighbors(n_neighbors=1, algorithm='auto').fit(arraynorm1[[j]])
        distances, indices = nbrs.kneighbors(case)
        sens[i]= distances
        i += 1