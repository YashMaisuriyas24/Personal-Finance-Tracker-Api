from pymongo import MongoClient
import os
import dotenv

dotenv.load_dotenv()


class DB:
    def __init__(self):

        try:
            self.client = MongoClient(os.getenv("MONGO_URL"))
            self.db = self.client['Finance-Tracker']
            self.transactions = self.db['transactions']
            self.categories = self.db['categories']
            self.create_indexes()
            print(f"Successfully connected to Finance-Tracker-Database!")
        except Exception as e:
            print(f"Failed to connect to Tracker-Database! --- Due to : {e}")

    def create_indexes(self):
        try:
            self.transactions.create_index([("date", -1)])
            self.transactions.create_index([("category", 1), ("date", -1)])
            self.transactions.create_index([("type", 1), ("date", -1)])
            self.transactions.create_index([
                ("title", "text"),
                ("description", "text")
            ])
            self.categories.create_index("name", unique=True)

            print("Indexes created successfully")
        except Exception as e:
            print(f"Index creation error: {e}")


    def create_transaction(self,data):
        try:
            result = self.transactions.insert_one(data)
            return f" Inserted : {result.inserted_id}"
        except Exception as e:
            print(f" Unexpected Error while inserting: {e}")


    def get_all_transactions(self):
        try :
            transactions = self.transactions.find()
            return transactions

        except Exception as e:
            print(f"unexpected error while fetching all transactions records : {e}")

    def get_specific_transaction(self,transaction_id):
        try:
            if transaction_id:
                self.transactions = self.transactions.find_one({'_id': transaction_id})
            else:
                print(f'No transaction found with this {transaction_id}')
        except Exception as e:
            print(f"Unexpected error while fetching specific transaction: {e}")


    def update_transaction(self,transaction_id,data):
        try:
            if transaction_id:
                self.transactions = self.transactions.update_one({'_id': transaction_id}, {'$set': data})
            else:
                print(f'No transaction found with this {transaction_id}!')
        except Exception as e:
            print(f"Unexpected error while updating transaction: {e}")


    def  delete_transaction(self,transaction_id):
        try:
            if transaction_id:
                self.transactions = self.transactions.delete_one({'_id': transaction_id})
            else:
                print(f'No transaction found with this {transaction_id}!')
        except Exception as e:
            print(f"Unexpected error while deleting transaction: {e}")


    # CATEGORY

    def create_category(self, data):
        try:
            result = self.categories.insert_one(data)
            return f"Inserted Category : {result.inserted_id}"
        except Exception as e:
            print(f"Category Insert Error: {e}")

    def get_all_categories(self):
        try:
            return list(self.categories.find())
        except Exception as e:
            print(f"Category Fetch Error: {e}")

    def update_category(self, name, data):
        try:
            return self.categories.update_one(
                {"name": name},
                {"$set": data}
            )
        except Exception as e:
            print(f"Category Update Error: {e}")

    def delete_category(self, name):
        try:
            return self.categories.delete_one({"name": name})
        except Exception as e:
            print(f"Category Delete Error: {e}")



if __name__ == "__main__":
    db = DB()