"""
MIT License

Copyright (c) 2022 Vad Nik (https://github.com/vadniks)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from threading import Thread
from queue import SimpleQueue
from typing import Callable, Tuple, List, Any
from overrides import overrides
from sync import NUM_UNDEF, THRESHOLD
from time import time, sleep


class TaskExecutor(Thread): #  id    task     argument
    _queue: SimpleQueue[Tuple[int, Callable, Any | None]]
    _canRun: bool #    id status result
    _tasks: List[Tuple[int, bool, Any]]

    def __init__(S):
        super().__init__()
        S._queue = SimpleQueue()
        S._canRun = True
        S._tasks = []

    def doPost(S,
        gonnaWaitForResult: bool,
        task: Callable,
        arg: Any | None
    ) -> int:
        if gonnaWaitForResult:
            _id: int = round(time() * 1000)
            S._tasks.append((_id, False, None))
        else: _id = NUM_UNDEF

        S._queue.put((_id, task, arg))
        return _id

    def _getTask(S, _id: int) -> int: # index
        for j, i in enumerate(S._tasks):
            if i[0] == _id: return j
        return -1

    @overrides
    def run(S) -> None:
        while S._canRun:
            if not S._queue.empty():
                _id, task, arg = S._queue.get()

                if (index := S._getTask(_id)) >= 0:
                    S._tasks[index] = (_id, True, task(arg))
                else: task(arg)
            sleep(THRESHOLD)

    def checkTask(S, _id: int) -> Any:
        if not (task := S._tasks[S._getTask(_id)])[1]:
            return None
        S._tasks.remove(task)
        return task[2]

    def end(S):
        S._canRun = False
