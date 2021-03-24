
import linkdisksappp


class users(linkdisksappp.db.Document):

    user_id=linkdisksappp.db.StringField(unique=True,required=True)
    size = linkdisksappp.db.StringField(required=True)
    email=linkdisksappp.db.StringField(unique=True,required=True)
    pass_code=linkdisksappp.db.StringField(required=True)
    admin=linkdisksappp.db.BooleanField(required=True)

    def to_json(self):
        #convert this document to json
        return {
            "user_id":self.user_id,
            "size":self.size,
            "email":self.email,
            "pass_code":self.pass_code,
            "admin":self.admin
        }
