#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# build in 2017/5/8 by QianYuanJing
from orm import Model,StringField,IntegerField

@asyncio.coroutine
def create_pool(loop,**kw):
    logging.info('Create database connection pool...')
    global __poll
    __poll = yield from aiomysql.create_pool(
    host=kw.get('host','localhost'),
    port=kw.get('port',3306),
    user=kw['user'],
    password=kw['password'],
    db=kw['db'],
    charset=kw.get('charset','utf8'),
    autocommit=kw.get('cutocommit',True),
    maxsize=kw.get('maxsize',10),
    minsize=kw.get('minsize',1),
    loop=loop
    )
  
@asyncio.coroutine
def select(sql,args,size=None):
    log(sql,args)
    global __poll
    with (yield from __poll) as conn:
        cur = yield from conn.cursor(aiomysql.DictCursor)
        yield from cur.execute(sql.replace('?','%s'),args or ())
        if size:
            rs = yield from cur.fetchmany(size)
        else:
            rs = yield from cur.fetchall()
        yield from cur.close()
        logging.info('rows return:%s'% len(rs))
        return rs
        
@asyncio.coroutine
def excute(sql,args):
    log(sql)
    with (yield from __pool) as conn:
        try:
            cur = yield from conn.cursor()
            yield from cur.excute(sql.replace('?','%s'),args)
            affected = cur.rowcount
            yield from cur.close()
        except BaseException as e:
            raise
        return affected

    
class Model(dict,metaclass=ModelMetaclass):

        def __init__(self,**kw):
            super(Model,self).__init__(**kw)        
        def __getattr__(self,key):
            try:
                return self[key]
            except KeyError:
                raise ArithmeticError(r"'Model' object has no attribute '%s' " %key)
        
        def __setattr__(self,key,value):
            self[key] = value
           
        def getValue(self,key):
            return getattr(self,key,None)
            
        def getValueOrDefault(self,key):
            value = getattr(self,key,None)
            if value is None:
                field = self.__mappings__[key]
                if field.default is not None:
                    value = field.default() if callable(field.default) else field.default
                    logging.debug('using default value for %s: %s' % (key,str(value)))
            return value
            
        @classmethod
        @asyncio.coroutine
        def find(cls,pk):
            'find object by primary key'
            rs = yield from select('%s where `%s`=?'%(cls.__select__,cls.__primary_key__),[pk],1)
            if les(rs) == 0:
                return None
            return clls(**rs[0])
         
        @asyncio.coroutine
        def save(self):
            args = list(map(self.getValueOrDefault,self.__fields__))
            args.append(self.getValueOrDefaultDefault(self.__primary_key__))
            rows = yield from excute(self.__insert__,args)
            if rows != 1:
                logging.warn('Faild to insert record: affected rows：%s'% rows)
            
    
    
class Field(object):
    
    def __init__(self,name,column_type,primary_key,default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default
        
    def __str__(self):
        return '(%s,%s:%s)'%(self.__class__.__name__,self.column_type,self.name)
        

class StringField(Field):
    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        super().__init__(name,ddl,primary_key,default)
        
class ModelMetaclass(type):
 
    def __new__(cls,name,bases,attrs):
        #删除Model本身
        if name=='Model':
            return type.__new__(cls,name,bases,attrs)
        #获取table名称
        tableName= attrs.get('__table__',None) or name
        logging.info('found model: %s (table: %s)'%(name,tableName))
        #获取所有的Field和主键名
        mappings = dict()
        fields = []
        primaryKey = None
        for k,v in attrs.items():
            if isinstance(v,Field):
                logging.info("  found mapping: %s ==> %s"%(k,v))
                if v.primary_key:
                    #找到主键
                    if primaryKey:
                        raise RuntimeError('Duplicate primary key for field: %s'%k)
                    primaryKey = k
                else:
                    fields.append(k)
        
        if not primaryKey:
            raise RuntimeError('Primary key not found')
        for k in mappings.keys():
            attrs.pop(k)
        escaped_ields = list(map(lambda f:  '`%s`'% f,fields))
        attrs['__mappings__'] = mappings #保存属性和列的映射关系
        attrs['__table__'] = tableName
        attrs['__primary_key__'] = primaryKey #主键和属性名
        attrs['__fields__'] = fields
        #构建默认的SELECT,INSERT,UPDATE和DELETE语句
        attrs['__select__'] =  'select `%s`, %s from `%s`'%(primaryKey,','.join(escaped_ields),tableName)
        attrs['__insert__'] = 'insert into `%s` (%s,`%s`) values (%s)'%(tableName, ','.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1))
        attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey)
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tableName, primaryKey)            
        return type.__new__(cls, name, bases, attrs)
            