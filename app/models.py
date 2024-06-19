from decimal import Decimal
from datetime import datetime, timezone
import enum

from sqlalchemy.orm import backref
import sqlalchemy as sqlalchemy
import sqlalchemy.orm as orm
from typing import List
from typing import Optional
from app.api.constants import ACTIVE_VALUE
from app.api.constants import BLOCKED_VALUE
from app.extensions import db


class TransactionTypeEnum(enum.Enum):
    deposit = "deposito"
    withdraw = "saque"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.name, cls))


class Person(db.Model):
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(30), nullable=False)
    cpf: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(14), unique=True, nullable=False)
    birthdate: orm.Mapped[datetime] = orm.mapped_column(
        default=lambda: datetime.now(timezone.utc), nullable=False)
    email: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(120), index=True, unique=True)


class AccountTypeEnum(enum.Enum):
    individual = "pessoaFisica"
    company = "pessoaJuridica"


class Account(db.Model):
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    person_id: orm.Mapped[int] = orm.mapped_column(sqlalchemy.ForeignKey(Person.id),
                                               index=True, nullable=False)
    
    person = db.relationship('Person', foreign_keys=person_id)
    balance: orm.Mapped[Decimal] = orm.mapped_column(sqlalchemy.DECIMAL, nullable=False, default=0)
    daily_withdraw_limit: orm.Mapped[Decimal] = orm.mapped_column(sqlalchemy.DECIMAL, nullable=False, default=0)
    active_flag: orm.Mapped[bool] = orm.mapped_column(sqlalchemy.Boolean, default=True)
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        default=lambda: datetime.now(timezone.utc), nullable=False)

    account_type = db.Column(
        db.Enum(AccountTypeEnum),
        nullable=False,
        name='tipoConta',
        default=AccountTypeEnum.individual.value
    )
    transactions: orm.Mapped[List["Transaction"]] = orm.relationship(back_populates='account', lazy="noload")

    @property
    def status(self):
        return ACTIVE_VALUE if self.active_flag else BLOCKED_VALUE


class Transaction(db.Model):
    default_time = lambda: datetime.now(timezone.utc)
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    account_id: orm.Mapped[int] = orm.mapped_column(sqlalchemy.ForeignKey(Account.id),
                                               index=True)
    value: orm.Mapped[Decimal] = orm.mapped_column(sqlalchemy.DECIMAL, nullable=False, default=0)
    transaction_date: orm.Mapped[datetime] = orm.mapped_column(
        default=default_time, onupdate=default_time, nullable=False)
    account: orm.Mapped[Account] = orm.relationship(back_populates='transactions')
    
    transaction_type = db.Column(
        db.Enum(TransactionTypeEnum),
        name='tipoTransacao',
        nullable=False,
        default=TransactionTypeEnum.deposit.value
    )
    description: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(80))


class Filters:

    _from = None
    _to = None
    limit = 50      # it's good to have a default limit.
    offset = 0

    def __init__(self, _from=None, _to=None, limit=None, offset=None):
        self._from = _from
        self._to = _to
        self.limit = limit
        self.offset = offset