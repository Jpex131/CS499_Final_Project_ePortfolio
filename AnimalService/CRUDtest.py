import unittest
from CRUDmodule import AnimalShelter


class TestCRUDOperations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize the AnimalShelter instance for all tests
        cls.shelter = AnimalShelter('yourUsername', 'yourPassword')  # Use actual credentials

        # Sample data for testing
        cls.data = {
            "age_upon_outcome": "3 years",
            "animal_id": "XY3028",
            "animal_type": "Dog",
            "breed": "Akita",
            "color": "Gray",
            "date_of_birth": "Aug 2018",
            "name": "Wren",
            "outcome_subtype": "",
            "outcome_type": "",
            "sex_upon_outcome": "Spayed Female",
            "age_upon_outcome_in_weeks": "164 weeks"
        }
        cls.key = {"animal_id": "XY3028"}

    def setUp(self):
        # Ensure the database is in a known state and add the test record
        self.shelter.delete(self.key)  # Attempt to clear out any existing test record
        self.shelter.create(self.data)

    def tearDown(self):
        # Clean up the database after each test
        self.shelter.delete(self.key)

    def test_create(self):
        # Test creating an additional record (with a new ID to avoid duplicates)
        new_data = self.data.copy()
        new_data["animal_id"] = "XY3029"  # Changing the ID for the test
        create_result = self.shelter.create(new_data)
        self.assertIsNotNone(create_result.inserted_id, "Create method failed to return an inserted ID")

    def test_read(self):
        # Test reading the test record
        read_result = list(self.shelter.read(self.key))
        self.assertTrue(any(read_result), "Read method failed to find the test record")

    def test_update(self):
        # Test updating the test record's color
        update_result = self.shelter.update(self.key, {"$set": {"color": "Black"}})
        self.assertTrue(update_result.modified_count > 0, "Update method failed to modify any records")

    def test_delete(self):
        # Test deleting the test record
        delete_result = self.shelter.delete(self.key)
        self.assertTrue(delete_result.deleted_count > 0, "Delete method failed to delete any records")


if __name__ == '__main__':
    unittest.main()
