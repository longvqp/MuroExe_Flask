import os
import json



datadir = "/Users/longvu/Projects/Moroexe_Flask/app/static/data"
data = []
with os.scandir(datadir) as folders:
    for folder in folders:
        if(folder.name!='.DS_Store'):
            folderPath = (folder.path)
            print('-----')
            print("In Folder: "+folder.name)
            for file in os.scandir(folderPath):
                if( file.name!='.DS_Store' ):
                    #print(file)
                    if(file.name=='infor.JSON'):
                        with open(file, 'r') as fcc_file:
                            data.append(json.load(fcc_file)) 
                    else:
                        print(file.name)
                        # file.save(os.path.join('app/static/assets/Product_Image', file.name))
                   

