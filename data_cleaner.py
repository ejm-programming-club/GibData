import os
import json
import pandas as pd
from typing import *
from tqdm import tqdm


class Data:
    """
    This class uses the pandas has methods to
    extract information from the raw pandas
    dataframe.

    The class will be used by the class
    CleanData to organise this extracted data.
    """

    def __init__(self, df_data: pd.DataFrame):
        self.df_data = df_data

        self.l_students = []

        # TODO maybe later make self.d_students in this class as well

        # ERROR CHECKING
        # checking whether each column of the dataframe
        # exists as expected, and with the expected name.

        l_expected_headers = ['Subject', 'Level', 'Component',
                              'Language', 'School', 'Registration number',
                              'Component mark', 'Component grade',
                              'Scaled total mark for subject', 'Subject grade']

        if list(self.df_data) != l_expected_headers:
            raise ValueError('Data: Headers are not correct, they should be the following:\n%s'
                             % l_expected_headers)
        self.get_all_student_ids()

        self._d_rows: Dict[int, List] = {i_id: [] for i_id in self.l_students}
        for idx, row in self.df_data.iterrows():
            self._d_rows[row['Registration number']].append(row)

    def get_all_student_ids(self) -> List[int]:
        """
        Gets all the students' ID numbers,
        which are each integers.
        Stores this in self.l_students
        :return: list of student IDs
        """
        self.l_students = list(set(self.df_data['Registration number']))

        # checking if student IDs are all ints
        for i in self.l_students:
            if type(i) != int:
                raise TypeError('get_all_student_ids: Student IDs must be integers')

        return self.l_students

    def get_student_school(self, i_student_id: int) -> str:
        """
        Gets the student's school ID from dataframe
        :param i_student_id: integer student ID
        :return: string of the school ID
        """
        # name of school / school ID
        if i_student_id in self._d_rows and self._d_rows[i_student_id]:
            return str(self._d_rows[i_student_id][0]['School'])
        raise ValueError("get_student_school: unexpected results for student's school ID")

    def get_student_subjects(self, i_student_id: int) -> List[str]:
        """
        Gets all the subjects done by student with
        ID number i_student_id.
        :param i_student_id: integer student ID
        :return: list of all of student's subject
        """
        set_subjects = set()

        for row in self._d_rows[i_student_id]:
            if row['Level'] != 'EE':
                set_subjects.add(row['Subject'])

        l_student_subjects = list(set_subjects)
        return l_student_subjects

    def get_student_subject_info(self, i_student_id: int, s_subject: str) -> Dict[str, Union[str, int, Dict]]:
        """
        Gets the information about the student
        taking the particular subject.

        Organises the info into a dict as such:
        s_subject: {
                level: 'SL' or 'HL',
                grade: integer out of 7,
                total_mark: integer out of 100,
                language: 'ENGLISH', 'FRENCH', etc,
                *component1*: {
                    grade: integer out of 7,
                    mark: integer marks
                    },
                *component2* { ... }
                }

        CAREFUL: if component grade does not exist, the grade
        is changed to None.

        s_subject is NOT 'THEORY OF KNOWLEDGE.'

        :param i_student_id: integer student ID
        :param s_subject: str subject name
        :return: dictionary of info
        """

        # raise error if TOK is given as subject
        if s_subject == 'THEORY OF KNOWLEDGE.':
            raise ValueError('get_student_subject_info: TOK is unexpected subject')

        # dictionary to fill in
        d_subject = {}

        for row in self._d_rows[i_student_id]:
            s_sub = row['Subject']
            if s_sub == s_subject:

                # level at which subject is taken
                # standard or higher (SL or HL)
                s_lvl = row['Level']
                if s_lvl == 'EE':
                    # The case of EE will be handled elsewhere
                    continue
                elif s_lvl != 'EE':
                    # raise error if unexpected input
                    if s_lvl not in ('SL', 'HL'):
                        raise ValueError('get_student_subject_info: Subject level must '
                                         'be either "SL" or "HL"')
                    # else, update the dictionary
                    d_subject['level'] = s_lvl

                # grade out of 7
                d_subject['grade'] = int(row['Subject grade'])
                # mark out of 100
                d_subject['total_mark'] = int(row['Scaled total mark for subject'])
                # language in which subject taken
                d_subject['language'] = row['Language']

                # includes the component in d_subject
                # e.g. 'PAPER TWO'
                s_component = row['Component']
                # TODO make error message?
                # new dict with grade and mark of component
                d_component = {}
                # sometimes, people do not have a component grade or mark
                # instead, it is NaN - TODO make it easier
                # component grade
                try:
                    d_component['grade'] = int(row['Component grade'])
                except ValueError:
                    d_component['grade'] = None
                # component mark
                try:
                    d_component['mark'] = int(row['Component mark'])
                except ValueError:
                    d_component['mark'] = None
                d_subject[s_component] = d_component

        return d_subject

    def get_student_EE_info(self, i_student_id: int) -> Dict[str, Union[str, int]]:
        """
        Gets the information about TOK for
        particular student

        Organises the info into a dict as such:
        EE: {subject: str name of subject,
             letter_grade: 'A', 'B', 'C', ...,
             total_mark: integer out of 34,
             language: 'ENGLISH', etc,
             }

        :param i_student_id: integer student ID
        :return: dictionary of info
        """

        # dictionary to fill in
        d_ee = {}

        for idx, row in self.df_data.iterrows():
            i_id = row['Registration number']
            s_lvl = row['Level']
            if i_id == i_student_id and s_lvl == "EE":

                # subject of EE
                d_ee['subject'] = row['Subject']

                # get letter grade
                s_lttr = row['Subject grade']
                # raise error
                if s_lttr not in ('A', 'B', 'C', 'D', 'E'):
                    raise ValueError('get_student_EE_info: unexpected letter grade')
                d_ee['letter_grade'] = s_lttr

                # mark out of 34
                d_ee['total_mark'] = int(row['Scaled total mark for subject'])
                # language EE was written in
                d_ee['language'] = row['Language']

                # once the correct row is found, for loop must break
                break
        else:
            # if student's EE doesn't exist...
            d_ee = {'subject': 'NONE', 'letter_grade': 'E', 'total_mark': 0, 'language': 'NONE'}

        return d_ee

    def get_student_TOK_info(self, i_student_id: int) -> Dict[str, Union[str, int, Dict]]:
        """
        Gets the information about TOK for
        particular student

        Organises the info into a dict as such:
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
            }

        :param i_student_id: integer student ID
        :return: dictionary of info
        """

        # dictionary to fill in
        d_tok = {}

        # name of subject
        s_subject = 'THEORY OF KNOWLEDGE.'

        for row in self._d_rows[i_student_id]:
            s_sub = row['Subject']
            if s_sub == s_subject:

                # get letter grade
                s_lttr = row['Subject grade']
                # raise error
                if s_lttr not in ('A', 'B', 'C', 'D', 'E'):
                    raise ValueError('get_student_TOK_info: unexpected letter grade')
                d_tok['letter_grade'] = s_lttr

                # total mark out of 30
                d_tok['total_mark'] = int(row['Scaled total mark for subject'])
                # language in which TOK is taken
                d_tok['language'] = row['Language']

                # makes dict for this component
                d_component = {}
                d_component['mark'] = int(row['Component mark'])
                # get letter grade of component
                s_comp_lttr = row['Subject grade']
                # raise error
                if s_comp_lttr not in ('A', 'B', 'C', 'D', 'E'):
                    raise ValueError('get_student_TOK_info: unexpected component letter grade')
                d_component['letter_grade'] = s_comp_lttr

                # presentation
                if row['Component'] == 'PRESENTATION WORK':
                    d_tok['presentation'] = d_component

                # essay
                elif row['Component'] == 'THEORY OF KNOWLEDGE':
                    # double the mark of essay, as this is
                    # the coefficient for the final grade
                    d_component['mark'] = d_component['mark'] * 2
                    d_tok['essay'] = d_component

                if 'presentation' in d_tok and 'essay' in d_tok:
                    break
        else:
            # if student's TOK doesn't exist...
            d_tok = {'letter_grade': 'E', 'total_mark': 0, 'language': 'NONE',
                     'presentation': {'mark': 0, 'letter_grade': 'E'},
                     'essay': {'mark': 0, 'letter_grade': 'E'}}

        return d_tok


class CleanData:
    """
    This class is initiated by a set of data
    as a pandas dataframe, and cleans it into
    the following dictionary (called d_students),
    by using the class Data.

    """

    def __init__(self, d_students: Dict[int, Dict]):
        # See from_df method below for the format
        self.d_students = {int(k): v for k, v in d_students.items()}
        self.l_students = list(self.d_students.keys())

        # stores the conversion from EE
        # and TOK grades into the 3
        # additional core points
        self.d_core_points = {
            "AA": 3,
            "AB": 3,
            "AC": 2,
            "AD": 2,
            "BB": 2,
            "BC": 1,
            "BD": 1,
            "CC": 1,
            "CD": 0,
            "DD": 0,
        }

    @classmethod
    def from_df(cls, df_data: pd.DataFrame) -> 'CleanData':
        Da_data = Data(df_data)

        l_students = Da_data.l_students

        # Organises the data into dicts
        # of dicts as explained below:

        """
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
                    grade: integer out of 7, None otherwise,
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
        self = cls({})

        self.d_students = {i_id: {} for i_id in l_students}

        # for every student:
        for i_student_id in tqdm(l_students):

            # school number
            self.d_students[i_student_id]['school'] = Da_data.get_student_school(i_student_id)

            l_subjects = Da_data.get_student_subjects(i_student_id)

            # for every subject student takes:
            for s_subject in l_subjects:
                if s_subject != "THEORY OF KNOWLEDGE.":
                    self.d_students[i_student_id][s_subject] = Da_data.get_student_subject_info(i_student_id,
                                                                                                s_subject)

            # EE info
            self.d_students[i_student_id]['EE'] = Da_data.get_student_EE_info(i_student_id)

            # TOK info
            self.d_students[i_student_id]['TOK'] = Da_data.get_student_TOK_info(i_student_id)

            # core points (number of points gained from TOK and EE, out of 3)
            s_ee_lttr = self.d_students[i_student_id]['EE']['letter_grade']
            s_tok_lttr = self.d_students[i_student_id]['TOK']['letter_grade']

            # letter grades of both EE and TOK put together like 'BC' or 'AD'
            s_lttrs = s_ee_lttr + s_tok_lttr
            # raise error
            if "".join(sorted(s_lttrs)) not in self.d_core_points:
                del self.d_students[i_student_id]
                print(f'CleanData: unexpected letter grades for EE and TOK: {s_lttrs!r};\n'
                      f'Ignoring candidate {i_student_id}')
            else:
                self.d_students[i_student_id]['core_pt'] = self.d_core_points["".join(sorted(s_lttrs))]

        return self

    def get_students_doing(self, s_subject: str) -> List[int]:
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

    def get_student_grade_out_of_42(self, i_student: int) -> int:
        """
        Gets the total grade (out of 42)
        of a particular student.
        Requires self.
        :param i_student: student ID num
        :return: integer grade of 42
        """
        total_grade = 0
        for subject in self.d_students[i_student]:
            if subject in ('school', 'EE', 'TOK', 'core_pt'):
                continue
            total_grade += self.d_students[i_student][subject]['grade']
        return total_grade

    def get_student_grade_out_of_45(self, i_student: int) -> int:
        """
        Gets the total grade (out of 45)
        of a particular student.
        Requires self.
        :param i_student: student ID num
        :return: integer grade of 45
        """
        total_grade = 0
        for subject in self.d_students[i_student]:
            if subject in ('school', 'EE', 'TOK', 'core_pt'):
                continue
            total_grade += self.d_students[i_student][subject]['grade']
        total_grade += self.d_students[i_student]['core_pt']
        return total_grade

    def print_dict(self):
        """
        Prints all students' information dictionary
        """
        print(self.d_students)


if __name__ == '__main__':
    # path to files
    s_path = os.path.dirname(__file__)
    s_path_data = os.path.join(s_path, "data")

    s_data_fname = os.path.join(s_path_data, 'c2018_v2.csv')

    df_data = pd.read_csv(s_data_fname)

    CD_ib2018 = CleanData.from_df(df_data)

    # Cache processed data
    with open(os.path.join(s_path_data, 'cached_data.json'), 'w') as f:
        json.dump(CD_ib2018.d_students, f)
