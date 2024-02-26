# This module initiates the MongoClient authentication, and
# defines the Create(), Read(), Update(), and Delete() and handles possible errors
# READ() is used in the DB Dashboard in order to populate Database data
# CREATE(), UPDATE(), and DELETE() can only be run from the command line locally in order to confirm user authentication to alter database records
from pymongo import MongoClient
import logging
from datetime import datetime


class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB with advanced analysis and security enhancements """

    def __init__(self, username, password):
        # Initializing the MongoClient. Consider using a more secure connection method in production.
        self.client = MongoClient('mongodb://' + username + ":" + password + '@localhost:27017')
        self.database = self.client['AAC']

        # Initialize logging for audit trails
        logging.basicConfig(filename='database_operations.log', level=logging.INFO,
                            format='%(asctime)s:%(levelname)s:%(message)s')

    def log_operation(self, operation, data):
        """ Log database operations for audit trails """
        logging.info(f"{operation} operation performed on database with data: {data}")

    def create(self, data):
        """ Create operation with error handling and logging """
        if data:
            result = self.database.animals.insert_one(data)
            self.log_operation('CREATE', data)  # Log the create operation
            return result
        else:
            raise Exception("ERROR: Nothing to save, because data parameter is empty")

    def read(self, query):
        """ Read operation with logging """
        result = self.database.animals.find(query)
        self.log_operation('READ', query)  # Log the read operation
        return result

    def update(self, query, new_data):
        """ Update operation with error handling and logging """
        result = self.database.animals.update_one(query, {"$set": new_data})
        self.log_operation('UPDATE', {'query': query, 'new_data': new_data})  # Log the update operation
        return result

    def delete(self, query):
        """ Delete operation with error handling and logging """
        result = self.database.animals.delete_one(query)
        self.log_operation('DELETE', query)  # Log the delete operation
        return result

    def aggregate_data(self, aggregation_pipeline):
        """ Perform complex aggregation queries for advanced data analysis """
        result = self.database.animals.aggregate(aggregation_pipeline)
        self.log_operation('AGGREGATE', aggregation_pipeline)  # Log the aggregation operation
        return result


# Example usage of the enhanced AnimalShelter class

if __name__ == "__main__":
    # Initialize the AnimalShelter instance (replace 'username' and 'password' with actual credentials)
    shelter = AnimalShelter('username', 'password')

    # Example of creating a new animal record
    new_animal_data = {
        "animal_id": "A123",
        "breed": "Labrador",
        "location": {"lat": 40.7128, "long": -74.0060},
        "status": "available"
    }
    shelter.create(new_animal_data)

    # Example of reading animal records with a query
    query = {"animal_id": "A123"}
    print(list(shelter.read(query)))

    # Example of updating an animal record
    new_data = {"status": "adopted"}
    shelter.update(query, new_data)

    # Example of deleting an animal record
    shelter.delete(query)

    # Example of using aggregate for advanced data analysis
    aggregation_pipeline = [
        {"$match": {"status": "adopted"}},
        {"$group": {"_id": "$breed", "count": {"$sum": 1}}}
    ]
    print(list(shelter.aggregate_data(aggregation_pipeline)))
