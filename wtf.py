#!/usr/bin/env python3



lines = ['a','b','c']
with open('./wtf.txt', 'w') as f:
  f.writelines(lines)