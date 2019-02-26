

import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from data_cleaner import CleanData


def heatmap(na_data, f_vline_pos, ylab, xlab):
    """
    Makes a heatmap

    :param na_data: rectangular ndarray matrix
    :param f_vline_pos: line separating 2 things being compared
    :param ylab: label on y-axis
    :param xlab: label on x-axis
    """

    fig, ax = plt.subplots()
    im = ax.imshow(na_data)

    # might want to change ymin TODO
    ymax = na_data.shape[0]
    plt.vlines(f_vline_pos, ymin=-1, ymax=ymax, colors='r')

    plt.ylabel(ylab)
    plt.xlabel(xlab)

    plt.tick_params(
        axis='x',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom=False,  # ticks along the bottom edge are off
        top=False,  # ticks along the top edge are off
        labelbottom=False)

    # Loop over data dimensions and create text annotations.
    for i in range(na_data.shape[0]):
        for j in range(na_data.shape[1]):
            text = ax.text(j, i, na_data[i, j],
                           ha="center", va="center", color="w")

    plt.show()
#


class Questions:
    """
    This class has methods which answer questions
    about the data. It uses CleanData class
    from data_cleaner.py.
    """
    def __init__(self, df_data):

        self.CD = CleanData(df_data)
    #

    def q1_1(self):
        """
        Do students generally do better in their HL classes compared to their SL classes?

        q1_1 compares the total_marks of the subjects
        q1_2 compares the grade out of 7 of the subjects
        q1_3 compares for every student the total_marks across SLs and HLs

        MUST ZOOM IN to look at the heatmap (numbers appear once zoomed in)
        :return: makes a heatmap
        """

        l_hls = []
        l_sls = []

        for i_student in self.CD.l_students:
            # HL and SL marks for student
            l_hl_subs = []
            l_sl_subs = []
            for s_subject in self.CD.d_students[i_student]:
                if s_subject in ('school', 'EE', 'TOK', 'core_pt'):
                    # for now we only want the actual subjects
                    continue

                # append the total marks gained in that subject
                if self.CD.d_students[i_student][s_subject]['level'] == 'HL':
                    l_hl_subs.append(self.CD.d_students[i_student][s_subject]['total_mark'])
                if self.CD.d_students[i_student][s_subject]['level'] == 'SL':
                    l_sl_subs.append(self.CD.d_students[i_student][s_subject]['total_mark'])

            # make the l_hls and l_sls into rectangular matrices
            # make it pretty and symmetrical
            while len(l_hl_subs) < 4:
                l_hl_subs.append(np.nan)
            while len(l_sl_subs) < 4:
                l_sl_subs.insert(0, np.nan)

            l_hls.append(l_hl_subs)
            l_sls.append(l_sl_subs)

        na_sl_vs_hls = np.column_stack((np.array(l_sls), np.array(l_hls)))

        heatmap(na_sl_vs_hls, 3.5, ylab='Student ID number', xlab=' SL  HL')
    #

    def q1_2(self):
        """
        Do students generally do better in their HL classes compared to their SL classes?

        q1_1 compares the total_marks of the subjects
        q1_2 compares the grade out of 7 of the subjects
        q1_3 compares for every student the total_marks across SLs and HLs

        MUST ZOOM IN to look at the heatmap (numbers appear once zoomed in)
        :return: makes a heatmap
        """

        l_hls = []
        l_sls = []

        for i_student in self.CD.l_students:
            # HL and SL marks for student
            l_hl_subs = []
            l_sl_subs = []
            for s_subject in self.CD.d_students[i_student]:
                if s_subject in ('school', 'EE', 'TOK', 'core_pt'):
                    # for now we only want the actual subjects
                    continue

                # append the total marks gained in that subject
                if self.CD.d_students[i_student][s_subject]['level'] == 'HL':
                    l_hl_subs.append(self.CD.d_students[i_student][s_subject]['grade'])
                if self.CD.d_students[i_student][s_subject]['level'] == 'SL':
                    l_sl_subs.append(self.CD.d_students[i_student][s_subject]['grade'])

            # make the l_hls and l_sls into rectangular matrices
            # make it pretty and symmetrical
            while len(l_hl_subs) < 4:
                l_hl_subs.append(np.nan)
            while len(l_sl_subs) < 4:
                l_sl_subs.insert(0, np.nan)

            l_hls.append(l_hl_subs)
            l_sls.append(l_sl_subs)

        na_sl_vs_hls = np.column_stack((np.array(l_sls), np.array(l_hls)))

        heatmap(na_sl_vs_hls, 3.5, ylab='Student ID number', xlab=' SL  HL')
    #

    def q1_3(self):
        """
        Do students generally do better in their HL classes compared to their SL classes?

        q1_1 compares the total_marks of the subjects
        q1_2 compares the grade out of 7 of the subjects
        q1_3 compares for every student the total_marks across SLs and HLs

        MUST ZOOM IN to look at the heatmap (numbers appear once zoomed in)
        :return: makes a heatmap
        """
        pass
    #

    def q2(self):
        """
        Are there trends in terms of taking more languages at HL vs. taking more
        math or science classes at HL?

        :return: makes a heatmap
        """
        pass
    #

    def q3(self):
        """
        Even though we don't have "filières" as they always have in the French
        Baccalaureate (S, L, ES...) are there trends in our students' subject
        choices that, in fact, show such a classification in IB students?

        :return:
        """
        pass
    #

    def q4(self):
        """
        Do students who score well on their TOK also score well in other
        essay-based subjects such as languages or history (and vice-versa, do
        science and math students score more poorly on TOK in general?)

        :return:
        """
        pass
    #

    def q5(self):
        """
        Are there certain component results that don't fit the rest of the data?
        For example, do French B orals seem low compared to the other components
        such as the written task or the exam papers?

        :return:
        """
        pass
    #

    def q6(self):
        """
        Do students who do well on their EE also do equally as well in that subject?
        Are there certain subjects where the EE results don't match the results
        for the rest of the class?

        :return:
        """
        pass
#


if __name__ == '__main__':

    # path to files
    # TODO change
    s_path = "/Users/ ... path ... /GibData"
    s_path_data = os.path.join(s_path, "data")

    s_data_fname = os.path.join(s_path_data, 'c2018_v2.csv')

    df_data = pd.read_csv(s_data_fname)

    Q_ib2018 = Questions(df_data)

    Q_ib2018.q1_1()

#