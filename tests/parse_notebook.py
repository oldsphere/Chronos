'''
    File to check how to parse TimeNotebook files
'''
import pandas as pd

NOTEBOOK = 'myNotebook-bak'

col_names = ['ID','category','task','init','end','type']
df = pd.read_csv(NOTEBOOK,sep=';',names=col_names)

#list tasks and subtasks:
catalog = {}
for cat in df.category.unique():
    if cat:
        print(cat)
        subtasks = df[df.category == cat].task
        print('\t','\n\t'.join( subtasks.values ) )
    print('\n')


    


