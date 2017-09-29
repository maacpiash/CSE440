import sys

inputf = sys.argv[1]

with open(inputf, 'r') as f:
    lines = f.readlines()

# print(len(lines))

routes = []

for r in lines:
    if(r == str("END OF INPUT")):
        break
    else:
        routes.append(r)
    

# print(len(routes))

# for p in routes:
#     print(p)