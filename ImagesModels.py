from mongoengine import Document,fields


class Images(Document):
    user_id=fields.StringField(required=True)
    email=fields.StringField(required=True)
    image = fields.ImageField(thumbnail_size=(400,400,False))






