from db import db


def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"Error: {e}"

    return wrapper


class CatHouse:
    def __init__(self):
        self.db = db()

    # READ
    @error_handler
    def get_all_cats(self):
        result = list(self.db.find())
        if len(result) == 0:
            return "No cats in the house"
        return result

    @error_handler
    def get_by_name(self, name):
        result = self.db.find_one({"name": name})
        if result is None:
            return f"Cat with name '{name}' not found"
        return result

    #UPDATE
    @error_handler
    def update_age_by_name(self, name, age):
        self.db.update_one(
            {'name': name},
            {'$set': {
                'age': age
            }})

        return f"{name}'s age updated to {age}"

    @error_handler
    def add_feature(self, name, feature):
        self.db.update_one(
            {'name': name},
            {'$push': {
                'features': feature
            }}
        )

    #DELETE
    @error_handler
    def delete_cat(self, name):
        self.db.delete_one({'name': name})
        print(f"Cat {name} was deleted successfully")

    @error_handler
    def delete_all(self):
        self.db.delete_many({})
        print("All cats were deleted successfully")
