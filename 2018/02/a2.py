x = list(open('input').readlines())
for i in range(len(x[0])):
  m = {}
  for y in x:
    z = y[:i] + y[i + 1:]
    if z in m:
      print(''.join(sorted(z[:-1])))
      break
    m[z] = y
