
from mongoengine.document import Document
from mongoengine.fields import DateTimeField, StringField, EmailField,BooleanField


class users(Document):

    user_id=StringField(unique=True,required=True)
    size = StringField(required=True)
    email=StringField(unique=True,required=True)
    pass_code=StringField(required=True)
    admin=BooleanField(required=True)

    def to_json(self):
        #convert this document to json
        return {
            "user_id":self.user_id,
            "size":self.size,
            "email":self.email,
            "pass_code":self.pass_code,
            "admin":self.admin
        }


