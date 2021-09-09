import pandas as pd

q1 = [10,20,30]
i1 = [1,2,3]

q2 = [1,2,3]
i2 = [2,3,4]

df1 = pd.DataFrame(q1, i1)
df2 = pd.DataFrame(q2, i2)

# print(pd.concat([df1, df2]))
print(df1.add(df2, fill_value=0))