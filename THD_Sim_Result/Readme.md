### 1. How to plot multiple line in a figure
```python 

    for i in xrange(len(Data)-5):
        plt.plot(x, Data[i], color=colorstyle[i], marker=markerstyle[i], markersize=2, linewidth=0.8, label='Frequency = %sMHz'%Freq[i])
```
### 2. Set x-axis minor ticks
