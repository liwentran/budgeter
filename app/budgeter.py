"""The Python implementation of the gRPC budgeter server."""

from concurrent import futures
import logging
import sys

import grpc
import db
import protos.budgeter_pb2 as budgeter_pb2
import protos.budgeter_pb2_grpc as budgeter_pb2_grpc
from grpc_reflection.v1alpha import reflection

is_ready = False


def record_transaction(transaction: budgeter_pb2.Transaction):
    db.add_transaction("db", "transactions", transaction.name, transaction.notes)


class BudgeterServicer(budgeter_pb2_grpc.BudgeterServicer):
    """BudgeterServicer provides an implementation of the methods of the Budgeter service."""

    def __init__(self):
        self.database = "db"
        self.table = "transactions"
        self.reset_db()

    def reset_db(self):
        db.reset_database(self.database)
        db.reset_transactions_table(self.database, self.table)

    def RecordTransactions(
        self,
        request: budgeter_pb2.RecordTransactionsRequest,
        context: grpc.ServicerContext,
    ):
        print("RecordTransaction called")
        num_transaction = 0
        for transaction in request.transactions:
            record_transaction(transaction)
            num_transaction += 1
        return budgeter_pb2.RecordTransactionsReply(transactions_count=num_transaction)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    budgeter_pb2_grpc.add_BudgeterServicer_to_server(BudgeterServicer(), server)
    SERVICE_NAMES = (
        budgeter_pb2.DESCRIPTOR.services_by_name["Budgeter"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port("[::]:50051")
    server.start()
    global is_ready
    is_ready = True
    server.wait_for_termination()


def ready() -> bool:
    if is_ready:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    logging.basicConfig()
    serve()
