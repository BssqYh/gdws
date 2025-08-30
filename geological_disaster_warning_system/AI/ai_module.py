import dashscope
from dashscope import Generation
import json
from PySide6.QtCore import QObject, Signal, QTimer, QMutex


class AIEvaluationModule(QObject):
    evaluation_finished = Signal(dict)  # 返回评价文本
    evaluation_stopped = Signal()     # 请求被手动停止

    _instance = None
    _mutex = QMutex()

    def __new__(cls, *args, **kwargs):
        """实现线程安全的单例"""
        cls._mutex.lock()
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        cls._mutex.unlock()
        return cls._instance

    def __init__(self, parent=None):
        if hasattr(self, '_initialized'):
            return
        super().__init__(parent)
        """暂时使用这种方式"""
        self._api_key = "sk-1b7e6e0cc92441fab8105e5cad233d29"
        dashscope.api_key = self._api_key
        self._criteria = {}
        self._current_request_active = False
        self._typing_text = ""
        self._score = ""
        self._typing_index = 0
        self._evaluation_widget = None
        self._typing_timer = QTimer()
        self._typing_timer.timeout.connect(self._type_character)

    def initialize(self, api_key):
        """初始化方法，用于设置 API Key（仅需调用一次）"""

        if not self._api_key:
            dashscope.api_key = api_key
            self._api_key = api_key
        print(f"ai model initialize-----{ self._api_key}")

    def set_criteria(self, criteria):
        """外部传入分级标准"""
        """必须调用如果不调用，那么就会造成分析错误。格式如下：
        criteria = [
    {
        "分级标准": "坡形为凹地形；地面相对高差>200m；地面坡度>25°为主；植被覆盖度低，坡面裸露；",
        "分值范围": "70-100"
    },
    {
        "分级标准": "坡形为凸地形；地面相对高差50m～200m；地面坡度8~25°为主；植被覆盖度中等，坡面局部裸露；",
        "分值范围": "70-100"
    },
    {
        "分级标准": "坡形为直线型；地面相对高差<50m；地面坡度小于8°；坡面植被覆盖度高；",
        "分值范围": "70-100"
    }
]"""
        self._criteria = criteria

    def build_prompt(self, input_values,user_input_values):

        #criteria_str = ""
        # for idx, item in enumerate(self._criteria, start=1):
        #     criteria_str += f"【等级 {idx}】\n"
        #     criteria_str += f"分级标准: {item['分级标准']}\n"
        #     criteria_str += f"分值范围: {item['分值范围']}\n\n"
        prompt = f"""
你是地质灾害风险评估专家，请根据以下分级标准和输入指标值进行评估：

【分级标准】:
{self._criteria}

【用户额外要求】:
{user_input_values}

【输入指标值】:
{input_values}
请以如下 JSON 格式输出你的判断结果，不要添加额外解释,不要在评级结果里面使用分级标准的内容，不要出现等级字眼：
[
    {{"指标评价": "具体评价内容"}},
    {{"建议得分": "具体的得分"}}
]
"""
        return prompt

    def call_qwen(self, prompt):
        try:
            response = Generation.call(
                model='qwen-max',
                prompt=prompt
            )
            return response.output.text.strip()
        except Exception as e:
            return json.dumps([{"指标评价": f"调用Qwen失败: {str(e)}"}, {"建议得分": "0"}])

    def parse_response(self, response_text):
        try:
            result = json.loads(response_text)
            if isinstance(result, list) and len(result) >= 2:
                evaluation = result[0]["指标评价"]
                score = result[1]["建议得分"]
                return {
                    "指标评价": evaluation,
                    "建议得分": score
                }
            else:
                return {
                    "指标评价": "解析失败",
                    "建议得分": "0"
                }
        except Exception as e:
            return f"JSON 解析错误: {str(e)}"

    def evaluate(self, input_values,user_input_values, widget=None,):
        """主入口方法：启动 AI 分析并显示打字机效果"""
        if not self._api_key:
            raise RuntimeError("AI 模块未初始化，请先调用 initialize(api_key)")

        if not self._criteria:
            raise ValueError("未设置分级标准 criteria，请先调用 set_criteria()")

        if self._current_request_active:
            self.stop()  # 如果已有请求在进行，先停止

        self._current_request_active = True
        self._typing_widget = widget
        self._typing_index = 0

        prompt = self.build_prompt(input_values,user_input_values)
        print(f"<UNK>{prompt}<UNK>")
        QTimer.singleShot(0, lambda: self._async_call_qwen(prompt))

    def _async_call_qwen(self, prompt):
        """异步调用 Qwen 避免阻塞主线程"""
        try:
            raw_response = self.call_qwen(prompt)
            result = self.parse_response(raw_response)
            # print("评价内容:", result["指标评价"])
            # print("建议得分:", result["建议得分"])
            self._typing_text = result["指标评价"]
            self._score = result["建议得分"]
            self._start_typing_effect()
        except Exception as e:
            self.evaluation_finished.emit({
                "指标评价": f"发生错误：{e}",
                "建议得分": "0"
            })
        finally:
            self._current_request_active = False

    def _start_typing_effect(self):
        """启动打字机动画"""
        if not self._evaluation_widget:
            full_result = {
                "指标评价": self._typing_text,
                "建议得分": self._score
            }
            self.evaluation_finished.emit(full_result)
            return
        self._evaluation_widget.setText("")  # 清空旧内容
        self._typing_index = 0  # 确保索引重置
        self._typing_timer.start(80)  # 每 80ms 显示一个字符

    def _type_character(self):
        if self._typing_index < len(self._typing_text):
            self._evaluation_widget.setText(
                self._evaluation_widget.text() + self._typing_text[self._typing_index]
            )
            self._typing_index += 1
        else:
            self._typing_timer.stop()
            full_result = {
                "指标评价": self._typing_text,
                "建议得分": self._score
            }
            print(f"------------<UNK>{full_result}<UNK>")
            self.evaluation_finished.emit(full_result)

    def stop(self):
        """停止当前请求和动画"""
        if self._current_request_active:
            self._current_request_active = False
            self._typing_timer.stop()
            self.evaluation_stopped.emit()