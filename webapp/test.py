#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# build in 2017/5/8 by QianYuanJing
import orm,asyncio
from models import User, Blog, Comment

async def test(loop):

    await orm.create_pool(loop=loop,host='127.0.0.1',user='root', password='qianyuanjing', database='awesome')
    u = User(name='qyj', email='qyj@example.com', passwd='0987654321', image='about:blank')
    await u.save()

loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
loop.close()
