f = open('input')
x = [int(s) for s in f.readlines()]
m = {0: True}
cur = 0
found = False
while not found:
  for a in x:
    cur += a
    if cur in m:
      print(cur)
      found = True
      break
    m[cur] = True
