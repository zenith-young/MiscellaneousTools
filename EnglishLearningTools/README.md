# EnglishLearningTools

## Overview

用来辅助英语学习的工具，使用 python 编写

[TOC]

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
conda install -c conda-forge/label/cf201901 pdfminer3k
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


