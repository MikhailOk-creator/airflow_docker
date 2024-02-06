# Нахождение цикла в графе
def dfs1(v):
    colors[v] = 1
    for u in g[v]:
        if colors[u] == 0:
            if dfs1(u): return True
        elif colors[u] == 1:
            return True
    colors[v] = 2
    return False



def dfs2(v):
    visited[v] = True
    for u in g[v]:
        if not visited[u]:
            dfs2(u)
    tout.append(v)


n,m = [int(i) for i in input().split()]
g = [[] for i in range(n)]
colors = [0 for i in range(n)]
visited=[False for i in range(n)]
tout = [ ]
for i in range(m):
    a,b = [int(i)-1 for i in input().split()]
    g[a].append(b)


result = False
for i in range(n):
    if dfs1(i):
        result = True
        break
print(result)
for i in range(n):
    if not visited[i]:
        dfs2(i)
for vertex in tout[::-1]:
    print(vertex+1)

'''
Exaple:
5 6
1 2
1 4
4 3
2 3
4 5
3 5
'''
