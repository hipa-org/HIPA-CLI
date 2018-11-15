import matplotlib.pyplot as plt


def test_plotting(ones_per_minutes):
    minute = 0
    y_axis_data = []
    set_length = len(ones_per_minutes[0])
    for x in range(set_length):
        y_axis_data.append(minute)
        minute += 1

    print(ones_per_minutes[0])
    print(len(ones_per_minutes[0]))
    print(len(y_axis_data))
    print(y_axis_data)
    # print(y_axis_data)
    # print(x_axis_data)
    # plt.plot(x_axis_data, y_axis_data)
    plt.ylabel('Ones')
    plt.xlabel('Time in Minutes')
# plt.show()
