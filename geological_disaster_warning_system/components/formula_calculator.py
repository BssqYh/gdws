import logging
import re
import json
from PySide6.QtCore import QFile, QIODevice
import os
from pathlib import Path
import compiled_resources
from PySide6.QtCore import QFile, QTextStream
from asteval import Interpreter, make_symbol_table
import math

math_funcs = {
    'sqrt': math.sqrt, 'log': math.log, 'log10': math.log10,
    'log2': math.log2, 'exp': math.exp, 'sin': math.sin,
    'cos': math.cos, 'tan': math.tan, 'floor': math.floor,
    'ceil': math.ceil, 'abs': abs, 'pow': pow, 'pi': math.pi,
    'e': math.e, 'tau': math.tau, 'inf': float('inf'), 'nan': float('nan'),
    'max': max,
    'min': min,
}

# ================== 加载变量映射表 ==================
def _load_replacements_from_resource(resource_path: str) -> dict:
    """
    从 Qt 资源系统（qrc）中加载 JSON 配置（兼容 PySide6 所有版本）
    resource_path: 如 ":/resources/variables.json"
    """
    file = QFile(resource_path)

    if not file.exists():
        raise FileNotFoundError(f"资源文件未找到: {resource_path}")

    if not file.open(QIODevice.ReadOnly | QIODevice.Text):
        raise RuntimeError(f"无法打开资源文件: {resource_path}")

    # 读取全部内容为 QByteArray，然后解码为 UTF-8 字符串
    data = file.readAll()
    content = str(data, 'utf-8')  # PySide6: QByteArray 转 str
    file.close()

    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON 解析失败: {e}")

    replacements = {}
    for item in data.get("variables", []):
        raw = item["raw"]
        safe = item["safe"]
        if not safe.isidentifier():
            raise ValueError(f"安全变量名不合法（非标识符）: {safe}")
        replacements[raw] = safe

    return replacements
# 全局变量映射表
REPLACEMENTS = _load_replacements_from_resource(":/resources/variables.json")

# ================== 构建正则匹配器 ==================
_sorted_vars = sorted(REPLACEMENTS.keys(), key=lambda x: len(x), reverse=True)
_escaped_vars = [re.escape(var) for var in _sorted_vars]
VARIABLE_PATTERN = '|'.join(_escaped_vars)
VAR_REGEX = re.compile(VARIABLE_PATTERN)

# ================== FormulaCalculator 类 ==================
class FormulaCalculator:
    def __init__(self):
        symtable = make_symbol_table()
        symtable.update(math_funcs)
        self.interpreter = Interpreter(symtable=symtable)
        self.last_error = None

    def evaluate(self, formula: str, **variables):
        self.last_error = None
        self.interpreter.symtable.update(variables)
        try:
            result = self.interpreter(formula.strip())
            if self.interpreter.error:
                err = self.interpreter.error
                msg = f"{err.get('error', '')}: {err.get('message', '')}"
                self.last_error = msg
                raise ValueError(msg)
            return float(result)
        except Exception as e:
            self.last_error = str(e)
            raise ValueError(f"计算失败: {e}")

    def get_error(self):
        return self.last_error


_calculator = FormulaCalculator()

# ================== 提取变量名 ==================
def extract_variables(formula: str) -> dict[str, str]:
    """
    从公式中提取变量，返回字典：{raw_name: safe_name, ...}
    按变量在公式中首次出现的顺序排列（Python 3.7+ dict 保持插入顺序）

    示例：
        extract_variables("I₅,₁₀ + α₁")
        → {'I₅,₁₀': 'i_5_10', 'α₁': 'alpha_1'}
    """
    found_raw_vars = VAR_REGEX.findall(formula)

    seen = set()
    mapping = {}
    for raw in found_raw_vars:
        # 跳过未声明变量（理论上不会发生）
        if raw not in REPLACEMENTS:
            continue
        # 跳过重复
        if raw in seen:
            continue
        seen.add(raw)
        mapping[raw] = REPLACEMENTS[raw]  # raw → safe

    return mapping

# ================== 计算公式 ==================
def calc_formula(formula: str, **inputs):
    """
    计算公式，所有变量必须在 resources/variables.json 中定义。
    """
    used_raw_to_safe = extract_variables(formula)
    if not used_raw_to_safe:
        try:
            return _calculator.evaluate(formula)
        except Exception as e:
            raise logging.error(f"无效公式或缺少变量: {formula}") from e

    # 检查是否有未声明的变量（理论上 extract_variables 已过滤，可选）
    unknown_vars = [v for v in used_raw_to_safe if v not in REPLACEMENTS]
    if unknown_vars:
        raise logging.error(f"以下变量未在 variables.json 中定义: {unknown_vars}")

    # 替换原始变量名为安全变量名
    safe_formula = formula
    for raw_var, safe_var in used_raw_to_safe.items():
        safe_formula = safe_formula.replace(raw_var, safe_var)

    # 获取需要传入的变量名（safe 名）
    required_safe_vars = list(used_raw_to_safe.values())
    missing = [var for var in required_safe_vars if var not in inputs]
    if missing:
        raise logging.error(f"缺少输入变量: {missing}")

    logging.info(f"开始计算---公式：{safe_formula}--值：{inputs}")

    try:
        result = _calculator.evaluate(safe_formula, **inputs)
        return result
    except Exception as e:
        raise logging.error(f"公式计算失败: {e}\n公式: {safe_formula}")
