import ast

import astpretty

from parser_traverse import trsverse_test   #调用抽象语法树遍历类
"""
主要参数说明：
formal_name:func_def内形参列表
value:用于保存对应func_def内形参列表的值
"""
def parse(func_def: ast.FunctionDef, func_expr: ast.Expr) -> None:
    assert isinstance(func_expr.value, ast.Call), "ast.Call Node"

    ##### 在这里实现你的逻辑
    formal_name = []        # func_def内形参列表
    value = []      # 用于保存对应func_def内形参列表的值


    # 首先进行判断此函数是否需要传入参数，即args、vararg、kwarg中至少一个不为空
    if func_def.args.args or func_def.args.vararg or func_def.args.kwarg:

        ### 下列过程仅为提取出形参列表以供后用，提取顺序为一般形参，可变位置参数，可变关键字参数：
        # 提取一般形参
        # 此处i为一个1个节点，需再往下一层进arg得到形参名
        if func_def.args.args:
            for i in func_def.args.args:
                formal_name.append(i.arg)       # 存入formal_name中
        # 提取可变位置参数名
        if func_def.args.vararg:
            formal_name.append(func_def.args.vararg.arg)        # 存入formal_name中
        # 提取可变关键字参数名
        if func_def.args.kwarg:
            formal_name.append(func_def.args.kwarg.arg)     # 存入formal_name中
        # print(formal_name)# 测试输出

        ### 整个传入过程分为是否有可变位置参数存在
        # 若有可变位置参数存在，则在可变位置参数前必没有关键字参数
        # 因此判断为干扰项，进行分开实现

        # 若有可变位置参数,则判断较为简单，若有关键字参数则必为可变关键字参数，否则报错
        # 且由于可变位置参数存在，默认值参数是否存在无关紧要
        # 若有可变位置参数
        if func_def.args.vararg:
            k = len(func_def.args.args)     # k设为形参列表内一般参数的数量，使用k进行传入参数控制
            l = []      # 使用l保存可变位置参数的元素
            for i in func_expr.value.args:
                # 当k为零时，则说明一般参数的值传入完毕，则将后续位置参数值传入l中
                if k == 0:
                    l.append(i.value)
                # k不为0，一般参数的值传入未全部完成，则直接存入value中
                else:
                    value.append(i.value)
                    k-=1
            # print(l)      # 输出测试
            # 由于此过程必有可变位置参数，无需判断l是否为空
            # 将l转为元组类型存入value中
            value.append(tuple(l))
            # print(value)      # 输出测试

            # 进行关键字参数和可变关键字参数判断，都存在时程序启动
            if func_expr.value.keywords and func_def.args.kwarg:
                # 可变关键字参数为字典类型，因此先建立一个字典
                m = {}
                for i in func_expr.value.keywords:
                    m[i.arg] = i.value.value
                # print(m)        # 输出测试
                value.append(m)     # 将m存入value中
                # print(value)        # 输出测试
            else:
                assert not (func_expr.value.keywords and (not func_def.args.kwarg)), "TypeError"
            print("形参名列表：", formal_name)        # 打印输出
            print("传入值列表：", value)        # 打印输出


        # 若无可变位置参数
        else:
            ## 由于没有可变位置参数干扰，如果位置参数存在，可以直接传入位置参数
            ## 直接按顺序导入至value中
            # if func_expr.value.args:
            #     for i in func_expr.value.args:
            #         value.append(i.value)#存入value中
            #     print(value)

            # 若有可变关键字参数,无需进行默认值参数判断
            if func_def.args.kwarg:
                # 先直接判断是否有位置参数，然后按顺序导入至value中
                if func_expr.value.args:
                    for i in func_expr.value.args:
                        value.append(i.value)  # 存入value中
                    # print(value)        # 输出测试
                # 使用k保存位置参数数量
                k = len(func_expr.value.args)
                # 使用l保存形参总数量
                l = len(formal_name)
                # 后先使用字典j保存一般关键字参数的arg和value
                j = {}
                for i in func_expr.value.keywords[0:l-1-k]:
                    j[i.arg] = i.value.value
                # print(j)        #输出测试
                # 以形参名为关键字，按形参顺序导入实参值
                for i in range(k, l-1):
                    value.append(j[formal_name[i]])
                # print(value)        #输出测试
                # 再使用字典m 保存可变关键字参数的arg和value
                m = {}
                for i in func_expr.value.keywords[l-1-k:]:
                    m[i.arg] = i.value.value
                value.append(m)
                print("形参名列表：", formal_name)        # 打印输出
                print("传入值列表：", value)        # 打印输出


            # 没有可变关键字参数时
            else:
                # 有关键字参数时,无需进行默认值参数判断
                if func_expr.value.keywords:
                    # 先直接判断是否有位置参数，然后按顺序导入至value中
                    if func_expr.value.args:
                        for i in func_expr.value.args:
                            value.append(i.value)  # 存入value中
                        # print(value)        # 输出测试
                    #后先使用字典j保存关键字参数的arg和value
                    j={}
                    for i in func_expr.value.keywords:
                        j[i.arg] = i.value.value
                    # print(j)        #输出测试
                    #使用k保存位置参数数量
                    k = len(func_expr.value.args)
                    #使用l保存形参总数量
                    l = len(formal_name)
                    #以形参名为关键字，按形参顺序导入实参值
                    for i in range( k, l):
                        value.append(j[formal_name[i]])
                    print("形参名列表：", formal_name)
                    print("传入值列表：", value)

                # 没有关键字参数时，需要进行默认值参数判断
                else:
                    # 先直接判断是否有位置参数，然后按顺序导入至value中
                    if func_expr.value.args:
                        for i in func_expr.value.args:
                            value.append(i.value)# 存入value中
                        # print(value)        # 输出测试
                        # 判断默认值参数是否应该导入列表
                        # 由于无可变参数类型，实参与形参都为一一对应
                        # 当实参数量少于形参数量时，需要导入默认值参数值
                        # j为实参数量
                        j = len(func_expr.value.args)
                        # k为形参数量
                        k = len(func_def.args.args)
                        # 进行是否缺少传入参数判断
                        if j < k:
                            # 缺少时，进行默认值参数补充，补充数量为（k-j）个，即传入defaults的后(k-j)个
                            for i in func_def.args.defaults[j-k:]:
                                value.append(i.value)
                            assert k-j <= len(func_def.args.defaults), "TypeError"
                        print("形参名列表：", formal_name)        # 打印输出
                        print("传入值列表：", value)        # 打印输出


    # 如果形参列表为空，则进行是否有实参传入判断，若有则进行警告
    else:
        assert not func_expr.value.args and not func_expr.value.keywords, "TypeError:{:}() does not require incoming parameters".format(
            func_def.name)

