"""The Python implementation of the gRPC budgeter server."""

import logging
import sys
import threading
from concurrent import futures
from time import sleep

import grpc
import protos.budgeter_pb2 as budgeter_pb2
import protos.budgeter_pb2_grpc as budgeter_pb2_grpc
from grpc_health.v1 import health, health_pb2, health_pb2_grpc
from grpc_reflection.v1alpha import reflection
from server import db

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


def _toggle_health(health_servicer: health.HealthServicer, service: str):
    next_status = health_pb2.HealthCheckResponse.SERVING
    while True:
        if next_status == health_pb2.HealthCheckResponse.SERVING:
            next_status = health_pb2.HealthCheckResponse.NOT_SERVING
        else:
            next_status = health_pb2.HealthCheckResponse.SERVING

        health_servicer.set(service, next_status)
        sleep(5)


def _configure_health_server(server: grpc.Server):
    #  We use the non-blocking implementation to avoid thread starvation.
    health_servicer = health.HealthServicer(
        experimental_non_blocking=True,
        experimental_thread_pool=futures.ThreadPoolExecutor(max_workers=10),
    )
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)

    # Use a daemon thread to toggle health status
    toggle_health_status_thread = threading.Thread(
        target=_toggle_health,
        args=(health_servicer, "Budgeter"),
        daemon=True,
    )
    toggle_health_status_thread.start()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    budgeter_pb2_grpc.add_BudgeterServicer_to_server(BudgeterServicer(), server)

    _configure_health_server(server)

    # Create a tuple of all of the services we want to export via reflection.
    SERVICE_NAMES = (
        budgeter_pb2.DESCRIPTOR.services_by_name["Budgeter"].full_name,
        reflection.SERVICE_NAME,
        health.SERVICE_NAME,
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
