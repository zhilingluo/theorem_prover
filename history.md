## 2025-1-5

从matrixcookbook的lean项目和陶哲轩的素数定理来看
1. 构造证明能完成的只是整个数学体系中一小部分,剩下的大部分要么没有被formalize成构造类型的定理,要么缺失证明,后者很可怕,前者更可怕
2. 证明相比,前者易于验证,可以直接检查结果.后者难以验证,定理证明辅助工具大概就是为数不多的验证方法了. 前者对于数学体系的进步帮助有限, 后者帮助很大. 而且定理证明的方式中,通过计算来证明也是一种有趣的方式
3. lean4和coq是仅存的定理证明工具了,他们俩都有一个非常有挑战性的点,就是对当前定理的证明中往往需要从过去的定理中找到可以用的,这就需要记住(或者搜索)那些已有的定理.找到之后还需要尝试(所以是交互性的)
4. LLM在此场景中重要的不是记住了什么定理和推理方式,而是需要从动态的定理库中发现和使用必要的定理参与证明.
5. 此处可能有一种负面效应,就是随着定理库的扩充,证明下一个定理的难度未必是降低了
6. 这个task有一个很有趣的好处,就是他重要的是结果,而非方法.换言之只要得到了证明过程,这就是伟大的成果,不需要考虑得到一个方法,然后看其泛化性.

Lean4的语法非常不稳定,跟lean3很不兼容,llm很容易误使用lean3的语法,比如begin end

## 2025-1-7

Lean-dojo提供了一个对github上的lean项目集成推理的环境

internLM使用lean-dojo封装了一个使用LLM参与搜索推理的方案

Minif2f提供了数据集,

Leanworkbook 提供了一种利用LLM去将question转化为lean4的方法,然后在再回来,然后再由LLM评估其是否一致

## 2025-1-8

参考书生internLM-math的proofsearch,

引入qwenmax作为基础LLM

遇到了一个问题:接口调用的LLM无法获得loglikelihood,这玩意儿只有走GPU本机部署调用比如vllm才有,先设置为一个常数

另一个问题是lean-dojo的constants.py中会检查git的版本,这个在我本机window上会报错,所以可以注释掉 

    #check_git_version((2, 25, 0))

lean-dojo的init也有一个跟windows不兼容的部分,也可以通过注释解决

    #if os.geteuid() == 0:
    #    raise RuntimeError("LeanDojo should not be run as root.")

lean-dojo 还会遇到超时的问题

    Request GET /repositories/129571436/branches?page=48 failed with 403: rate limit exceeded
    Setting next backoff to 406.606571s

这玩意儿总是连接github也是醉了

又一个错误

    Traceback (most recent call last):
      File "E:\PY39\lib\encodings\idna.py", line 165, in encode
        raise UnicodeError("label empty or too long")
    UnicodeError: label empty or too long

我打算改造lean-dojo成本地的...需要些日子
