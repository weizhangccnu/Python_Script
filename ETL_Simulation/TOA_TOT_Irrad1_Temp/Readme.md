### 1. How draw bar graph and list convert to tuple
```
def sigma_column(data):
    n_groups = 3;
    Irrad1 = tuple(data[0])
    Irrad2 = tuple(data[1])
    Irrad3 = tuple(data[2])

    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.25

    opacity = 0.8
    rects1 = plt.bar(index, Irrad1, bar_width,alpha=opacity, color='b',label='Irrad=1')
    rects2 = plt.bar(index + bar_width, Irrad2, bar_width,alpha=opacity,color='r',label='Irrad=2')
    rects2 = plt.bar(index + 2*bar_width, Irrad3, bar_width,alpha=opacity,color='g',label='Irrad=3')

    plt.xlabel('Temperature', family="Times New Roman", fontsize=8)
    plt.ylabel('TOA Corrected sigma [ps]', family="Times New Roman", fontsize=8)
    plt.title('TOA Corrected sigma distribution', family="Times New Roman", fontsize=12)
    plt.xticks(index + bar_width, ('30$^{\circ}$C', '-20$^{\circ}$C', '-30$^{\circ}$C'))
    plt.ylim(0,65);
    plt.legend(fontsize=8, edgecolor='green')
    plt.xticks(family="Times New Roman", fontsize=8)
    plt.yticks(family="Times New Roman", fontsize=8)
    plt.grid(linestyle='-.', linewidth=lw_grid)
    plt.tight_layout();
    plt.savefig("Time_Walk.png", dpi=fig_dpi)
    plt.clf()
```
### 2. No more
