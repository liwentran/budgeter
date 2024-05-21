"""The Python implementation of the gRPC budgeter server."""

from __future__ import print_function

import logging
import sys

sys.path.append("/usr/app/protos")
from datetime import datetime

import grpc
import protos.budgeter_pb2 as budgeter_pb2
import protos.budgeter_pb2_grpc as budgeter_pb2_grpc
from google.protobuf.timestamp_pb2 import Timestamp
from grpc_health.v1 import health_pb2, health_pb2_grpc


def make_transaction(
    date: datetime,
    envelope: str,
    account: str,
    name: str,
    notes: str,
    amount: float,
    details: str,
) -> budgeter_pb2.Transaction:
    timestamp = Timestamp()
    return budgeter_pb2.Transaction(
        date=timestamp.FromDatetime(date),
        envelope=envelope,
        account=account,
        name=name,
        notes=notes,
        amount=amount,
        details=details,
    )


def budgeter_record_transactions(stub: budgeter_pb2_grpc.BudgeterStub):
    request = budgeter_pb2.RecordTransactionsRequest(
        transactions=[
            make_transaction(
                datetime(2016, 3, 4),
                "food",
                "main",
                "Laundry",
                "",
                5.90,
                "double load",
            )
        ]
    )

    reply = stub.RecordTransactions(request)
    if not reply:
        print("Server returned incomplete feature")
        return

    if reply.transactions_count:
        print(
            f"RecordTransaction successful, received {reply.transactions_count} transactions"
        )
    else:
        print("RecoredTransaction reply had no transactions_count")


def health_check_call(stub: health_pb2_grpc.HealthStub):
    request = health_pb2.HealthCheckRequest(service="Budgeter")
    resp = stub.Check(request)
    if resp.status == health_pb2.HealthCheckResponse.SERVING:
        print("server is serving")
    elif resp.status == health_pb2.HealthCheckResponse.NOT_SERVING:
        print("server stopped serving")


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel("server:50051") as channel:
        health_stub = health_pb2_grpc.HealthStub(channel)
        health_check_call(health_stub)
        stub = budgeter_pb2_grpc.BudgeterStub(channel)
        print("-------------- GetFeature --------------")
        budgeter_record_transactions(stub)


if __name__ == "__main__":
    logging.basicConfig()
    run()
