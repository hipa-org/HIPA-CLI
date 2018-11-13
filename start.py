class plotValue:
    def __init__(self, id, number):
        self.id = id
        self.number = number




time_traces = open("sampleData/time_traces.txt", "r").read()
plot_values = open("sampleData/plot_values.txt", "r").read().splitlines()
plotValueArray = []
splitArray = []





for i in plot_values:
    splitArray.append((i.split('\t', 1)))


for i in splitArray:
    plotValueArray.append(plotValue(i[0], i[1]))



print(time_traces)





#print([i.split('\t', 1)[0] for i in plot_values])
