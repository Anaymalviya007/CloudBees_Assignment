import unittest
import train_service_pb2
from server import TrainService

class TestTrainService(unittest.TestCase):
    def setUp(self):
        self.service = TrainService()

    def test_purchase_ticket(self):
        request = train_service_pb2.PurchaseTicketRequest(departure="London", to="France", user=train_service_pb2.User(first_name="Test", last_name="User", email="test@example.com"))
        response = self.service.PurchaseTicket(request, None)
        self.assertIsNotNone(response.receipt_id)

    def test_get_receipt(self):
        # First, create a ticket to get a receipt_id
        request = train_service_pb2.PurchaseTicketRequest(departure="London", to="France", user=train_service_pb2.User(first_name="Test", last_name="User", email="test@example.com"))
        purchase_response = self.service.PurchaseTicket(request, None)

        # Now, use the receipt_id to get the receipt
        request = train_service_pb2.GetReceiptRequest(receipt_id=purchase_response.receipt_id)
        response = self.service.GetReceipt(request, None)
        self.assertEqual(response.user.first_name, "Test")
        self.assertEqual(response.user.last_name, "User")
        self.assertEqual(response.user.email, "test@example.com")

    def test_remove_user(self):
        # First, create a ticket to get a receipt_id
        request = train_service_pb2.PurchaseTicketRequest(departure="London", to="France", user=train_service_pb2.User(first_name="Test", last_name="User", email="test@example.com"))
        purchase_response = self.service.PurchaseTicket(request, None)

        # Now, use the receipt_id to remove the user
        request = train_service_pb2.RemoveUserRequest(receipt_id=purchase_response.receipt_id)
        self.service.RemoveUser(request, None)

        # Try to get the receipt for the removed user, should raise an exception
        request = train_service_pb2.GetReceiptRequest(receipt_id=purchase_response.receipt_id)
        with self.assertRaises(Exception):
            self.service.GetReceipt(request, None)

    def test_modify_user_seat(self):
        # First, create a ticket to get a receipt_id
        request = train_service_pb2.PurchaseTicketRequest(departure="London", to="France", user=train_service_pb2.User(first_name="Test", last_name="User", email="test@example.com"))
        purchase_response = self.service.PurchaseTicket(request, None)

        # Now, use the receipt_id to modify the user seat
        request = train_service_pb2.ModifyUserSeatRequest(receipt_id=purchase_response.receipt_id, new_seat="A1")
        self.service.ModifyUserSeat(request, None)

        # Get the receipt and check if the seat has been modified
        request = train_service_pb2.GetReceiptRequest(receipt_id=purchase_response.receipt_id)
        response = self.service.GetReceipt(request, None)
        self.assertEqual(response.seat, "A1")




if __name__ == "__main__":
    unittest.main()