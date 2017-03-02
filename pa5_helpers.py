
def exp(a,k):

    new = ''
    a_len = len(a)
    count = 0
    index = 0
    h = []

    while count < a_len:
          
        if count == len(a)-k-1:
            a+=a[0:k]
            
        h.append((a[count:count+k],a[count+k]))
        count+=1
    return h

def hash_it(h,k):
    d = {}

    for i in h:
        #print(d)
        if i[:k] not in d:
            d[i[:k]] = {i[-1]:1}
        else:
            print('hi')
            if i[-1] in d[i[:k-1]]:
                d[i[:k-1]][i[-1]] = d[i[:k-1]].get(i[-1],0)+1
            else: 
                d[i[:k-1]] = {i[-1]:1}

            print(i[:k-1])