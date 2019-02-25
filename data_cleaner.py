# python3

import os
import numpy as np
import pandas as pd


class CleanData(object):
    """
    This class is initiated by a set of data
    as a pandas dataframe, and cleans it into
    the following dictionary (called d_students).

    (words marked with * * mean there is another
    name there instead)

    {
    *studentID1*:
        {
        school: 'schoolID',

        *subject1*: {
            level: 'SL' or 'HL',
            grade: integer out of 7,
            total_mark: integer out of 100,
            language: 'ENGLISH', 'FRENCH', etc,
            *component1*: {
                grade: integer out of 7,
                mark: integer marks
                },
            *component2* { ... }
            },

        *subject2*: {
            ...
        },

        EE: {
            subject: str name of subject,
            letter_grade: 'A', 'B', 'C', ...,
            total_mark: integer out of 34,
            language: 'ENGLISH', etc,
            },

        TOK: {
            letter_grade: 'A', 'B', 'C', ...,
            total_mark: integer out of 30,
            language: 'ENGLISH', etc,
            essay: {
                mark: mark out of 10, times 2,
                letter_grade: 'A', 'B', ...
                },
            presentation: {
                mark: mark out of 10,
                letter_grade: 'A', 'B', ...
                }
            },

        core_pt: 0, 1, 2, or 3
        },

    *studentID2*: { ... }

    ...

    }

    *studentID* is an integer ID number
    *subject* is the name of the subject,
        for example 'BIOLOGY'
    *component* is the name of the component,
        for example 'PAPER ONE'


    """

    def __init__(self, df_data):
        self.df_data = df_data

        # Organises the data into dicts
        # of dicts

        self.d_students = {}

        for idx, row in self.df_data.iterrows():
            id = row['Registration number']
            if id not in self.d_students:
                self.d_students[id] = {}

        # stores the conversion from EE
        # and TOK grades into the 3
        # additional core points

        # TODO find better way to do this
        self.d_core_points = {
            "AA": 3,
            "AB": 3,
            "AC": 2,
            "AD": 2,
            "AE": 0,  # not sure
            "BB": 2,
            "BC": 1,
            "BD": 1,
            "BE": 0,  # not sure
            "CC": 1,
            "CD": 0,
            "CE": 0,  # not sure
            "DD": 0,
            "DE": 0,  # not sure
            "EE": 0,  # not sure
        }

    #
    def get_students_doing(self, s_subject):
        """
        Gets the ID numbers of the students
        doing a particular subject
        :param s_subject: string subject name
        :return: list of student ID numbers
        """
        l_students_doing = []
        for i_student in self.d_students:
            if s_subject in self.d_students[i_student]:
                l_students_doing.append(i_student)
        return l_students_doing

    #

    def total_grade(self, i_student):
        """
        Gets the total grade (out of 45)
        of a particular student.
        Requires self.
        :param i_student: student ID num
        :return: integer grade of 45
        """
        pass
    #


#


if __name__ == '__main__':
    # path to files
    s_path = "/Users/ ... /GibData"
    s_path_data = os.path.join(s_path, "data")

    s_data_fname = os.path.join(s_path_data, 'c2018_v2.csv')
    df_data = pd.read_csv(s_data_fname)

    d_ib2018 = CleanData(df_data)