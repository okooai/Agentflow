import upyog as upy

class BaseModel(upy.BaseObject):
    def __init__(self, *args, **kwargs):
        super_ = super(BaseModel, self)
        super_.__init__(*args, **kwargs)