from pymongo.collection import Collection


def init_student_collection(collection: Collection):
    collection.create_index("email", unique=True)
