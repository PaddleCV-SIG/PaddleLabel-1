from marshmallow import fields


from pplabel.api.model import Annotation
from .base import BaseSchema


class AnnotationSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Annotation

    project_id = fields.Integer()
    # task = fields.Nested("TaskSchema", exclude=("annotations", "datas"))
    label = fields.Nested("LabelSchema")
