import requests
from test_main import bigfunc
from PIL import Image
import pandas as pd
from PIL import Image
clearframedict = {'g1':9999,'g2':0,'g3':0,'g4':0,'g5':0,'g6':0,'g7':0,'g8':0,'g9':0,'g10':0,'g11':0,'g12':0,'g13':0,'g14':0,'g15':0,'g16':0,
    'h1': 0, 'h2': 0, 'h3': 0, 'h4': 0, 'h5': 0, 'h6': 0, 'h7': 0, 'h8': 0,
    'ei1': 0, 'ei2': 0, 'ei3': 0, 'ei4': 0, 'ei5': 0, 'ei6': 0, 'ei7': 0, 'ei8': 0, 'ei9': 0, 'ei10': 0,'ei11': 0, 'ei12': 0, 'ei13': 0, 'ei14': 0, 'ei15': 0, 'ei16': 0,
    'eo1': 0, 'eo2': 0, 'eo3': 0, 'eo4': 0, 'eo5': 0, 'eo6': 0, 'eo7': 0, 'eo8': 0, 'eo9': 0, 'eo10': 0,'eo11': 0, 'eo12': 0, 'eo13': 0, 'eo14': 0, 'eo15': 0, 'eo16': 0,

    'wi1':0,'wi2':0,'wi3':0,'wi4':0,'wi5':0,'wi6':0,'wi7':0,'wi8':0,'wi9':0,'wi10':0,'wi11':0,'wi12':0,'wi13':0,'wi14':0,'wi15':0,'wi16':0,
    'wo1': 0, 'wo2': 0, 'wo3': 0, 'wo4': 0, 'wo5': 0, 'wo6': 0, 'wo7': 0, 'wo8': 0, 'wo9': 0, 'wo10': 0, 'wo11': 0,'wo12': 0, 'wo13': 0, 'wo14': 0, 'wo15': 0, 'wo16': 0,
    'i1':0,'i2':0,'i3':0,'i4':0,'i5':0,'i6':0,'i7':0,'i8':0,'i9':0,'i10':0,'i11':0,'i12':0,'i13':0,'i14':0,'i15':0,'i16':0,
    'bl':0,'br':0,
    'c':0}
clear = pd.DataFrame([clearframedict])
def exists(path):
    r = requests.head(path)
    return r.status_code == requests.codes.ok
def stream(match_id,szn):
    main_frame = pd.DataFrame()
    for i in range(1,7,1):
        for j in range(1,17):
            url = 'https://world-curling-federation.s3-eu-west-1.amazonaws.com/shot-images/CUR_'+str(szn)+'_WMCC/'+str(match_id) + '/shot-image-E' + str(i)+ 'S' + str(j) +'.jpg'
            data = requests.get(url).content
            f = open('img.jpg', 'wb')
            f.write(data)
            f.close()
            #print('END: ' + str(i) + ' SHOT: ' + str(j))
            if (i % 2 == 1):
                val =True
            else:
                val = False
            shot_dict = bigfunc('img.jpg', val)
            hold = pd.DataFrame([shot_dict])
            hold['refid'] = 'E' + str(i) + 'S'+ str(j)
            #print(hold)
            main_frame = pd.concat([main_frame,hold],ignore_index=True)
            #main_frame._append(shot_dict, ignore_index=True)
            #img = Image.open('img.jpg')
            #img.show()
            #print(main_frame)
    main_frame = pd.concat([main_frame, clear], ignore_index=True)
    #print(main_frame)
    return main_frame

def gather_data(games, szn):
    # nums is a list of match ids
    string = r'C:\Users\alexr\PycharmProjects\NextShotCurling\outputupd.xlsx'
    big_frame = pd.read_excel(string)
    #big_frame = pd.DataFrame()
    print('loaded')
    for game in games:
        urlt = 'https://world-curling-federation.s3-eu-west-1.amazonaws.com/shot-images/CUR_'+str(szn)+'_WMCC/' + str(game) + '/shot-image-E1S1.jpg'
        if exists(urlt) == False:
            print('********')
            print('********')
            print('MATCH ' + str(game) + ' DNE')
            print('********')
            print('********')
            continue
        else:
            #print(exists(urlt))
            print('NEW MATCH ' +str(game))
            match_frame = stream(game,szn)
            print('CONCAT')
            big_frame = pd.concat([big_frame,match_frame], ignore_index=True)
    #print(big_frame)
    big_frame.to_excel("outputupd.xlsx", index=False)

#merpy = [7538,7539,7541,7542,7543,7544,7546,7547,7548,7549, 7551, 7552,7553,7554, 7556, 7557, 7558]
wow = [7592,7594,7595,7596,7597,7599,7600,7601,7602,7604,7605,7606,7607,7609,7610,7611,7612,7614,7615,7616,7617,7619,7620]

# get odd numbered ends
dorp = [7538,7539,7541,7542,7543,7544,7546,7547,7548,7549, 7551, 7552,7553,7554, 7556, 7557, 7558,7560, 7561, 7562, 7563, 7565, 7566, 7567, 7568, 7570, 7571, 7572, 7575, 7576, 7577, 7579, 7580, 7581, 7582, 7584, 7585, 7586, 7587, 7589, 7590, 7591, 7592,7594,7595,7596,7597,7599,7600,7601,7602,7604,7605,7606,7607,7609,7610,7611,7612,7614,7615,7616,7617,7619,7620]

test = [7534,7535,7536]

#2123
#4903

new = [4903, 4904, 4905, 4906, 4907, 4908, 4909, 4910, 4911, 4912, 4913, 4914, 4915, 4916, 4917, 4918, 4919, 4920, 4921, 4922, 4923, 4924, 4925, 4926, 4927, 4928, 4929, 4930, 4931, 4932, 4933, 4934, 4935, 4936, 4937, 4938, 4939, 4940, 4941, 4942, 4943, 4944, 4945, 4946, 4947, 4948, 4949, 4950, 4951, 4952, 4953, 4954, 4955, 4956, 4957, 4958, 4959, 4960, 4961, 4962]



#5009