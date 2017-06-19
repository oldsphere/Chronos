#!/bin/python3

from Chronos.TimeNotebook import TimeNotebook
from auxiliar import set_title , date_parser

ntPath = "/home/sphere/.myNotebook" 
nt = TimeNotebook(ntPath)
nt.readFile()

init,end = date_parser('1W')
resume = nt.get_tasks(init,end)
print(resume)
