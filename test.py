import json
import pandas as pd
a = pd.read_csv('hack.csv')
col = a.columns
map = {

}
# for ind,item in enumerate(a.loc[0,:]):
#     map[str(col[ind])] = str(item)
# b = json.dumps(map)
# print(b)


x=input()
for item in a.loc[:,x]:
    print(str(item))
