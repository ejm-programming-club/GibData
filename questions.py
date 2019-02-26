#python3

import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


if __name__ == '__main__':

    from data_cleaner import CleanData

    # path to files
    # TODO change
    s_path = "/Users/ ... path ... /GibData"
    s_path_data = os.path.join(s_path, "data")

    s_data_fname = os.path.join(s_path_data, 'c2018_v2.csv')

    df_data = pd.read_csv(s_data_fname)

    CD_ib2018 = CleanData(df_data)


    #####
    # Q1
    # Do students generally do better in their HL classes compared to their SL classes?

    hls = []
    sls = []

    for student in CD_ib2018.l_students:
        #print()
        #print(student)
        hl_subs = []
        sl_subs = []
        for subject in CD_ib2018.d_students[student]:
            if subject in ('school', 'EE', 'TOK', 'core_pt'):
                continue

            #print(subject)
            if CD_ib2018.d_students[student][subject]['level'] == 'HL':
                hl_subs.append(CD_ib2018.d_students[student][subject]['total_mark'])
            if CD_ib2018.d_students[student][subject]['level'] == 'SL':
                sl_subs.append(CD_ib2018.d_students[student][subject]['total_mark'])

        while len(hl_subs) < 4:
            hl_subs.append(np.nan)
        while len(sl_subs) < 4:
            sl_subs.insert(0, np.nan)

        hls.append(hl_subs)
        sls.append(sl_subs)

    sl_vs_hls = np.column_stack((np.array(sls), np.array(hls)))

    fig, ax = plt.subplots()
    im = ax.imshow(sl_vs_hls)

    plt.vlines(3.5, ymin=-1, ymax=61, colors='r')

    plt.ylabel('Student ID number')
    plt.xlabel(' SL  HL')

    plt.tick_params(
        axis='x',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom=False,  # ticks along the bottom edge are off
        top=False,  # ticks along the top edge are off
        labelbottom=False)

    plt.show()

    # No... in conclusion heatmap doesnt seem to show such a correlation


    #####
    # Q2
    # Are there trends in terms of taking more languages at HL vs. taking more math or science classes at HL?

    # ...