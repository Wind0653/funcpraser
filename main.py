import argparse
import ast
import os.path
from pathlib import Path

#
import astpretty
# 引入参数解析模块
import funcparser

# 创建一个参数解析器
parser = argparse.ArgumentParser(prog="parser", description="A trivial function parser")
# 要求输入具有一个参数 file
parser.add_argument("file")

if __name__ == "__main__":
    # 解析命令行参数
    args = parser.parse_args()
    # 得到参数file对应的值
    parsed_file = args.file

    # 检测是不是一个文件
    is_file = os.path.isfile(parsed_file)
    assert is_file, "the file is really a file"
    # 检测是不是一个Python文件
    is_python_file = Path(parsed_file).suffix == ".py"
    assert is_python_file, "the file is really a Python file"

    # with管理打开文件的上下文
    with open(parsed_file, "r") as f:
        # 解析的Python文件是一个模块
        abstract_syntax_tree: ast.Module = ast.parse(f.read())
        # 要求此模块抽象语法树具有两个节点，一个函数定义，一个函数调用
        assert len(abstract_syntax_tree.body) == 2, "Two AST nodes"
        func_def = abstract_syntax_tree.body[0]
        assert isinstance(func_def, ast.FunctionDef), "ast.FunctionDef Node"
        # 格式化打印
        astpretty.pprint(func_def)
        func_call = abstract_syntax_tree.body[1]
        assert isinstance(func_call, ast.Expr), "ast.Expr Node"
        # 格式化打印
        astpretty.pprint(func_call)

        # 正式开始解析
        funcparser.parse(func_def, func_call)
