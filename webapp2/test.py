#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# build in 2017/5/8 by QianYuanJing
import orm,asyncio
from models import User, Blog, Comment

@asyncio.coroutine
def test(loop):

    yield from orm.create_pool(loop,user='qianyuanjing', password='qianyuanjing', database='mysql')
    u = User(name='qyj', email='qyj@example.com', passwd='0987654321', image='about:blank')
    yield from u.save()

loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
loop.close()
