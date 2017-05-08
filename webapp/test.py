#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# build in 2017/5/8 by QianYuanJing
import orm
from model import User,Blog,Comment

def test():
    yield from orm.create_pool(user='www-data',password='www-data',database='awesome')
    
    u = User(name='Test', email='test@example.com', passwd='1234567890',image='about:blank')
    
    yield from u.save()
    
for x in test():
        pass
