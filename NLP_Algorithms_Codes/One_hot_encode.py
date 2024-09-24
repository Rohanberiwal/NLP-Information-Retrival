import pandas as pd

data = {'Color': ['Red', 'Green', 'Blue', 'Red']}
df = pd.DataFrame(data)
df_encoded = pd.get_dummies(df, columns=['Color'])

print(df_encoded)
