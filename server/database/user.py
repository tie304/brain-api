from pymodm import connect, fields, MongoModel, EmbeddedMongoModel




# Now let's define some Models.
class User(MongoModel):
    # Use 'email' as the '_id' field in MongoDB.
    email = fields.EmailField(primary_key=True)
    name = fields.CharField()
    password = fields.CharField()
