from pymongo import MongoClient
import os
import dotenv

dotenv.load_dotenv()


class DB:
    """
        A database wrapper class for managing transactions and categories in MongoDB.
     """
    def __init__(self):
        """
           Initializes the MongoDB client using the MONGO_URL from environment variables
           and sets up references to collections.
        """
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
        """
            Creates performance-optimizing indexes for date, category, and type,
            plus a text search index for transaction titles and descriptions.
        """
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
        """
            Inserts a single transaction record into the database.
            :param data: Dictionary containing transaction details (title, amount, category, date, etc.)
            :return: String message with the inserted ID.
        """
        try:
            result = self.transactions.insert_one(data)
            return f" Inserted : {result.inserted_id}"
        except Exception as e:
            print(f" Unexpected Error while inserting: {e}")


    def get_all_transactions(self):
        """
            Retrieves all transaction records from the database.
            :return: A MongoDB cursor pointing to all transactions.
        """
        try :
            transactions = self.transactions.find()
            return transactions

        except Exception as e:
            print(f"unexpected error while fetching all transactions records : {e}")

    def get_specific_transaction(self,transaction_id):
        """
            Retrieves a single transaction by its unique ID.
            :param transaction_id: The ObjectId or ID of the transaction to find.
            :return: The transaction document or None if not found.
        """
        try:
            if transaction_id:
                self.transactions = self.transactions.find_one({'_id': transaction_id})
            else:
                print(f'No transaction found with this {transaction_id}')
        except Exception as e:
            print(f"Unexpected error while fetching specific transaction: {e}")


    def update_transaction(self,transaction_id,data):
        """
            Updates an existing transaction identified by its ID.
            :param transaction_id: The ID of the transaction to update.
            :param data: Dictionary of fields and values to update.
            :return: UpdateResult object.
         """
        try:
            if transaction_id:
                self.transactions = self.transactions.update_one({'_id': transaction_id}, {'$set': data})
            else:
                print(f'No transaction found with this {transaction_id}!')
        except Exception as e:
            print(f"Unexpected error while updating transaction: {e}")


    def  delete_transaction(self,transaction_id):
        """
            Deletes a transaction record from the database.
            :param transaction_id: The ID of the transaction to remove.
            :return: DeleteResult object.
        """
        try:
            if transaction_id:
                self.transactions = self.transactions.delete_one({'_id': transaction_id})
            else:
                print(f'No transaction found with this {transaction_id}!')
        except Exception as e:
            print(f"Unexpected error while deleting transaction: {e}")


    # CATEGORY

    def create_category(self, data):
        """
            Adds a new category for transaction classification.
            :param data: Dictionary containing category details (e.g., {'name': 'Food'}).
            :return: String message with the inserted category ID.
        """
        try:
            result = self.categories.insert_one(data)
            return f"Inserted Category : {result.inserted_id}"
        except Exception as e:
            print(f"Category Insert Error: {e}")

    def get_all_categories(self):
        """
            Retrieves a list of all available categories.
            :return: List of category documents.
        """
        try:
            return list(self.categories.find())
        except Exception as e:
            print(f"Category Fetch Error: {e}")

    def update_category(self, name, data):
        """
            Updates a category document identified by its name.
            :param name: String name of the category to update.
            :param data: Dictionary of fields to update.
            :return: UpdateResult object.
        """
        try:
            return self.categories.update_one(
                {"name": name},
                {"$set": data}
            )
        except Exception as e:
            print(f"Category Update Error: {e}")

    def delete_category(self, name):
        """
           Removes a category from the database based on its name.
           :param name: String name of the category to delete.
           :return: DeleteResult object.
         """
        try:
            return self.categories.delete_one({"name": name})
        except Exception as e:
            print(f"Category Delete Error: {e}")



if __name__ == "__main__":
    db = DB()