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

## 2025-1-9

我在LeanDojo上提问了 https://github.com/lean-dojo/LeanDojo/discussions/219

翻了一下LeanDojo的文档，他们也给社区贡献了一些定理的证明，It discovers [33 proofs in miniF2F](https://github.com/facebookresearch/miniF2F/pull/13) and [39 proofs in ProofNet](https://github.com/zhangir-azerbayev/ProofNet/pull/14) 

我注意到leandojo实际上是重点提供了一个docker,然后在里面做lean的事情,其实如果在native的环境下,会方便很多
大量的leandojo的配置都是linux的,比如并行,在window上无法运行
还有一个ast文件跟库面的冲突,可以rename成ast_new

由于网络太慢,可以自己从github上,拖
1. lean的4.7.0版本,放到 用户/.elan/toolchains/leanprover--lean4---v4.7.0 , 用elan show可以看版本
2. matlib的4.7.0版本,放到.lake里面 https://github.com/leanprover-community/mathlib4/releases/tag/v4.7.0 lake (好像不行)

    
    # following command can replace _trace
    python lean_dojo/data_extraction/build_lean4_repo.py repos/lean-dojo-mew --no-deps
    # 这里面有一个lake build 一个安装matlib，一个拷贝lean的标准库到packages，然后lake env lean --threads 6 --run ExtractData.lean noDeps

它会在initial之后，将目标定理改成 lean_dojo_repl，然后准备一个Lean4Repl.lean文件，然后改了lakefile.lean，在里面加入对这个文件的依赖
    set_option maxHeartbeats 0 in
    theorem imo_1997_p5 (x y : ℕ) (h₀ : 0 < x ∧ 0 < y) (h₁ : x ^ y ^ 2 = y ^ x) :
        (x, y) = (1, 1) ∨ (x, y) = (16, 2) ∨ (x, y) = (27, 3) := 
    by
        lean_dojo_repl
        sorry
这一堆事情其实都应该在一个临时目录中做，不要动原始的repo

## 2025-1-10
我的提问收到的回复 https://github.com/lean-dojo/LeanDojo/pull/179

然而看起来他的修改跟我的类似,还是需要在dojo类做一些改动才行

我的改动已经可以运行了,然而qwenmax只保留了message接口,不太适合目前需要的complete模式,惊讶的是openai的接口里面也删除了complete接口,真是可惜.

message模式调用qwenmax的格式对齐非常糟糕,十个里面只有两三个的格式是对的,我试着增加了一些后处理代码,这也不太靠谱

棒棒的github镜像! https://gitclone.com/  感谢他们
还有这个文件加速 https://ghp.quickso.cn/ 感恩

## 2025-1-11
试用aws的ec服务器,也许访问git会快一些,我顺便记下这一些安装的命令

    # install elan on linux
    curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh

    # install elan on windows
    curl -O --location https://raw.githubusercontent.com/leanprover/elan/master/elan-init.ps1
    powershell -ExecutionPolicy Bypass -f elan-init.ps1
    del elan-init.ps1

    # install python on linux
    sudo yum install python3
    sudo yum install pip3
    
    # install python packages
    pip3 install -r minif2f/requirements.txt

上帝啊,AWS送的机器连接github很快,但是CPU是真的慢啊,一个lake build就很久很久

又回到qwenmax的格式问题了,我设置调用llm 32次, 一个定理需要6min,这是每条都不对的情况,如果有对的,还进一步的探索,时间未知

遇到了一个异常
    requests.exceptions.ProxyError: HTTPSConnectionPool(host='dashscope.aliyuncs.com', port=443): Max retries exceeded with url: /api/v1/services/aigc/text-generation/generation (Caused by ProxyError('Unable to connect to proxy', RemoteDisconnected('Remote end closed connection without response')))

看起来是有一个max retries的限制

我加了一个异常处理

顺便换成了qwen-turbo, 速度变成了 400s一条

## 2025-01-13
用qwen-turbo跑完了miniF2F的Test.lean,总计30个定理,用时2:58:00,其中每个sample32次,其中的到了一个正确的

    theorem mathd_numbertheory_175 : 2 ^ 2010 % 10 = 4:=
    norm_num

这个看似不复杂的证明,貌似之前还没有人提交过

棒棒的,证明这个路子不是死路,而是我们的效率太低,解决效率问题是这个的关键

我打算用vscode验证一下之后提交给 https://github.com/facebookresearch/miniF2F/blob/main/lean/src/test.lean

注意到这是一个lean3的库,而且已经没有新的提交了,看起来这块在lean3上已经没有更新了

将minif2f迁移到lean4 上的git是 https://github.com/yangky11/miniF2F-lean4  

注意到这个git实际上已经变成了一个测试集,没有人提交正确答案

那就先不考虑在这个集子上直接提交了,只拿来测试和优化我的方法吧

## 2025-01-14

现在的重点是需要将后搜索,通过RFT做到模型里面去

目前首要的几个事情是

1. 考虑微调来保证对齐,减少搜索中由于不对齐导致的浪
2. 多生成器多候选,提高多样性

具体而言,我会先参考书生模型的数据构建方式,搞一批微调数据,只需要几百到千级别就可以,训练1-2epoch,基于开源的qwen模型来做

感谢书生提供的训练数据,搞了2w条,我将其加工成jsonl的形态,在qwen上微调,这个任务大概需要一两天(据说这批数据有可能对minif2f的泄露问题,所以也要小心地评估)

同步的,我考虑加入关键的多生成器与多候选搜索,我分几个部分开发

1. 修改bfs中的对llm的调用,转为调用一个虚拟llm,其包含一组模型
2. 在虚拟llm中,增加对deepseek在内的多个模型的调用,产生多候选,每个模型使用的fewshot配置,prompt配置分别做到配置
3. 增加数据收集器,在bfs中,收集数据的正负反馈,将数据写入文件,包含state_before, tactic,state_after, llm,is_correct,is_finish 这几个字段

训练居然只花了几个小时,看起来主要是样本很短的缘故,

在写数据收集器的时候,遇到了一个有趣的事情,就是__del__ 中无法调用open,解决方式是使用atexit

    atexit.register(self.flush)

微调的两个模型,其中qwen 比 qwencoder的ft版本要好些,可能说明咱们这个任务离coder比较远

我把对ft模型的调用改成了多进程

但是我注意到ft模型的多样性好差,开到32的样本,其实都是一样的,temperature对结果的多样性帮助好像不大,可能是部署平台上的temperature没有生效

## 2025-01-15

两个微调模型,32采样,100最大迭代,重跑minif2f,总共花了2消失,做对了13个,总共30个,比率为43%

结果在output/minif2f/14-01-2025-19-57/results__qwenmax__1.json
数据保存在了report_2025-01-14_19-57-07.txt

接下来需要分析

1. 这个多样性的问题,我需要观察虽然有32个sample,但是去重之后剩了几个,我可以画一个直方图或者做一个统计

脚本是analyze_unique_sample.py, 结论是1个的有11个,2个的有36个,3个的有4个,可见实际上采样数量在目前配置下只需要8左右就可以的,32是不太需要的

我将这个参数改成8重新试一下,注意到时间上改变不太明显,大部分的时间都是花在了重新拷贝,lake之类部分,实际上每一次推理的时间都是1-2s,而整个一个定理需要跑近2min,总体上还是需要一个多小时来一次完整的30题

这一次的实验结果一模一样,结果在output/minif2f/15-01-2025-10-49/results__qwenmax__1.json 我的数据记录在report_2025-01-15_10-49-13.txt

这个上的统计结果也和之前一样,说明从32减到8不会有什么影响

我可以修改ft模型的部署中的temperature,这玩意儿之前是0.1,也许是这个参数导致我在调用的时候传入的temperature的0.5并未生效

我试着改了服务器上的这个配置,重启服务,我重启实验

结果还是对了13个,结果在output/minif2f/15-01-2025-13-43/results__qwenmax__1.json  数据在report_2025-01-15_13-43-47.txt

我不信这个邪,我给改成了1,再试一次

结果还是对了13个,结果在output/minif2f/15-01-2025-17-04/results__qwenmax__1.json 数据在report_2025-01-15_17-04-54.txt

数据分布跟之前一模一样,这玩意儿的temperature一点用没有

一个好主意是,考虑对数据增广,增加一个槽位,允许prompt中在这里构造不同的思路
比如
- have 
- simp
- induction
- case
- ring

这个做法非常有效,多样性陡增,我同步调大了max_iter到了400,我们看看开一晚上能收集到多少数据

## 2025-01-16

首先从结果上看,还是只对了13个,结果在output/minif2f/15-01-2025-20-11/results__qwenmax__1.json  数据在report_2025-01-15_20-11-30.txt

时间上总体花了2个半小时
多样性好了不少,总共有836个样本
![report_2025-01-15.png](imgs/report_2025-01-15.png)

注意到有的出现了13条记录,而实际上我的搜搜宽度是8,所以只能是出现了环,即后续又回到了之前的某个状态,所以那个状态的记录数会超过搜搜宽度

那条13个记录的state是'case step\nn✝ n : ℕ\nh₀ : Nat.le 3 n\nIH : n ! < n ^ (n - 1)\n⊢ n ! * (n + 1) < (n + 1) ^ n'

这是真的有环,但是我的数据查起来有点麻烦,可以看到有些策略比如rw [Nat.succ_eq_add_one]是可以反复重复的

    case step\nn\u271d n : \u2115\nh\u2080 : Nat.le 3 n\nIH : n ! < n ^ (n - 1)\n\u22a2 (n + 1) * n ! < succ n ^ n

    rw [Nat.succ_eq_add_one]

    case step\nn\u271d n : \u2115\nh\u2080 : Nat.le 3 n\nIH : n ! < n ^ (n - 1)\n\u22a2 (n + 1) * n ! < (n + 1) ^ n

平均每条question有27个样本,注意是step级别的

接下来我需要考虑利用收集的数据,做进一步的rft

我需要一个cooker

 - 从report数据中洗出三类样本,绝对正确,绝对错误,和语法正确样本
 - 如果某个state已经有绝对正确样本了,其实他的样本都可以删掉
 - 如果某个state没有绝对正确样本,需要考虑降低绝对错误样本的概率

此处需要加工出
bs state
ba action
bprob probability
badvtarg advantage
bvtarge v target

优化器方面,参考XRL,我需要一个轻便的,torch版本的,cuda支持的,我可以翻下TRL

这玩意儿可以支持 sfttrainer,dpotrainer, rewardtrainer和ORPOTrainer

我得准备一个脚本,从日志数据中洗出来jsonl的格式的,用于支持dpo训练的数据

这玩意儿,只需要三个字段 prompt,chosen,rejected

注意到report_2025-01-15_20-11-30.txt 这玩意儿有834条样本,但是做成DPO只有58条,实在是太少了,去重之后只有了17条,太可怜了

## 2025-01-22

我首先是试着在M0上进一步DPO

我重新检查样本,重新生成了一批,还是可怜的17条

从训练的loss上看,基本没啥变化,维持在2.7附近,我训练了7个epoch,我取了1-2epoch位置上的一个checkpoint,使用的框架式TRL,DPO训练,训练模式是lora,基础模型是qwen-7B


    
    {'loss': 2.7656, 'grad_norm': 1.156054398017703, 'learning_rate': 0.0, 'rewards/chosen': 0.0, 'rewards/rejected': 0.0, 'rewards/accuracies': 0.0, 'rewards/margins': 0.0, 'logps/chosen': -24.5, 'logps/rejected': -30.375, 'logits/chosen': 0.875, 'logits/rejected': 0.265625, 'epoch': 0.31}
    {'loss': 2.7354, 'grad_norm': 1.2127426981682132, 'learning_rate': 2e-06, 'rewards/chosen': 0.010986328125, 'rewards/rejected': 0.0078125, 'rewards/accuracies': 0.25, 'rewards/margins': 0.0031280517578125, 'logps/chosen': -21.875, 'logps/rejected': -29.5, 'logits/chosen': 0.66796875, 'logits/rejected': 0.6875, 'epoch': 0.62}
    {'loss': 2.7529, 'grad_norm': 1.247688454843583, 'learning_rate': 2e-06, 'rewards/chosen': 0.02978515625, 'rewards/rejected': 0.0172119140625, 'rewards/accuracies': 0.375, 'rewards/margins': 0.01251220703125, 'logps/chosen': -22.375, 'logps/rejected': -24.25, 'logits/chosen': 0.72265625, 'logits/rejected': 0.87890625, 'epoch': 0.92}
    {'loss': 0.6904, 'grad_norm': 1.247688454843583, 'learning_rate': 2e-06, 'rewards/chosen': 0.03759765625, 'rewards/rejected': 0.0250244140625, 'rewards/accuracies': 1.0, 'rewards/margins': 0.0125732421875, 'logps/chosen': -25.625, 'logps/rejected': -29.0, 'logits/chosen': -0.09228515625, 'logits/rejected': -0.373046875, 'epoch': 1.0}
    {'loss': 2.7451, 'grad_norm': 1.148525779921521, 'learning_rate': 2e-06, 'rewards/chosen': 0.040771484375, 'rewards/rejected': 0.0164794921875, 'rewards/accuracies': 0.5, 'rewards/margins': 0.0242919921875, 'logps/chosen': -24.625, 'logps/rejected': -27.375, 'logits/chosen': 0.140625, 'logits/rejected': 0.859375, 'epoch': 1.31}
    {'loss': 2.7334, 'grad_norm': 1.2037811829142275, 'learning_rate': 2e-06, 'rewards/chosen': 0.015625, 'rewards/rejected': 0.0, 'rewards/accuracies': 0.75, 'rewards/margins': 0.015625, 'logps/chosen': -22.5, 'logps/rejected': -26.875, 'logits/chosen': 0.3359375, 'logits/rejected': 1.671875, 'epoch': 1.62}
    {'loss': 2.748, 'grad_norm': 1.2383992505684203, 'learning_rate': 2e-06, 'rewards/chosen': 0.02587890625, 'rewards/rejected': 0.007080078125, 'rewards/accuracies': 0.625, 'rewards/margins': 0.018798828125, 'logps/chosen': -22.625, 'logps/rejected': -25.5, 'logits/chosen': 0.6640625, 'logits/rejected': 1.0078125, 'epoch': 1.92}
    {'loss': 0.6914, 'grad_norm': 1.2383992505684203, 'learning_rate': 2e-06, 'rewards/chosen': -0.0250244140625, 'rewards/rejected': 0.006256103515625, 'rewards/accuracies': 0.0, 'rewards/margins': -0.03125, 'logps/chosen': -27.0, 'logps/rejected': -32.0, 'logits/chosen': 1.3828125, 'logits/rejected': -0.2412109375, 'epoch': 2.0}
    {'loss': 2.7354, 'grad_norm': 1.1236553900509187, 'learning_rate': 2e-06, 'rewards/chosen': 0.01409912109375, 'rewards/rejected': 0.00933837890625, 'rewards/accuracies': 0.5, 'rewards/margins': 0.004669189453125, 'logps/chosen': -24.0, 'logps/rejected': -25.0, 'logits/chosen': 0.435546875, 'logits/rejected': 0.396484375, 'epoch': 2.31}
    {'loss': 2.7686, 'grad_norm': 1.3990693416811004, 'learning_rate': 2e-06, 'rewards/chosen': 0.00469970703125, 'rewards/rejected': 0.00156402587890625, 'rewards/accuracies': 0.25, 'rewards/margins': 0.003143310546875, 'logps/chosen': -22.625, 'logps/rejected': -28.375, 'logits/chosen': 0.6796875, 'logits/rejected': -0.03759765625, 'epoch': 2.62}
    {'loss': 2.7354, 'grad_norm': 1.1526812574292118, 'learning_rate': 2e-06, 'rewards/chosen': 0.01251220703125, 'rewards/rejected': 0.00469970703125, 'rewards/accuracies': 0.625, 'rewards/margins': 0.0078125, 'logps/chosen': -24.25, 'logps/rejected': -25.75, 'logits/chosen': 0.625, 'logits/rejected': 0.34375, 'epoch': 2.92}
    {'loss': 0.6855, 'grad_norm': 1.1526812574292118, 'learning_rate': 2e-06, 'rewards/chosen': 0.006256103515625, 'rewards/rejected': -0.0250244140625, 'rewards/accuracies': 0.5, 'rewards/margins': 0.03125, 'logps/chosen': -26.25, 'logps/rejected': -27.5, 'logits/chosen': 0.06640625, 'logits/rejected': 0.6171875, 'epoch': 3.0}
    {'loss': 2.7441, 'grad_norm': 0.9307379679929956, 'learning_rate': 2e-06, 'rewards/chosen': 0.0, 'rewards/rejected': -0.006256103515625, 'rewards/accuracies': 0.75, 'rewards/margins': 0.006256103515625, 'logps/chosen': -25.0, 'logps/rejected': -30.25, 'logits/chosen': 0.478515625, 'logits/rejected': -0.0302734375, 'epoch': 3.31}
    {'loss': 2.7285, 'grad_norm': 1.1571385241840177, 'learning_rate': 2e-06, 'rewards/chosen': 0.043701171875, 'rewards/rejected': 0.01409912109375, 'rewards/accuracies': 0.875, 'rewards/margins': 0.0296630859375, 'logps/chosen': -23.25, 'logps/rejected': -27.25, 'logits/chosen': 0.65625, 'logits/rejected': 1.03125, 'epoch': 3.62}
    {'loss': 2.7217, 'grad_norm': 1.3602375047729942, 'learning_rate': 2e-06, 'rewards/chosen': 0.034423828125, 'rewards/rejected': -0.025146484375, 'rewards/accuracies': 0.875, 'rewards/margins': 0.0595703125, 'logps/chosen': -20.75, 'logps/rejected': -27.125, 'logits/chosen': 0.43359375, 'logits/rejected': 1.640625, 'epoch': 3.92}
    {'loss': 0.6777, 'grad_norm': 1.1641266251895739, 'learning_rate': 2e-06, 'rewards/chosen': 0.01251220703125, 'rewards/rejected': 0.018798828125, 'rewards/accuracies': 0.0, 'rewards/margins': -0.006256103515625, 'logps/chosen': -31.0, 'logps/rejected': -25.25, 'logits/chosen': 0.59375, 'logits/rejected': 0.5390625, 'epoch': 4.0}
    {'loss': 2.7227, 'grad_norm': 1.351855225997049, 'learning_rate': 2e-06, 'rewards/chosen': 0.02587890625, 'rewards/rejected': -0.016357421875, 'rewards/accuracies': 1.0, 'rewards/margins': 0.042236328125, 'logps/chosen': -23.375, 'logps/rejected': -25.625, 'logits/chosen': 0.578125, 'logits/rejected': 0.21875, 'epoch': 4.31}
    {'loss': 2.7119, 'grad_norm': 1.2012034539737284, 'learning_rate': 2e-06, 'rewards/chosen': 0.0211181640625, 'rewards/rejected': -0.01953125, 'rewards/accuracies': 0.75, 'rewards/margins': 0.04052734375, 'logps/chosen': -19.75, 'logps/rejected': -27.75, 'logits/chosen': 0.3828125, 'logits/rejected': 0.87890625, 'epoch': 4.62}
    {'loss': 2.7461, 'grad_norm': 1.0718952269317132, 'learning_rate': 2e-06, 'rewards/chosen': -0.00390625, 'rewards/rejected': -0.0211181640625, 'rewards/accuracies': 0.625, 'rewards/margins': 0.0172119140625, 'logps/chosen': -23.375, 'logps/rejected': -28.25, 'logits/chosen': 0.84765625, 'logits/rejected': 0.443359375, 'epoch': 4.92}
    {'loss': 0.6973, 'grad_norm': 1.0718952269317132, 'learning_rate': 2e-06, 'rewards/chosen': 0.01251220703125, 'rewards/rejected': -0.006256103515625, 'rewards/accuracies': 0.5, 'rewards/margins': 0.018798828125, 'logps/chosen': -16.875, 'logps/rejected': -26.875, 'logits/chosen': 1.0, 'logits/rejected': 1.8359375, 'epoch': 5.0}
    {'loss': 2.7432, 'grad_norm': 1.2505251888925102, 'learning_rate': 2e-06, 'rewards/chosen': 0.0234375, 'rewards/rejected': -0.01251220703125, 'rewards/accuracies': 0.75, 'rewards/margins': 0.0361328125, 'logps/chosen': -24.125, 'logps/rejected': -28.0, 'logits/chosen': 0.234375, 'logits/rejected': 1.015625, 'epoch': 5.31}
    {'loss': 2.7266, 'grad_norm': 1.2965263628092838, 'learning_rate': 2e-06, 'rewards/chosen': 0.026611328125, 'rewards/rejected': 0.0093994140625, 'rewards/accuracies': 0.5, 'rewards/margins': 0.0172119140625, 'logps/chosen': -22.25, 'logps/rejected': -27.375, 'logits/chosen': 0.55078125, 'logits/rejected': 0.62109375, 'epoch': 5.62}
    {'loss': 2.7188, 'grad_norm': 1.502436154738745, 'learning_rate': 2e-06, 'rewards/chosen': 0.042236328125, 'rewards/rejected': 0.0, 'rewards/accuracies': 0.875, 'rewards/margins': 0.042236328125, 'logps/chosen': -19.75, 'logps/rejected': -24.5, 'logits/chosen': 0.7578125, 'logits/rejected': 1.734375, 'epoch': 5.92}
    {'loss': 0.6797, 'grad_norm': 1.502436154738745, 'learning_rate': 2e-06, 'rewards/chosen': -0.01251220703125, 'rewards/rejected': -0.006256103515625, 'rewards/accuracies': 0.0, 'rewards/margins': -0.006256103515625, 'logps/chosen': -25.625, 'logps/rejected': -29.625, 'logits/chosen': -0.0869140625, 'logits/rejected': -0.40234375, 'epoch': 6.0}
    {'loss': 2.6992, 'grad_norm': 1.1662627987916439, 'learning_rate': 2e-06, 'rewards/chosen': 0.034423828125, 'rewards/rejected': -0.0078125, 'rewards/accuracies': 0.875, 'rewards/margins': 0.042236328125, 'logps/chosen': -21.0, 'logps/rejected': -25.25, 'logits/chosen': 0.5234375, 'logits/rejected': 1.8671875, 'epoch': 6.31}
    {'loss': 2.6963, 'grad_norm': 1.2600378321991774, 'learning_rate': 2e-06, 'rewards/chosen': 0.015625, 'rewards/rejected': -0.0015716552734375, 'rewards/accuracies': 0.5, 'rewards/margins': 0.0172119140625, 'logps/chosen': -24.875, 'logps/rejected': -29.75, 'logits/chosen': 0.30859375, 'logits/rejected': 0.71875, 'epoch': 6.62}
    {'loss': 2.6934, 'grad_norm': 1.0970709895398894, 'learning_rate': 2e-06, 'rewards/chosen': 0.04150390625, 'rewards/rejected': 0.002349853515625, 'rewards/accuracies': 1.0, 'rewards/margins': 0.0390625, 'logps/chosen': -21.25, 'logps/rejected': -26.625, 'logits/chosen': 0.392578125, 'logits/rejected': 0.291015625, 'epoch': 6.92}
    {'loss': 0.6748, 'grad_norm': 1.0970709895398894, 'learning_rate': 2e-06, 'rewards/chosen': 0.018798828125, 'rewards/rejected': -0.018798828125, 'rewards/accuracies': 0.5, 'rewards/margins': 0.03759765625, 'logps/chosen': -21.25, 'logps/rejected': -33.5, 'logits/chosen': 1.296875, 'logits/rejected': 0.81640625, 'epoch': 7.0}
    {'loss': 2.707, 'grad_norm': 1.3491108785715766, 'learning_rate': 2e-06, 'rewards/chosen': 0.039794921875, 'rewards/rejected': 0.01251220703125, 'rewards/accuracies': 0.625, 'rewards/margins': 0.02734375, 'logps/chosen': -23.375, 'logps/rejected': -26.5, 'logits/chosen': 0.392578125, 'logits/rejected': 0.890625, 'epoch': 7.31}
    {'loss': 2.708, 'grad_norm': 1.23132859854857, 'learning_rate': 2e-06, 'rewards/chosen': 0.0296630859375, 'rewards/rejected': -0.01092529296875, 'rewards/accuracies': 0.625, 'rewards/margins': 0.04052734375, 'logps/chosen': -24.25, 'logps/rejected': -29.125, 'logits/chosen': 0.7421875, 'logits/rejected': 0.50390625, 'epoch': 7.62}
    {'train_runtime': 202.8681, 'train_samples_per_second': 5.028, 'train_steps_per_second': 0.148, 'train_loss': 2.252799479166667, 'epoch': 7.62} 

评测的结果是,对了14题,比之前那个要好些,结果在 output/minif2f/22-01-2025-17-09/results__qwenmax__1.json 数据在 report_2025-01-22_17-09-27.txt

## 2025-01-23
考虑将探索的数据和adaption阶段的sft数据合并训练

我准备一个cooker_sft.py,加工出sft数据来

结果也只有23条数据,我用这个数据在M0上进一步sft,然后开始部署和测试

实验结果是12题,output/minif2f/23-01-2025-14-08/results__qwenmax__1.json, 数据在report_2025-01-23_14-08-45.txt



我引入gpt来做反向cot构造,并且再做一次recheck,效率很低,大约1分钟一条,大约需要17天


## 2025-01-27

我仔细读了deepseek那篇论文 https://arxiv.org/abs/2501.12948

几个有趣的参考是

1. 直接在非推理的小尺寸模型上的rft可能不如在更大尺寸上做，或者可以在推理模型上做
2. 其训练过程采用GRPO或者PPO其实都可以，重点是是freeze了valuemodel
3. 采样过程simple，不要去用复杂的mcts
4. 目前TRL逐步在支持GRPO，届时就会可以像SFT一样去调用RFT，这个重点在于工程开发
5. 如果TRL的建设符合预期，此时的重点就在与数据的构建，无论是数据增增广还是数据配置策略可能都是未被公开的重点细节，而且是开源社区的工程建设所不能触及的，所以我可以先把lean的这个RFT的集子做起来。

可以先对齐到这个版本 https://github.com/huggingface/trl/blob/grpo_vllm/docs/source/grpo_trainer.md

参考这个做数据准备

然后推理模型的基础模型，我可以选择一个14b的，比如https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-14B

同步下载这个模型


## 2025-02-05
TRL已经将GRPO集成了，果然都是在跟时间赛跑啊，不过对我来说就很方便了，只需要更新TRL，准备数据集就可以直接用GRPO了

注意几个reward函数

比如format reward

    import re
    
    def format_reward_func(completions, **kwargs):
        """Reward function that checks if the completion has a specific format."""
        pattern = r"^<think>.*?</think><answer>.*?</answer>$"
        completion_contents = [completion[0]["content"] for completion in completions]
        matches = [re.match(pattern, content) for content in completion_contents]
        return [1.0 if match else 0.0 for match in matches]

比如accuracy reward

    import re
    
    def reward_func(completions, ground_truth, **kwargs):
        # Regular expression to capture content inside \boxed{}
        matches = [re.search(r"\\boxed\{(.*?)\}", completion) for completion in completions]
        contents = [match.group(1) if match else "" for match in matches]
        # Reward 1 if the content is the same as the ground truth, 0 otherwise
        return [1.0 if c == gt else 0.0 for c, gt in zip(contents, ground_truth)]

TRL跟deepspeed一起用的时候 GRPO和PPO都有个异常，是关于 
self.warmup_num_steps = max(2, warmup_num_steps)
[rank0]: TypeError: '>' not supported between instances of 'str' and 'int'

这个主要是ds的配置中的auto在TRL中初始化报错，他是真的穿了一个auto，这玩意儿是个字符串
参考是 https://github.com/LianjiaTech/BELLE/issues/558
修改方法是将ds的配置中修改了那个steps


    "scheduler": {
        "type": "WarmupLR",
        "params": {
            "warmup_min_lr": "auto",
            "warmup_max_lr": "auto",
            "warmup_num_steps": 10
        }
    },