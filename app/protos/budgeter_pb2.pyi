from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Transaction(_message.Message):
    __slots__ = ("date", "envelope", "account", "name", "notes", "amount", "details")
    DATE_FIELD_NUMBER: _ClassVar[int]
    ENVELOPE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NOTES_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    date: _timestamp_pb2.Timestamp
    envelope: str
    account: str
    name: str
    notes: str
    amount: float
    details: str
    def __init__(self, date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., envelope: _Optional[str] = ..., account: _Optional[str] = ..., name: _Optional[str] = ..., notes: _Optional[str] = ..., amount: _Optional[float] = ..., details: _Optional[str] = ...) -> None: ...

class RecordTransactionsRequest(_message.Message):
    __slots__ = ("transactions",)
    TRANSACTIONS_FIELD_NUMBER: _ClassVar[int]
    transactions: _containers.RepeatedCompositeFieldContainer[Transaction]
    def __init__(self, transactions: _Optional[_Iterable[_Union[Transaction, _Mapping]]] = ...) -> None: ...

class RecordTransactionsReply(_message.Message):
    __slots__ = ("transactions_count",)
    TRANSACTIONS_COUNT_FIELD_NUMBER: _ClassVar[int]
    transactions_count: int
    def __init__(self, transactions_count: _Optional[int] = ...) -> None: ...
