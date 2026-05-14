# pybase01_env

这一节只做一件事：

> 把 Python 开发环境、虚拟环境和包管理跑通。

如果这一步不稳，后面学 LangChain 时会频繁遇到这些问题：

* `python` 和 `pip` 不是同一个环境
* 包明明装了，但运行时找不到
* 同一个项目今天能跑，明天不能跑
* 不知道当前到底用了哪个解释器

所以这一节不是“理论介绍”，而是可执行练习。

---

# 学习目标

完成本节后，你应该能独立完成：

1. 确认本机 Python 版本
2. 创建和激活虚拟环境
3. 安装基础依赖
4. 确认 `python` 和 `pip` 来自同一环境
5. 运行一个简单 Python 程序
6. 导出依赖清单
7. 排查最常见的环境问题

---

# 你要掌握的核心概念

---

## 1. 什么是 Python 解释器

Python 程序不是直接被系统执行的，而是由 Python 解释器执行。

你需要知道：

* `python` 命令对应的是一个具体解释器
* 不同路径的解释器可能对应不同环境
* 项目能不能跑，首先取决于你到底在用哪个解释器

---

## 2. 什么是虚拟环境

虚拟环境的作用是：

* 给当前项目隔离依赖
* 避免不同项目之间包版本冲突
* 让项目环境可控

你应该建立这个习惯：

> 一个项目，一个虚拟环境。

---

## 3. 什么是包管理

包管理的核心问题是：

* 这个项目依赖哪些第三方库
* 这些库安装到哪里了
* 如何复现同样的环境

---

# 练习 1：确认 Python 是否可用

先在终端执行：

```bash
python --version
```

如果系统里 `python` 不可用，再试：

```bash
python3 --version
```

---

## 练习目标

确认：

* 机器上已经安装 Python
* 你知道当前应使用 `python` 还是 `python3`

---

## 你需要记录

记录下面两个信息：

1. Python 版本号
2. 当前可执行文件命令是 `python` 还是 `python3`

---

## 通过标准

你能明确回答：

* 当前机器的 Python 版本是多少
* 后续命令应该用 `python` 还是 `python3`

---

# 练习 2：确认解释器路径

执行：

```bash
which python
```

如果你的环境实际使用 `python3`，则执行：

```bash
which python3
```

---

## 练习目标

理解你当前调用的解释器到底在磁盘哪个位置。

---

## 为什么这一步重要

很多环境问题都源于：

* 你以为自己在用项目虚拟环境
* 实际上你用的是系统 Python

所以不能只看命令名，必须看路径。

---

## 通过标准

你能解释：

* 当前解释器的绝对路径
* 为什么“同样叫 python”不代表是同一个环境

---

# 练习 3：创建虚拟环境

在项目目录下执行：

```bash
python -m venv .venv
```

如果你的系统主要使用 `python3`，就执行：

```bash
python3 -m venv .venv
```

---

## 练习目标

创建当前项目专属虚拟环境。

---

## 你应该看到什么

项目目录下会出现：

```text
.venv/
```

其中会包含：

* `bin/`
* `lib/`
* 一些环境元数据

---

## 通过标准

你能解释：

* `.venv` 是做什么的
* 为什么不建议把依赖直接装到全局环境

---

# 练习 4：激活虚拟环境

在 macOS / Linux 下通常执行：

```bash
source .venv/bin/activate
```

激活后，再执行：

```bash
which python
```

---

## 练习目标

确认当前终端已经切换到项目虚拟环境。

---

## 你应该观察什么

激活后通常会看到两类变化：

1. 终端提示符前面出现 `(.venv)` 之类标记
2. `which python` 指向项目目录下的 `.venv/bin/python`

---

## 通过标准

你能判断当前是否已经进入虚拟环境，而不是靠猜。

---

# 练习 5：升级 pip

激活虚拟环境后执行：

```bash
python -m pip install --upgrade pip
```

---

## 练习目标

习惯使用：

```bash
python -m pip ...
```

而不是直接依赖 `pip` 命令。

---

## 为什么推荐这样做

因为：

* `python -m pip` 明确使用当前解释器对应的 pip
* 可以减少“包装到了别的环境里”的问题

---

## 通过标准

你能解释：

* 为什么 `python -m pip` 通常比直接 `pip` 更稳

---

# 练习 6：安装基础依赖

执行：

```bash
python -m pip install langchain langchain-openai
```

如果你只是先练环境，不急着装 LangChain，也可以先装一个更小的包，例如：

```bash
python -m pip install requests
```

---

## 练习目标

完成一次标准的第三方依赖安装。

---

## 你要理解的点

### 1. 安装到哪里

包会安装到当前虚拟环境里，不是全局系统目录。

---

## 2. 为什么要在虚拟环境里装

为了：

* 版本隔离
* 可复现
* 减少污染

---

## 通过标准

你能确认：

* 包已经安装成功
* 包安装在当前 `.venv` 对应环境中

---

# 练习 7：查看已安装依赖

执行：

```bash
python -m pip list
```

如果想只看某个包：

```bash
python -m pip show langchain
python -m pip show langchain-openai
```

---

## 练习目标

学会确认某个依赖是否真的装好了。

---

## 通过标准

你能回答：

* 当前环境装了哪些包
* `langchain` 是否安装成功
* `langchain-openai` 是否安装成功

---

# 练习 8：确认 python 和 pip 是否属于同一环境

执行：

```bash
which python
which pip
python -m pip --version
pip --version
```

---

## 练习目标

识别最常见环境问题：

* `python` 是虚拟环境里的
* `pip` 却是系统里的

---

## 你需要重点观察

看这些路径是否都指向同一个虚拟环境目录，例如：

```text
.../.venv/bin/python
.../.venv/bin/pip
```

---

## 通过标准

你能判断：

* 当前 `python` 和 `pip` 是否匹配
* 如果不匹配，为什么会出问题

---

# 练习 9：创建并运行一个最小 Python 文件

在项目里新建一个文件，例如：

```text
hello_env.py
```

内容：

```python
print("python env is ready")
```

运行：

```bash
python hello_env.py
```

---

## 练习目标

确认你不仅装好了环境，而且真的能用当前环境执行代码。

---

## 通过标准

屏幕输出：

```text
python env is ready
```

---

# 练习 10：读取已安装包并导入测试

把 `hello_env.py` 改成：

```python
import langchain

print("langchain import success")
```

再执行：

```bash
python hello_env.py
```

---

## 练习目标

验证“安装成功”和“代码里能导入成功”是一致的。

---

## 关键理解

有时候你看到安装成功了，但导入仍失败，通常原因是：

* 安装和运行不是同一个环境
* 解释器路径不一致

---

## 通过标准

成功打印：

```text
langchain import success
```

---

# 练习 11：导出依赖清单

执行：

```bash
python -m pip freeze > requirements.txt
```

---

## 练习目标

学会把当前环境依赖固化下来。

---

## 为什么这一步重要

因为项目不是只在你机器上运行一次。  
后面你需要：

* 复现环境
* 分享给别人
* 重新部署

这时依赖清单就很重要。

---

## 通过标准

项目目录下生成：

```text
requirements.txt
```

并且里面能看到已安装依赖。

---

# 练习 12：从依赖文件恢复环境

如果未来要恢复环境，标准做法是：

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## 练习目标

理解环境复现的基本流程。

---

## 通过标准

你能口头或书面说明一个项目从零恢复依赖的完整步骤。

---

# 常见问题排查

这一部分必须掌握。  
环境问题不是少数情况，而是新手最高频阻塞点之一。

---

## 问题 1：`python` 找不到

现象：

```text
command not found: python
```

处理思路：

* 试 `python3`
* 确认 Python 是否已安装

---

## 问题 2：包安装成功，但 `import` 失败

最常见原因：

* 安装时用的是一个环境
* 运行时用的是另一个环境

排查顺序：

1. `which python`
2. `python -m pip --version`
3. `python -m pip show 包名`

---

## 问题 3：`pip` 和 `python` 不一致

现象：

* `pip list` 能看到包
* 但 `python` 运行代码仍提示模块不存在

处理原则：

* 优先使用 `python -m pip`
* 少直接依赖裸 `pip`

---

## 问题 4：没有激活虚拟环境

现象：

* `which python` 指向系统目录
* 安装包后仍然混乱

排查方式：

* 看提示符
* 看 `which python`

---

## 问题 5：依赖版本冲突

现象：

* 安装包时报冲突
* 某些包版本不兼容

处理思路：

* 使用干净虚拟环境
* 明确安装版本
* 不在一个环境里堆很多无关项目

---

# 推荐你形成的习惯

---

## 1. 一个项目一个 `.venv`

---

## 2. 优先用 `python -m pip`

---

## 3. 先看 `which python`

---

## 4. 改完环境后先做导入测试

---

## 5. 依赖能固化就尽早固化

---

# 本节最小验收标准

完成这节后，你至少要能独立做到下面这些事：

1. 创建 `.venv`
2. 激活 `.venv`
3. 用 `python -m pip` 安装依赖
4. 用 `python` 运行脚本
5. 导入已安装包
6. 导出 `requirements.txt`
7. 判断 `python` 和 `pip` 是否来自同一环境

如果这些还做不到，不要急着进入 LangChain 代码学习。

---

# 下一步学什么

环境和包管理跑通后，下一步建议进入：

```text
pybase02_types
```

也就是：

* 基本类型
* 字符串
* 列表
* 字典
* 条件判断

因为这些是后面读写 prompt、组织消息、处理 JSON 的基础。
