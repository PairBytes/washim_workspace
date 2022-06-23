from bson.json_util import dumps
from bson.objectid import ObjectId


class RestResponse:

    def __init__(self, data={}, status=0, message="", err="", next_offset=None, limit=None, total=None, page=None):
        """
        :param data: Response data of Rest call.
        :param status: Response status of Rest call , default is 1 means success.
        :param messages: Response message of Rest call , default is None.
        """
        self.__entity = {}
        self.__entity['data'] = data
        self.__entity['status'] = status
        self.__entity['message'] = message
        self.__entity['err'] = err
        if next_offset is not None:
            self.__entity['next_offset'] = next_offset
        if limit is not None:
            self.__entity['limit'] = limit
        if total is not None:
            self.__entity['total'] = total
        if page is not None:
            self.__entity['page'] = page

    def to_json(self):
        """
        :return json-object.
        """
        if '_id' in self.__entity['data'] and isinstance(self.__entity['data']['_id'], ObjectId):
            self.__entity['data']['_id'] = str(self.__entity['data']['_id'])
        if 'created_at' in self.__entity['data']:
            if self.__entity['data']['created_at'] and type(self.__entity['data']['created_at']) != str:
                self.__entity['data']['created_at'] = self.__entity['data']['created_at'].strftime(
                    "%Y-%m-%dT%H:%M:%S.000Z")
            else:
                self.__entity['data']['created_at'] = self.__entity['data']['created_at']
        if 'updated_at' in self.__entity['data']:
            if self.__entity['data']['updated_at'] and type(self.__entity['data']['updated_at']) != str:
                self.__entity['data']['updated_at'] = self.__entity['data']['updated_at'].strftime(
                    "%Y-%m-%dT%H:%M:%S.000Z")
            else:
                self.__entity['data']['updated_at'] = self.__entity['data']['updated_at']
        return self.__entity
