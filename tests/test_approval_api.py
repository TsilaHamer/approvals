import json
import time
import unittest

from approval import create_app
from approval.models import Approval


class APITestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        test_app = create_app('testing', name='test_app')
        Approval.drop_collection()
        Approval.insert_approvals()

    @classmethod
    def tearDownClass(cls):
        Approval.drop_collection()

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.id_num = '333'
        self.id_num_new = '111'
        self.id_num_to_delete = '555'
        self.not_exist_id_num = '000'

    def tearDown(self):
        self.app_context.pop()

    def test_get_approval_by_id(self):
        # test success response
        response = self.client.get(
            '/approval/{id_num}'.format(id_num=self.id_num))
        self.assertEqual(response.status_code, 200)

        # test 404 for wrong url
        response = self.client.get(
            '/wrong/url')
        self.assertEqual(response.status_code, 404)
        response_data = response.get_data(as_text=True)
        self.assertIn('404 Not Found', response_data)

        # test 404 for id_num that does not exist
        response = self.client.get(
            '/approval/{id_num}'.format(id_num=self.not_exist_id_num))
        self.assertEqual(response.status_code, 404)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['error'],
                         'The requested id_num does not exist')

    def test_upsert_approval(self):
        # insert new approval
        approval_data = {
             "id_type": "id",
             "update_system": "website",
             "update_user": "tsila",
             "source_update_date": int(time.time()) - 20,
             "value_update_date": int(time.time()) - 20,
             "approval_status": "agree"}
        response = self.client.post(
             "approval/{}".format(self.id_num), data=approval_data)
        self.assertEqual(response.status_code, 201)

        # check that the new approval exists
        response = self.client.get(
            '/approval/{id_num}'.format(id_num=self.id_num))
        self.assertEqual(response.status_code, 200)

        json_response = json.loads(response.get_data(as_text=True))
        subset_json_response = {
            k: v for k, v in json_response.items()
            if k in approval_data}
        self.assertDictEqual(approval_data, subset_json_response)

        # edit the new approval
        new_approval_data = {
            "id_type": "id",
            "update_system": "myPensya",
            "update_user": "tsila",
            "source_update_date": int(time.time()),
            "value_update_date": int(time.time()),
            "approval_status": "disagree"}
        response = self.client.post(
            "approval/{}".format(self.id_num_new), data=new_approval_data)
        self.assertEqual(response.status_code, 201)

        # check that update is successful
        response = self.client.get(
            '/approval/{id_num}'.format(id_num=self.id_num_new))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        subset_json_response = {
            k: v for k, v in json_response.items()
            if k in new_approval_data}
        self.assertDictEqual(new_approval_data, subset_json_response)

        # edit the new approval with earlier value_update_date
        response = self.client.post(
            "approval/{}".format(self.id_num_new), data={
            "id_type": "id",
            "update_system": "sibel",
            "update_user": "tsila",
            "source_update_date": int(time.time()),
            "value_update_date": int(time.time()) - 50,
            "approval_status": "agree"
            })
        self.assertEqual(response.status_code, 201)

        # check that the approval was not changed
        response = self.client.get(
            '/approval/{id_num}'.format(id_num=self.id_num_new))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        subset_json_response = {
            k: v for k, v in json_response.items()
            if k in new_approval_data}
        self.assertDictEqual(new_approval_data, subset_json_response)

        # validate errors for post request with missing data
        # with self.assertRaises(ValidationError):
        with self.assertRaises(Exception):
            self.client.post("approval/444")

    def test_delete_approval(self):
        # delete request
        response = self.client.delete(
            '/approval/{id_num}'.format(id_num=self.id_num_to_delete))
        # check that the approval was deleted
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            '/approval/{id_num}'.format(id_num=self.id_num_to_delete))
        self.assertEqual(response.status_code, 404)

        # delete request for approval that is not exists
        response = self.client.delete(
            '/approval/{id_num}'.format(id_num=self.id_num_to_delete))
        # check error
        self.assertEqual(response.status_code, 404)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['error'],
                         'The requested id_num does not exist')


if __name__ == "__main__":
    unittest.main()