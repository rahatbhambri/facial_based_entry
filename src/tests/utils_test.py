import unittest, string
from unittest.mock import patch, MagicMock
from utils.utils import generate_random_string, get_all_bookings, get_all_cinemas

class TestUtils(unittest.TestCase):

    @patch('utils.utils.db')  # Mock the database connection object
    def test_get_all_bookings(self, mock_db):
        # Mock ticket data for a user
        mock_db.tickets.find.return_value = [
            {"ticket_id": "12345", "booking_time": "2024-10-06 10:00"},
            {"ticket_id": "67890", "booking_time": "2024-10-07 12:00"}
        ]
        
        # Capture the print output
        with patch('builtins.print') as mocked_print:
            get_all_bookings(user_id="user123")
            mocked_print.assert_any_call("All tickets booked for user: ", "user123")
            mocked_print.assert_any_call("12345", "2024-10-06 10:00")
            mocked_print.assert_any_call("67890", "2024-10-07 12:00")
        
        # Ensure the database query was made with correct parameters
        mock_db.tickets.find.assert_called_once_with({"user_id": "user123"})
    
    @patch('utils.utils.db')  # Mock the database connection object
    def test_get_all_cinemas(self, mock_db):
        # Mock cinema data
        mock_db.cinemas.find.return_value = [
            {"name": "Cinema A", "cinema_id": "001"},
            {"name": "Cinema B", "cinema_id": "002"}
        ]
        
        # Call the function and check the result
        result = get_all_cinemas()
        expected_result = [
            {"name": "Cinema A", "cinema_id": "001"},
            {"name": "Cinema B", "cinema_id": "002"}
        ]
        self.assertEqual(result, expected_result)
        
        # Ensure the database query was made correctly
        mock_db.cinemas.find.assert_called_once_with({}, {"_id": 0, "name": 1, "cinema_id": 1})
    
    def test_generate_random_string(self):
        # Ensure the generated string has the correct length and consists of valid characters
        result = generate_random_string(length=10)
        self.assertEqual(len(result), 10)
        self.assertTrue(all(c in (string.ascii_uppercase + string.digits) for c in result))

        # Test default length of 8
        result_default = generate_random_string()
        self.assertEqual(len(result_default), 8)
        