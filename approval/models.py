import time
from datetime import datetime

from mongoengine import *

from approval.extensions import db


class Approval(db.Document):
    id_num = StringField(required=True)
    id_type = StringField(required=True)
    update_system = StringField(required=True)
    update_user = StringField(required=True)
    source_update_date = LongField(required=True)
    value_update_date = LongField(required=True)
    approval_status = StringField(required=True)
    db_last_update_date = LongField(default=int(time.time()))

    def to_json(self):
        json_approval = {
            'id_num': self.id_num,
            'id_type': self.id_type,
            'update_system': self.update_system,
            'update_user': self.update_user,
            'source_update_date': self.source_update_date,
            'value_update_date': self.value_update_date,
            'approval_status': self.approval_status,
            'db_last_update_date': self.db_last_update_date,
            'timestamp': datetime.utcnow
        }
        return json_approval

    @staticmethod
    def from_json(json_approval):
        return Approval(id_num=json_approval.get('id_num'),
                        id_type=json_approval.get('id_type'),
                        update_system=json_approval.get('update_system'),
                        update_user=json_approval.get('update_user'),
                        source_update_date=json_approval.get('source_update_date'),
                        value_update_date=json_approval.get('value_update_date'),
                        approval_status=json_approval.get('approval_status'))

    @staticmethod
    def insert_approvals():
        approval_json = {
            "id_num": "333",
            "id_type": "id",
            "update_system": "website",
            "update_user": "tsila",
            "source_update_date": 1569127415,
            "value_update_date": 1569127415,
            "approval_status": "agree"}
        approval = Approval.from_json(approval_json)
        approval.save()
        approval_json = {
            "id_num": "555",
            "id_type": "id",
            "update_system": "website",
            "update_user": "tsila",
            "source_update_date": 1569127415,
            "value_update_date": 1569127415,
            "approval_status": "agree"}
        approval = Approval.from_json(approval_json)
        approval.save()


# inheritation?
class Approval_Hist(db.Document):
    id_num = StringField(required=True)
    id_type = StringField(required=True)
    update_system = StringField(required=True)
    update_user = StringField(required=True)
    source_update_date = LongField(required=True)
    value_update_date = LongField(required=True)
    approval_status = StringField(required=True)
    db_update_date = LongField(default=int(time.time()))

    def to_json(self):
        json_approval = {
            'id_num': self.id_num,
            'id_type': self.id_type,
            'update_system': self.update_system,
            'update_user': self.update_user,
            'source_update_date': self.source_update_date,
            'value_update_date': self.value_update_date,
            'approval_status': self.approval_status,
            'db_update_date': self.db_update_date,
            'timestamp': datetime.utcnow
        }
        return json_approval

    @staticmethod
    def from_json(json_approval):
        return Approval_Hist(
            id_num=json_approval.get('id_num'),
            id_type=json_approval.get('id_type'),
            update_system=json_approval.get('update_system'),
            update_user=json_approval.get('update_user'),
            source_update_date=json_approval.get('source_update_date'),
            value_update_date=json_approval.get('value_update_date'),
            approval_status=json_approval.get('approval_status'))