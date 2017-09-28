import sys

inputf = sys.argv[1]

with open(inputf, 'r') as f:
    lines = f.readlines()

routes = []
count = 0

while str(lines[count]) != str("END OF INPUT"):
    routes.append(lines[count])
    print(routes[count])
    count = count + 1

print(len(routes))
for p in routes:
    print(p)