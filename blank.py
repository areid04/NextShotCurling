import requests
from test_main import bigfunc
from PIL import Image
import pandas as pd

def stream(match_id):
    main_frame = pd.DataFrame()
    for i in range(2,8,2):
        for j in range(1,17):
            url = 'https://world-curling-federation.s3-eu-west-1.amazonaws.com/shot-images/CUR_2223_WMCC/'+str(match_id) + '/shot-image-E' + str(i)+ 'S' + str(j) +'.jpg'
            data = requests.get(url).content
            f = open('img.jpg', 'wb')
            f.write(data)
            #print(f)
            f.close()
            #print(f)
            print('END: ' + str(i) + ' SHOT: ' + str(j))
            shot_dict = bigfunc('img.jpg')
            hold = pd.DataFrame([shot_dict])
            hold['refid'] = 'E' + str(i) + 'S'+ str(j)
            #print(hold)
            main_frame = pd.concat([main_frame,hold],ignore_index=True)
            #main_frame._append(shot_dict, ignore_index=True)
            #img = Image.open('img.jpg')
            #img.show()
            #print(main_frame)
    print(main_frame)
    return main_frame

def gather_data(games):
    # nums is a list of match ids
    string = r'C:\Users\alexr\PycharmProjects\NextShotCurling\output.xlsx'
    big_frame = pd.read_excel(string)
    print('test')
    for game in games:
        print('NEW MATCH ' +str(game))
        match_frame = stream(game)
        print('CONCAT')
        big_frame = pd.concat([big_frame,match_frame], ignore_index=True)
    print(big_frame)
    big_frame.to_excel("output.xlsx", index=False)

#merpy = [7538,7539,7541,7542,7543,7544,7546,7547,7548,7549, 7551, 7552,7553,7554, 7556, 7557, 7558]
