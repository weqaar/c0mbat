# -*- coding: utf-8 -*-

import packages.globalvars as globalvars
import multiprocessing


class _init_queues():

    def __init__(self):
        #Initialize Queue0|Topic0
        globalvars._mp_queue0 = multiprocessing.Queue()
        #Initialize Queue1|Topic1
        globalvars._mp_queue1 = multiprocessing.Queue()

    def get(self, _mp_queue):
        return _mp_queue.get()

    def put(self, _mp_queue, item):
        return _mp_queue.put(item)

    def empty(self, _mp_queue):
        return _mp_queue.empty()

