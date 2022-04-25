from threading import Thread
from queue import SimpleQueue
from typing import Callable, Optional, Tuple, List, Any
from overrides import overrides
from sync import NUM_UNDEF, THRESHOLD
from time import time, sleep


class TaskExecutor(Thread): #  id    task  argument
    _queue: SimpleQueue[Tuple[int, Callable, Any]]
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
            sleep(THRESHOLD)

    def checkTask(S, _id: int) -> Any:
        if not (task := S._tasks[S._getTask(_id)])[1]:
            return None
        S._tasks.remove(task)
        return task[2]

    @overrides
    def join(S, timeout: Optional[float] = ...) -> None:
        S._canRun = False
