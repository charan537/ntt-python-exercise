d=[("user1","ph1","em1"),("user2","ph1","em2"),
   ("user3","ph3","em3"),("user4","ph4","em2")]

d=[("user1","ph1","em1"),("user4","ph4","em2"),
   ("user3","ph3","em3"),("user2","ph1","em2")]

d=[("user1","ph1","em1"),("user4","ph4","em2"),
   ("user3","ph3","em3"),("user2","ph1","em2"),("user4","ph5","em4")]

ulist=list(map(lambda x : x[0],d))
plist=list(map(lambda x : x[1],d))
elist=list(map(lambda x : x[2],d))

def findAllIdx(val_list,srch_val):
    idx_list=[]
    for idx, val in enumerate(val_list):
        if val == srch_val:
            idx_list.append(idx)
    return idx_list

res=[]
dict_u={}
dict_p={}
dict_e={}
for key in set(ulist):
    dict_u[key]=findAllIdx(ulist,key)
for key in set(plist):
    dict_p[key]=findAllIdx(plist,key)
for key in set(elist):
    dict_e[key]=findAllIdx(elist,key)
for i in range(0,len(d)):
    u,p,e=d[i]
    cur_res=[]
    cur_res.extend(dict_u[u])
    cur_res.extend(dict_p[p])
    cur_res.extend(dict_e[e])
    res.append(list(set(cur_res)))

print("Neighbors:")
for idx, neighbors in enumerate(res):
    print(idx,":",neighbors)

# Build a graph based on the connections obtained
N = len(d)
edges = [[False]*N for i in range(N)]
for idx, neighbors in enumerate(res):
    for nidx in neighbors:
        edges[idx][nidx] = True
print("Edges:")
for idx, val in enumerate(edges):
    print(idx,":",val)

# Now the problem translates to finding the connected components in the
# undirected graph
def visit(i, edges, visited, curr_set):
    curr_set.append(i)
    visited[i] = True
    for j in range(len(edges[i])):
        if edges[i][j] and not visited[j]:
            visit(j, edges, visited, curr_set)
    visited[i] = 1

visited = [False]*N
ans = []
for i in range(N):
    if not visited[i]:
        curr_set = []
        visit(i, edges, visited, curr_set)
        ans.append(curr_set)

print("Ans:")
print(ans)
