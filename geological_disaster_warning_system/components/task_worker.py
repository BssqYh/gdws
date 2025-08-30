# task_worker.py

from PySide6.QtCore import QThread, Signal


"""
任务队列：
当需要执行数据库等一些耗时操作的时候使用。
使用方法：创建、设置任务、设置结束时候左什么、start开始任务
worker = TaskWorker(self)
worker.set_task(lambda: self.save_all(data, self.work_point_id))
self.worker.finished.connect(self.on_save_done)
worker.start()

----
on_save_done
save_all 
都是调用的地方需要实现的。
"""

class TaskWorker(QThread):
    """
    通用后台任务执行器
    支持设置任意函数作为任务，并在完成时触发回调（主线程中执行）
    """
    finished = Signal(object)        # 返回结果
    error = Signal(str)              # 错误信息
    _instance_counter = 0

    def __init__(self, parent=None):
        super().__init__(parent=None)
        self._task_func = None
        self._result = None
        self._callback = None

        # # 绑定默认信号处理
        # self.finished.connect(self._on_finished)
        # self.error.connect(self._on_error)

    def set_task(self, func):
        """
        设置要执行的任务函数
        :param func: callable, 无参数函数，如: lambda: do_something(a, b)
        """
        self._task_func = func
        return self  # 支持链式调用

    def set_callback(self, callback):
        """
        设置任务成功后的回调函数（在主线程执行）
        :param callback: callable, 接收一个参数：return value of task
        """
        self._callback = callback
        return self

    def set_errback(self, errback):
        """
        设置错误回调（可选）
        :param errback: callable, 接收错误消息字符串
        """
        self._errback = errback
        return self

    def run(self):
        """QThread 的 run 方法，在子线程中执行"""
        if not self._task_func:
            self.error.emit("未设置任务函数")
            return
        try:

            result = self._task_func()

            self.finished.emit(result)

        except Exception as e:
            import traceback
            traceback.print_exc()
            self.error.emit(str(e))