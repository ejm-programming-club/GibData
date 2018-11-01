import csv
import sqlite3
import os


DATA_FILE_NAME = "c2018.csv"
DB_FILE_NAME = "c2018.db"
DATA_FOLDER = "data"

CATEGORIES = {
    "PAPER ONE": "paper1", "PAPER TWO": "paper2", "PAPER THREE": "paper3",
    "PROJECT": "project", "EXPLORATION": "exploration", "INTERNAL ASSESSMENT": "ia"
}
SCIENCES = ["BIOLOGY", "CHEMISTRY", "PHYSICS"]
LANGUAGES = ["ENGLISH", "FRENCH", "SPANISH", "GERMAN", "ITALIAN", "MANDARIN"]
BLOCK_3 = ["GEOGRAPHY", "HISTORY", "ECONOMICS"]


def to_key_value(l):
    """Converts a list of tuples to: a1 = 'b1', a2 = 'b2', ..., an = 'bn'"""
    return ", ".join([f"{a} = '{b}'" for a, b in l])


def converted_to_db(force_update=False):
    """
    Convert the csv file to a database
    :param force_update: regenerates the db from csv even if the db even exists
    :return:
    """
    if os.path.isfile(f"{DATA_FOLDER}/{DB_FILE_NAME}") and not force_update:
        print("Database already created")
        return

    print(os.getcwd())

    # Read CSV
    with open(f"{DATA_FOLDER}/{DATA_FILE_NAME}") as f:
        r = csv.reader(f.readlines(), delimiter=";")

    head, *rest = list(r)
    conn = sqlite3.connect(f"{DATA_FOLDER}/{DB_FILE_NAME}")
    cursor = conn.cursor()
    table_headers = [
        ("id", "integer"),
        ("ee_subject", "string"),
        ("ee_grade", "integer"),
        ("tok_presentation_grade", "integer"),
        ("tok_essay_grade", "integer"),
    ]

    for i in range(1, 7):
        # iterate over the 6 blocks
        # if i == 1 or i == 6:
        #     # languages (max)
        #     # TODO check if there are 3 papers in some other places
        #     n_papers = 3
        # else:
        n_papers = 3

        table_headers += [(f"block{i}_subject", "string"), (f"block{i}_level", "string")] + \
                         [(f"block{i}_paper{p}_score", "integer") for p in range(1, n_papers + 1)]

        if i == 3:
            table_headers += [("block3_ia_score", "integer")]
        if i == 5:
            table_headers += [("block5_project_score", "integer"), ("block5_exploration_score", "integer")]

    if force_update:
        cursor.execute(f"DROP TABLE if exists students")
    cursor.execute(
        f"CREATE TABLE if not exists students ({', '.join([f'{a} {b}' for a, b in table_headers])})"
    )

    ids_already_added = set()
    for row in rest:  # the first two aren't important
        # 0 -> Year
        # 1 -> Month
        # 2 -> Subject
        # 3 -> Level
        # 4 -> Component (Paper # / Exhibition / TOK / EXTENDED ESSAY)
        # 5 -> Language
        # 6 -> School
        # 7 -> Registration number
        # 8 -> Component grade
        # 9 -> Scaled total mark for subject
        # 10 -> Subject grade (letter for TOK & EE, /7 for the rest)

        subject = row[2]
        level = row[3]
        test_type = row[4]
        # lang = row[5]
        # we skip school num (6)
        student_id = row[7]
        component_grade = row[8]
        scaled_grade = row[9]
        subject_grade = row[10]

        if student_id not in ids_already_added:
            cursor.execute(f"INSERT INTO students (id) VALUES ({student_id})")
            ids_already_added.add(student_id)

        if test_type == "EXTENDED ESSAY":
            # EE
            to_set = [("ee_subject", subject), ("ee_grade", scaled_grade)]
        elif level == "TK":
            # TOK Essay & Presentation
            to_set = [(
                "tok_presentation_grade" if "PRESENTATION" in test_type else "tok_essay_grade", scaled_grade
            )]
        elif subject in BLOCK_3:
            # H/G/ECO (block 3)
            to_set = [
                ("block3_subject", subject), ("block3_level", level),
                (f"block3_{CATEGORIES[test_type]}_score", scaled_grade)
            ]
        elif "MATH" in subject:
            # Maths (block 5)
            level = level if "STUDIES" not in subject else "MS"
            to_set = [
                ("block5_subject", "MATH"), ("block5_level", level),
                (f"block5_{CATEGORIES[test_type]}_score", scaled_grade)
            ]
        else:
            print(subject, level, test_type)
        cursor.execute(f"UPDATE students SET {to_key_value(to_set)} WHERE id = {student_id}")

    conn.commit()
    conn.close()


converted_to_db(force_update=True)
