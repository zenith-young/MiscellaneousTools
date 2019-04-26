# EnglishLearningTools

## Overview

用来辅助英语学习的工具，使用 python 编写

- [EnglishLearningTools](#EnglishLearningTools)
  - [Overview](#Overview)
  - [english_word_frequency_statistics.py](#english_word_frequency_statistics.py)

## english_word_frequency_statistics.py

用来统计英语文章中的单词词频，目的是想了解自己做英语阅读后，如果完全掌握了其中的单词，词汇量能达到多少

**优点：**

1. 程序支持 pdf、txt 文件
2. 程序支持文件夹，并递归的解析文件夹内的文件
3. 程序支持以下几种统计结果：
   - 所有文件的总的单词数：重复单词多次统计
   - 所有文件出现的词汇量：重复单词一次统计
   - 所有文件统计出的词频详细信息：每个单词出现的次数
4. 支持解析常用缩写：'s、've、'll 等等
5. 支持词性还原：
   - 名词复数还原成单数
   - 动词各种时态语态词形还原成原形动词
   - 形容词、副词暂时没有处理，因为有些比较级最高级也应该单独记忆

**缺点：**

1. 解析文件夹时，递归解析出的文件不能重名，因为统一转换成了 txt 文件，并放到了 temp 文件夹下，递归解析文件重名会导致两个文件的内容输出到了同一个 txt 文件中（但是不影响统计结果）
2. 没有使用多线程，导致解析多个 pdf 文件时，耗时比较长，因为从 pdf 转成 txt 比较耗时
3. 词形还原的不彻底，一些专有名词还是不好识别出来，例如 U.S.
4. 暂时没法识别名字，所以有一些人名、地名也当做单词统计了，甚至还会分开统计，例如 Los Angeles，会被统计成 los、angeles

**后续开发：**

1. [优先] 加入图表显示功能，使用 pandas 做各种统计曲线
2. [推迟] 完善白名单功能，直接略过一些词，例如 Los Angeles、U.S. 等等
3. [推迟] 使用多线程加快解析速度

**构建开发环境：**

注：本人由于使用的是 Anaconda，所以部分步骤可能会不适用于 pip install

1) 安装 pdfminer3k：

[使用 Anaconda 安装 pdfminer3k](https://anaconda.org/conda-forge/pdfminer3k)

网站上有命令：
```shell
conda install -c conda-forge pdfminer3k
```

2) 安装 nltk：

[Installing NLTK](http://www.nltk.org/install.html)

[Installing NLTK Data](http://www.nltk.org/data.html)

nltk 是 python 自然语言处理库，必须搭配 nltk data 使用，其中有各种插件等等，简要记录一下安装步骤：

```shell
pip install -U nltk
```

打开 python 交互控制台：

```python
>>> import nltk
>>> nltk.download()
```

会弹出 UI 界面，安装以下几个插件：
- averaged_perceptron_tagger
- wordnet

修改 app.py，填写你要统计的文件或者文件夹

再编译运行源码就没有错误了

3) 安装 numpy、matplotlib：（不再使用，可跳过）

理论上安装完 Anaconda 之后，这些包默认就有了，但是使用 PyCharm 编译运行报错：

```
C:\Fate\Developer\Anaconda_5.3.1\python.exe C:/Fate/Workplace/miscellaneous/EnglishLearningTools/app.py
Traceback (most recent call last):
  File "C:/Fate/Workplace/miscellaneous/EnglishLearningTools/app.py", line 4, in <module>
    from english_word_frequency_statistics import EnglishWordFrequencyStatistics, StatisticsCharts
  File "C:\Fate\Workplace\miscellaneous\EnglishLearningTools\english_word_frequency_statistics.py", line 8, in <module>
    import numpy as np
  File "C:\Fate\Developer\Anaconda_5.3.1\lib\site-packages\numpy\__init__.py", line 140, in <module>
    from . import _distributor_init
  File "C:\Fate\Developer\Anaconda_5.3.1\lib\site-packages\numpy\_distributor_init.py", line 34, in <module>
    from . import _mklinit
ImportError: DLL load failed: The specified module could not be found.

Process finished with exit code 1
```

但是奇怪的是，直接使用 conda 命令行 import numpy 没有错，最后在 jetbrain 官网的一条评论里找到了解决方案：

说明：PyCharm 会要求填写 python 的路径，我并没有填写 conda 的 envs 路径，而是直接使用的 base env，并且系统变量 PATH 中没有设置 python 路径，原理不是很清楚，设置完系统变量就好了。

```
系统变量 PATH 中添加：
C:\Fate\Developer\Anaconda_5.3.1\Library\bin
```

附链接：[解决方案：见 Anya Datasci 的回答](https://intellij-support.jetbrains.com/hc/en-us/community/posts/360001194720-Numpy-import-error-in-PyCharm-Importing-the-multiarray-numpy-extension-module-failed-)

4) 安装 pyecharts：

试了 matplotlib，由于横轴表示大量的单词，导致 matplotlib 画出来的图几乎没法看，不支持缩放，因此改用 pyecharts 试试：

注：pyecharts 不支持 conda 安装，conda 中默认自带 pip，不是 pip3：

```
pip install pyecharts
pip install pyecharts_snapshot
```

