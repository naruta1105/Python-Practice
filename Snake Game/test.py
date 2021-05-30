# Import Libraries
import pandas as pd
from os import path

x = [0,1,2,3,4,7]
y = ['a','b','c','d','e','f']
z = [0,1,2,3,4,7]
file_name = 'CSVFileName.csv'
'''
# df = pd.DataFrame({'Time':x, 'Value':y})
df = pd.DataFrame([[7,'f']], columns = ['Time', 'Value'])
with open('CSVFileName.csv', 'a+', newline='') as f:
    df.to_csv(f, index=False, encoding='utf-8', mode='a',header=False)
    f.close()

'''
def save_data(list_direction, list_food, score):
    df = pd.DataFrame([[list_direction,list_food,score]], columns = ['Direction', 'Food Position', 'Score'])
    if not path.exists(file_name) :
        with open(file_name,'w', newline='') as f:
            df.to_csv(f, index=False, encoding='utf-8',header=True)
            f.close()
    else:
        with open(file_name, 'a+', newline='') as f:
            df.to_csv(f, index=False, encoding='utf-8', mode='a',header=False)
            f.close()

with open(file_name,'r') as f:
    df = pd.read_csv(f, usecols= ['Time'])
    lst = df.values.tolist()
    #print(type(max(lst)[0]))
    f.close()