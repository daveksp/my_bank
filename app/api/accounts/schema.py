from marshmallow import post_load
from marshmallow import validates
import simplejson

from app.api.common.failures import Failures as CommonFailures
from app.api.common.validators import validate_monetary_value
from app.api.exceptions import RequestDataException
from app.api.extensions import schemas
from app.api.persons.schema import PersonSchema
from app.api.transactions.schema import TransactionSchema
from app.models import Account


class BalanceSchema(schemas.Schema):
    id = schemas.Integer(required=True, dump_only=True)
    balance = schemas.Decimal(required=False)
    person = schemas.Nested(PersonSchema, only=['name'])

    class Meta:
        json_module = simplejson


class StatementSchema(schemas.Schema):
    id = schemas.Integer(required=True, dump_only=True)
    balance = schemas.Decimal(required=False)
    person = schemas.Nested(PersonSchema, only=['name'])
    transactions = schemas.Nested(TransactionSchema, required=False, many=True)

    class Meta:
        json_module = simplejson


class AccountSchema(schemas.Schema):
    id = schemas.Integer(required=True, dump_only=True)
    person = schemas.Nested(
        PersonSchema, exclude=['id'], required=True
    )
    active_flag = schemas.Boolean(required=False)
    balance = schemas.Decimal(required=False)
    daily_withdraw_limit = schemas.Decimal(required=True)
    status = schemas.String(dump_only=True)
    created_at = schemas.Date(required=True, dump_only=True)
    account_type = schemas.String(required=True)

    class Meta:
        json_module = simplejson

    def handle_error(self, exc, data, many, partial):
        response = CommonFailures.information_missing
        response['details'] = exc.messages
        raise RequestDataException(response)

    @validates('daily_withdraw_limit')
    def validate_daily_withdraw_limit(self, withdraw_limit):
        validate_monetary_value(withdraw_limit, 'daily_withdraw_limit')

    @validates('balance')
    def validate_initial_balance(self, balance):
        validate_monetary_value(balance, 'balance')

    @post_load
    def make_order(self, data, many, partial):
        return Account(**(data or {}))
