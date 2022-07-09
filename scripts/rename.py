import os
count = 1
for file_name in os.listdir("pic/"):
    os.rename("pic/"+file_name, "pic/"+ "8" +str(count)+file_name)