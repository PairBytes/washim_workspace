from bson.objectid import ObjectId


class Base_Mongo(object):
    def find_one(self, query, projection=None):
        """
        :desscription: returns the first document that satisfies the specified query criteria
        :param query: the query dict. example query = {'t1':'new'}
        :param projection: a list of fields to return. returns all the fields by default
        """
        return self.collection.find_one(query, projection)
    
    def update(self, query, update, upsert=False):
        """
        :description: Update a single document matching the filter.
        :param query: the query dict. example query = {'t1':'new'}
        :param update: the update dictionary. example update = {'t1':'e2'}

        """
        fUpdate = {"$set": update}
        return self.collection.update_one(query, fUpdate, upsert)

    def insert(self, docu):
        """
        :description: inserts a new document in the collection
        :param docu: the document to be inserted. example docu = {'t1':'e2'}

        """
        _id = self.collection.insert_one(docu)
        return _id