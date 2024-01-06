import grpc
from concurrent import futures
import uuid
import train_service_pb2
import train_service_pb2_grpc

class TrainService(train_service_pb2_grpc.TrainServiceServicer):
    def __init__(self):
        self._receipts = {}
        self._sections = {"A": [str(i) for i in range(1, 51)], "B": [str(i) for i in range(1, 51)]}

    def PurchaseTicket(self, request, context):
        receipt_id = str(uuid.uuid4())
        self._receipts[receipt_id] = {
            "departure": request.departure,
            "to": request.to,
            "user": request.user,
            "price_paid": 20.0,
            "seat": self._allocate_seat(),
        }
        return train_service_pb2.PurchaseTicketResponse(receipt_id=receipt_id)

    def GetReceipt(self, request, context):
        receipt = self._receipts.get(request.receipt_id)
        if receipt:
            return train_service_pb2.GetReceiptResponse(**receipt)
        else:
            context.abort(grpc.StatusCode.NOT_FOUND, "Receipt not found")

    def ViewUsersBySection(self, request, context):
        users = [receipt["user"] for receipt in self._receipts.values() if receipt["seat"].startswith(request.section)]
        return train_service_pb2.ViewUsersBySectionResponse(users=users)

    def RemoveUser(self, request, context):
        if request.receipt_id in self._receipts:
            del self._receipts[request.receipt_id]
        else:
            context.abort(grpc.StatusCode.NOT_FOUND, "Receipt not found")
        return train_service_pb2.RemoveUserResponse()

    def ModifyUserSeat(self, request, context):
        if request.receipt_id in self._receipts:
            self._receipts[request.receipt_id]["seat"] = request.new_seat
        else:
            context.abort(grpc.StatusCode.NOT_FOUND, "Receipt not found")
        return train_service_pb2.ModifyUserSeatResponse()

    def _allocate_seat(self):
        for i in range(1, 51):  # 50 seats per section
            for section in self._sections:  # iterate over sections
                if str(i) in self._sections[section]:  # if seat is available in this section
                    self._sections[section].remove(str(i))  # remove the seat from available seats
                    return f"{section}{i}"  # return the seat
        raise RuntimeError("Train is full")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    train_service_pb2_grpc.add_TrainServiceServicer_to_server(TrainService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()