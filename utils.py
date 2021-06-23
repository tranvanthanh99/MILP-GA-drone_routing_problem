from matplotlib import markers
import matplotlib.pyplot as plt
import matplotlib as mpl
import math


data = [
    {
        "node": 0,
        "coordinate": (0, 0),
        "label": "D",
        "demand": 0
    },
    {
        "node": 1,
        "coordinate": (0, 15),
        "label": "P",
        "demand": 2
    },
    {
        "node": 2,
        "coordinate": (7, 20),
        "label": "P",
        "demand": 5
    },
    {
        "node": 3,
        "coordinate": (25, 20),
        "label": "P",
        "demand": 5
    },
    {
        "node": 4,
        "coordinate": (25, 39),
        "label": "P",
        "demand": 3
    },
    {
        "node": 5,
        "coordinate": (14, 41),
        "label": "P",
        "demand": 1
    },
    {
        "node": 6,
        "coordinate": (17, 9),
        "label": "P",
        "demand": 3
    },
    {
        "node": 7,
        "coordinate": (13, 21),
        "label": "P",
        "demand": 2
    },
    {
        "node": 8,
        "coordinate": (4, 27),
        "label": "P",
        "demand": 2
    },
    {
        "node": 9,
        "coordinate": (26, 0),
        "label": "P",
        "demand": 2
    },
]

tour = [0, 1, 2, 8, 0, 3, 4, 5, 7, 0, 6, 9, 0]


def print_solution(data, tour, title="", save = False):
    
    #draw arc
    fig, ax = plt.subplots()
    for i in range(len(tour) - 1):
        # x= (i['src']['lon'], i['src']['lat'])
        # y = (i['des']['lon'], i['des']['lat'])
        x= (data[tour[i]]['coordinate'][0], data[tour[i]]['coordinate'][1])
        y= (data[tour[i+1]]['coordinate'][0], data[tour[i+1]]['coordinate'][1])

        size = 1000
        radius = math.sqrt(size)/2.
        arrow = mpl.patches.FancyArrowPatch(posA=x, posB=y, 
                                            arrowstyle='-|>', mutation_scale=20, 
                                            shrinkA=radius, shrinkB=radius)
        ax.add_patch(arrow)

    # draw label
    for idx, node in enumerate(data):
        # print(idx, node)
        demand = node['demand']
        plt.plot(node['coordinate'][0], node['coordinate'][1], marker='o', mfc='1', mec='g', markersize = 30)
        plt.plot(node['coordinate'][0], node['coordinate'][1], marker=f'${idx}, {demand}$', markersize = 20)

    # draw title
    plt.title(title)
    if save == True:
        plt.savefig("out.png")
    
    plt.show()

if __name__ == "__main__":
    print_solution(data, tour)