import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame({'Day': ['Mon', 'Tue', 'Wed', 'Thur', 'Fri'],
                   'Morning': [44, 46, 49, 59, 54],
                   'Night': [53, 66, 70, 69, 80],
                   'Evening': [33, 46, 50, 49, 60],
                   'Sunday': [13, 26, 30, 29, 40],
                   })
print(df)
# sns.set(style='white')

df.set_index('Day').plot(kind='barh', stacked=True)
plt.show()
