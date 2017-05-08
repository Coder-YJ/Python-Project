#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# build in 2017/5/8 by QianYuanJing
from orm import Model,StringField,IntegerField

class User(Model):
    __table__ = 'users'
    
    id = IntegerField(primary_key=True)
    name = StringField()
    
class Model(dict,metaclass=ModelMetaclass):

        def __init__(self,**kw)
            super(Model,self).__init__(**kw)
        
        def __getattr__(self,key):
            try:
                return self[key]
            excepr KeyError:
                raise ArithmeticError(r"'Model' object has no attribute '%s' " %key)
        
        def __setattr__(self,key,value):
            self[key] = value
            
        def getValue(self,key,None)
            value = getattr(self,key,None)
            if value is None:
                field = self.__mappings__[key]
                if field.default is not None:
                    value = field.default() if callable(field.default) else field.default
                    logging.debug('using default value for %s: %s' % (key,str(value)))
            return value