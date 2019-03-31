from collections import defaultdict

import os
import json
import numpy as np
from tqdm import tqdm
from scipy.stats import linregress
from matplotlib import pyplot as plt

from data_cleaner import CleanData

# plt.rcParams['figure.figsize'] = (50, 25)


def heatmap(na_data, f_vline_pos, ylab, xlab, s_fname, yticks=None):
    """
    Makes a heatmap
    Then saves it in "plots" folder

    :param na_data: rectangular ndarray matrix
    :param f_vline_pos: line separating 2 things being compared
    :param ylab: str label on y-axis
    :param xlab: str label on x-axis
    :param s_fname: str name of file
    :param yticks: ticks on y-axis
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
            text = ax.text(j, i, int(na_data[i, j]) if not np.isnan(na_data[i, j]) else '',
                           ha="center", va="center", color="w")

    if yticks is not None:
        plt.yticks(*yticks)

    plt.savefig(f'plots/{s_fname}.png', dpi=160, bbox_inches='tight')

    return fig


class Questions:
    """
    This class has methods which answer questions
    about the data. It uses CleanData class
    from data_cleaner.py.
    """

    def __init__(self, d_data):

        self.CD = CleanData(d_data)

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

        ytick_ticks = []
        ytick_labels = []
        for i_student in sorted(set(range(min(self.CD.l_students), max(self.CD.l_students) + 1)) - {33, 40},
                                key=lambda id_: self.CD.get_student_grade_out_of_45(id_)):
            # HL and SL marks for student
            l_hl_subs = []
            l_sl_subs = []

            if i_student in self.CD.l_students:
                ytick_labels.append(i_student)
                ytick_ticks.append(len(l_hls))

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

        # using the function defined above
        heatmap(na_sl_vs_hls, 3.5, ylab='Student ID number', xlab=' SL               HL', s_fname='q1_1',
                yticks=(ytick_ticks, ytick_labels))

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

        ytick_ticks = []
        ytick_labels = []
        for i_student in range(min(self.CD.l_students), max(self.CD.l_students) + 1):
            # HL and SL marks for student
            l_hl_subs = []
            l_sl_subs = []

            if i_student in self.CD.l_students:
                ytick_labels.append(i_student)
                ytick_ticks.append(len(l_hls))

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

        # using the function defined above
        heatmap(na_sl_vs_hls, 3.5, ylab='Student ID number', xlab=' SL               HL', s_fname='q1_2',
                yticks=(ytick_ticks, ytick_labels))

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

    def q2(self):
        """
        Are there trends in terms of taking more languages at HL vs. taking more
        math or science classes at HL?

        :return: makes a heatmap
        """
        pass

    def q3(self):
        """
        Even though we don't have "filières" as they always have in the French
        Baccalaureate (S, L, ES...) are there trends in our students' subject
        choices that, in fact, show such a classification in IB students?

        :return:
        """
        pass

    def q4(self):
        """
        Do students who score well on their TOK also score well in other
        essay-based subjects such as languages or history (and vice-versa, do
        science and math students score more poorly on TOK in general?)

        :return:
        """

        pass

    def q5(self, s_subject, b_hl, s_component1, s_component2):
        """
        Are there certain component results that don't fit the rest of the data?
        For example, do French B orals seem low compared to the other components
        such as the written task or the exam papers?

        COMPONENTS only from one subject

        USES INPUTS!

        This does not separate SL from HLs
        :return: graph
        """

        # # find the list of subjects for input
        # s_subs = "\n".join(map(str, self.CD.get_subjects_taken()))
        # s_subject = input(f"\nPlease choose between the following subjects\n(and type in exactly as shown):\n{s_subs}\n")
        #
        # s_yn = input("\nWould you like to look at HL components (comparing only HL students)? y/n\n")
        # b_hl = True if s_yn.lower() == "y" else False
        #
        # # find the list of components for input
        # s_comps = "\n".join(map(str, self.CD.get_subject_components(s_subject, b_hl)))
        # s_component1 = input(f"\nPlease choose between the following components\n(and type in exactly as shown):\n{s_comps}\n")
        # s_component2 = input(f"\nPlease choose another component between the following components\n(and type in exactly as shown):\n{s_comps}\n")

        l_substudents = self.CD.get_students_doing(s_subject)
        # if looking at only HL students
        if b_hl:
            l_substudents = [i for i in l_substudents if self.CD.d_students[i][s_subject]["level"] == "HL"]

        l_comp1 = []
        l_comp2 = []

        for student in l_substudents:
            l_comp1 += [self.CD.d_students[student][s_subject][s_component1]["mark"]]
            l_comp2 += [self.CD.d_students[student][s_subject][s_component2]["mark"]]


        slope, intercept, r_value, _, stderr = linregress(l_comp1, l_comp2)

        return l_comp1, l_comp2, slope, intercept, r_value**2


        # plt.figure()
        # plt.plot(l_comp1, l_comp2, ".")
        #
        xmin, xmax = plt.xlim()
        xs = np.linspace(0, xmax)
        ys = slope * xs + intercept
        # plt.plot(xs, ys, "C0-", label=f"{round(slope, 1)}x + {round(intercept, 2)}, R$^2$={r_value**2:.3f}")
        # plt.xlim(0, xmax)
        # plt.legend()
        #
        # plt.xlabel(f"{s_component1}")
        # plt.ylabel(f"{s_component2}")
        # plt.title(f"{s_subject}")
        # plt.show()

    def q6(self):
        """
        Do students who do well on their EE also do equally as well in that subject?
        Are there certain subjects where the EE results don't match the results
        for the rest of the class?

        :return:
        """
        # TODO: add comparaison to the rest of the grades (to see if it stands out)

        l_compare = defaultdict(list)

        for i_student in self.CD.l_students:
            ee_info = self.CD.d_students[i_student]["EE"]
            subject_results = self.CD.d_students[i_student].get(ee_info["subject"])
            if subject_results is not None:  # World Studies
                l_compare[ee_info["subject"]].append(
                    (ee_info["total_mark"], subject_results["total_mark"])
                )

        return l_compare


if __name__ == '__main__':
    # path to files
    s_path = os.path.dirname(__name__)
    s_path_data = os.path.join(s_path, "data")

    s_cached_data_fname = os.path.join(s_path_data, 'cached_data.json')

    with open(s_cached_data_fname) as f:
        Q_ib2018 = Questions(json.load(f))

    Q_ib2018.q1_1()
    Q_ib2018.q1_2()
    Q_ib2018.q5()
