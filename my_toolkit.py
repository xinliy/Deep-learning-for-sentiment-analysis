import numpy as np



def negative_precision(y_true,y_pred):
    y_pred = np.round(y_pred)
    count_neg = 0
    total_neg = 0
    total_pos=0
    count_pos=0
    for yt, yp in zip(y_true, y_pred):
        if int(yt) == 0:
            count_neg = count_neg + 1
            if int(yp[0]) == 1:
                total_neg = total_neg + 1

        if int(yt)==1:
            count_pos=count_pos+1
            if int(yp[0])==0:
                total_pos=total_pos+1

    # print("The precision for negative label is: ", total / count)
    return {'Precision':1-(total_pos+total_neg)/(count_pos+count_neg),
            'PP':1-total_pos/count_pos,
            'NP':1-total_neg/count_neg}