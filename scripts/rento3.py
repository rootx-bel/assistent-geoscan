import os
for i in os.listdir('1'):
    os.rename('1/'+i, '1/0'+i)