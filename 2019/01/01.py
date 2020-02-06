res = 0
while True:
  try:
    s = input()
  except:
    break
  a = int(s)
  res += a // 3 - 2
print(res)
