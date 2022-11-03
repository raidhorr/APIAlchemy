from dbclass import PerevalAdded

with open('data.txt') as test:
    data = test.read()


pereval = PerevalAdded()
res = pereval.submitData(data)
print(res)
