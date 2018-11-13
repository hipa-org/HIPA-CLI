class myObject:
    def __init__(self, id, number):
        self.id = id
        self.number = number


time_traces = open("sampleData/time_traces.txt", "r").read().splitlines()
plot_values = open("sampleData/plot_values.txt", "r").read().splitlines()
objectArray = []
splitArray = []





for i in plot_values:
    splitArray.append((i.split('\t', 1)))


for i in splitArray:
    objectArray.append(myObject(i[0], i[1]))



for object in objectArray:
    print(object.id)



#print([i.split('\t', 1)[0] for i in plot_values])
