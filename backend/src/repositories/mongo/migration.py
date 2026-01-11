from pymongo.collection import Collection


def init_student_collection(collection: Collection):
    collection.create_index("email", unique=True)


def init_enrollment_collection(collection: Collection):
    collection.create_index(
        [("student_id", 1), ("course_id", 1)], unique=True, name="student_course_unique_idx"
    )

    collection.create_index([("student_id", 1)], name="student_idx")

    collection.create_index([("course_id", 1)], name="course_idx")


def init_cs50_submission_problem_collection(collection: Collection):
    collection.create_index("slug", unique=True, name="slug_unique_idx")
