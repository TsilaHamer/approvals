import time

from flask import request, jsonify

from approval.extensions import LOG
from . import api
from ..models import Approval, Approval_Hist

#todo: request id for each request
#todo: logs for error in update db


@api.route('/approval/<string:id_num>')
def get_approval_by_id(id_num):
    LOG.info('{current_timestamp}: request for get id {id_num} is handled'.format(
        current_timestamp=time.time(), id_num=id_num))
    approval = Approval.objects(id_num=id_num).first()
    if approval:
        LOG.info('{current_timestamp}: response for {id_num}: {approval}'.
            format(current_timestamp=time.time(), id_num=id_num,
                   approval=approval.to_json()))
        return jsonify(approval)
    else:
        LOG.error('{current_timestamp}: The requested id {id_num} does not'
                  ' exist'.format(current_timestamp=time.time(), id_num=id_num))
        return jsonify({'error': 'The requested id_num does not exist'}), 404


@api.route('/upsert_approval', methods=['POST', 'PUT'])
def upsert_approval():
    approval_data = dict(request.form)
    LOG.info('{current_timestamp}: request for update id {id_num} is handled'.
             format(current_timestamp=time.time(),
                    id_num=approval_data.get('id_num')))
    approval_exists = Approval.objects(
        id_num=approval_data.get('id_num')).first()
    approval = Approval.from_json(approval_data)
    if approval_exists:
        if approval_exists.value_update_date < \
           int(approval_data.get('value_update_date')):
            #todo: update or delete and insert?
            approval_exists.update(**approval_data)
        else:
            approval_exists.update(
                **{"db_last_update_date": int(time.time())}
            )
    else:
        approval.save()
    approval_hist = Approval_Hist.from_json(approval_data)
    approval_hist.save()
    LOG.info('{current_timestamp}: id {id_num} was updated in db'.
             format(current_timestamp=time.time(),
                    id_num=approval_data.get('id_num')))
    return jsonify(approval), 201


@api.route('/delete_approval/<string:id_num>', methods=['DELETE'])
def delete_approval(id_num):
    LOG.info('{current_timestamp}: request for delete id {id_num} is handled'.
             format(current_timestamp=time.time(),
                    id_num=id_num))
    approval = Approval.objects(id_num=id_num).first()
    if not approval:
        LOG.error('{current_timestamp}: The requested id {id_num} does not'
                  ' exist'.format(current_timestamp=time.time(),
                                  id_num=id_num))
        return jsonify({'error': 'The requested id_num does not exist'}), 404
    approval.delete()
    LOG.info('{current_timestamp}: id {id_num} was deleted'
              ' exist'.format(current_timestamp=time.time(), id_num=id_num))
    return jsonify(approval)