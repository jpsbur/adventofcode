f = open('input')
c2 = 0
c3 = 0
for s in f.readlines():
  m = {}
  for x in s:
    if x not in m:
      m[x] = 0
    m[x] += 1
  x2 = False
  x3 = False
  for v in m:
    if m[v] == 2:
      x2 = True
    if m[v] == 3:
      x3 = True
  if x2:
    c2 += 1
  if x3:
    c3 += 1
print(c2 * c3)
