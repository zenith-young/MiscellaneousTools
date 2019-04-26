#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json

import numpy as np
import matplotlib.pyplot as plt

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextContainer, LTFigure
from pdfminer.pdftypes import PDFException

from nltk import pos_tag
from nltk.stem import WordNetLemmatizer

from pyecharts import Bar

from utils import FileSystemUtils


class EnglishWordFrequencyStatistics(object):

    def __init__(self, source, temp_folder='temp'):
        self._source = source
        self._temp_folder = temp_folder
        self._temp_converted_folder = os.path.join(temp_folder, '1. converted_txt')
        self._temp_formatted_folder = os.path.join(temp_folder, '2. formatted_txt')
        self._ignored_words = [
            'esl',
            'www',
            'com',
            'eslpod',
            'lucy',
            'tse',
            'jeff',
            'mcquillan',
            'sheila'
        ]

    # Public Functions

    def initialize(self):
        FileSystemUtils.init_folder(self._temp_folder)
        FileSystemUtils.init_folder(self._temp_converted_folder)
        FileSystemUtils.init_folder(self._temp_formatted_folder)

    def calculate(self):
        self._convert_files_to_txt_files()
        self._format_txt_files()
        return self._calculate_for_formatted_txt_files()

    # Private Functions

    def _convert_files_to_txt_files(self):

        source = self._source
        converted_folder = self._temp_converted_folder

        files = []

        if isinstance(source, str) and FileSystemUtils.is_file(source):
            files.append(source)
        elif isinstance(source, str) and FileSystemUtils.is_dir(source):
            files = FileSystemUtils.list_all_files_recursively(source)
        elif isinstance(source, list):
            files = source
        else:
            print("Error: Unknown source")
            return

        for file in files:
            ext = FileSystemUtils.get_file_ext(file)
            if ext == '.txt':
                FileSystemUtils.copyFilesToFolder([file], converted_folder)
            elif ext == '.pdf':
                try:
                    PDF2TXTConverter.convert(file, converted_folder)
                except PDFException as e:
                    print("Error: Failed to parse PDF: " + file + ":")
                    print(repr(e))
            else:
                print("Warning: File type: " + ext + ", is not supported, ignored")
                continue

    def _format_txt_files(self):

        converted_folder = self._temp_converted_folder
        formatted_folder = self._temp_formatted_folder

        files = FileSystemUtils.list_all_files_recursively(converted_folder)
        for file in files:
            target_file = os.path.join(formatted_folder, FileSystemUtils.get_file_name(file) + '.txt')
            with open(file, 'r', encoding='utf-8') as sp, open(target_file, 'a', encoding='utf-8') as tp:
                text = sp.read()
                text = self._format(text)
                tp.write(text)

    def _format(self, text):

        # 1. 替换中文单引号为英文单引号
        pat = re.compile(r'’')
        new_text = pat.sub('\'', text)

        # 2. 去掉所有非字母及英文单引号的所有字符
        pat = re.compile(r'[^a-zA-Z\']+')
        new_text = pat.sub(' ', new_text).strip().lower()

        # 3. 还原缩写: 'm -> am
        pat = re.compile(r'(?<=[Ii])\'m')
        new_text = pat.sub(' am', new_text)

        # 4. 还原缩写: 're -> are
        pat = re.compile(r'(?<=[a-zA-Z])\'re')
        new_text = pat.sub(' are', new_text)

        # 5. 还原缩写: 've -> have
        pat = re.compile(r'(?<=[a-zA-Z])\'ve')
        new_text = pat.sub(' have', new_text)

        # 6. 还原缩写: 'll -> will
        pat = re.compile(r'(?<=[a-zA-Z])\'ll')
        new_text = pat.sub(' will', new_text)

        # 7. 还原缩写: 'd -> would
        pat = re.compile(r'(?<=[a-zA-Z])\'d')
        new_text = pat.sub(' would', new_text)

        # 8. 还原缩写: can't -> can not
        pat = re.compile(r'(?<=can)\'t')
        new_text = pat.sub(' not', new_text)

        # 9. 还原缩写: n't -> not
        pat = re.compile(r'(?<=[a-zA-Z])n\'t')
        new_text = pat.sub(' not', new_text)

        # 10. 还原缩写: xx's -> xx is
        pat = re.compile(r'(it|he|she|that|this|there|here)(\'s)')
        new_text = pat.sub(r'\1 is', new_text)

        # 11. 还原缩写: let's -> let us
        pat = re.compile(r'(?<=let)\'s')
        new_text = pat.sub(' us', new_text)

        # 12. 去掉单数所有格: xx's -> xx
        pat = re.compile(r'(?<=[a-zA-Z0-9])\'s')
        new_text = pat.sub('', new_text)

        # 13. 去掉复数所有格: xxs' -> xx
        pat = re.compile(r'(?<=s)\'s?')
        new_text = pat.sub('', new_text)

        return new_text

    def _calculate_for_formatted_txt_files(self):

        normal_results = StatisticsResults()
        lemmed_results = StatisticsResults()

        files = FileSystemUtils.list_all_files_recursively(self._temp_formatted_folder)
        for file in files:
            normal_result, lemmed_result = self._calculate_for_formatted_txt_file(file)
            normal_results.add(normal_result)
            lemmed_results.add(lemmed_result)

        return normal_results, lemmed_results

    def _calculate_for_formatted_txt_file(self, file):

        normal_result = StatisticsResult()
        lemmed_result = StatisticsResult()

        with open(file, 'r', encoding='utf-8') as fp:

            txt = fp.read()

            words = txt.split(' ')
            for word in words:
                if word in self._ignored_words:
                    continue
                elif word in normal_result.word_frequency:
                    normal_result.word_frequency[word] += 1
                else:
                    normal_result.word_frequency[word] = 1
            normal_result.total_words = len(words)
            normal_result.total_words_distinct = len(normal_result.word_frequency)
            normal_result.filename = FileSystemUtils.get_file_name(file)

            words = self._lemmatization(txt.split(' '))
            for word in words:
                if word in self._ignored_words:
                    continue
                elif word in lemmed_result.word_frequency:
                    lemmed_result.word_frequency[word] += 1
                else:
                    lemmed_result.word_frequency[word] = 1
            lemmed_result.total_words = len(words)
            lemmed_result.total_words_distinct = len(lemmed_result.word_frequency)
            lemmed_result.filename = FileSystemUtils.get_file_name(file)

        return normal_result, lemmed_result

    def _lemmatization(self, words):

        wnl = WordNetLemmatizer()
        lemmed_words = []

        for word, tag in pos_tag(words):
            if tag.startswith('NN'):
                lemmed_words.append(wnl.lemmatize(word, pos='n'))
            elif tag.startswith('VB'):
                lemmed_words.append(wnl.lemmatize(word, pos='v'))
            else:
                lemmed_words.append(word)

        return lemmed_words


class StatisticsResults(object):

    def __init__(self):
        self.total_words = 0
        self.total_words_distinct = 0
        self.word_frequency = {}
        self.details = []

    def add(self, result):
        if result is None:
            return
        for key, value in result.word_frequency.items():
            if key in self.word_frequency:
                self.word_frequency[key] += value
            else:
                self.word_frequency[key] = value
        self.total_words += result.total_words
        self.total_words_distinct = len(self.word_frequency)
        self.details.append(result)

    def to_dict(self):
        return {
            'totalWords': self.total_words,
            'totalWordsDistinct': self.total_words_distinct,
            'wordFrequency': self.word_frequency,
            'details': [result.to_dict() for result in self.details]
        }

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)


class StatisticsResult(object):

    def __init__(self):
        self.filename = ''
        self.total_words = 0
        self.total_words_distinct = 0
        self.word_frequency = {}

    def to_dict(self):
        return {
            'filename': self.filename,
            'totalWords': self.total_words,
            'totalWordsDistinct': self.total_words_distinct,
            'wordFrequency': self.word_frequency,
        }

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)


class StatisticsCharts(object):

    @staticmethod
    def plot_word_frequency(results):

        # 数据源

        xticks = list(results.word_frequency.keys())
        xticks.sort()
        yticks = np.arange(0, 20000, 100)
        index = np.arange(len(xticks))
        values = [results.word_frequency[key] for key in xticks]
        width = 0.35

        # 使用 matplotlib 画图，实测效果不好

        # plt.figure()
        # plt.subplot(1, 1, 1)
        #
        # plt.bar(index, values, width, label="Normal")
        #
        # plt.xticks(index, xticks)
        # plt.yticks(yticks)
        #
        # plt.xlabel('Words')
        # plt.ylabel('Frequency')
        #
        # plt.title('English Word Frequency Statistics')
        # plt.legend(loc="upper right")
        #
        # plt.show()

        # 使用 pyecharts 画图，缺点是不能实时显示

        fig = Bar('English Word Frequency Statistics', width=1280, height=800, title_pos='center')
        fig.add('Normal', xticks, values)
        fig.show_config()
        fig.render()


class PDF2TXTConverter(object):

    # Public Functions

    @staticmethod
    def convert(source, target_folder):
        if isinstance(source, str) and FileSystemUtils.is_file(source):
            PDF2TXTConverter._convert_file(source, target_folder)
        elif isinstance(source, str) and FileSystemUtils.is_dir(source):
            PDF2TXTConverter._convert_folder(source, target_folder)
        elif isinstance(source, list):
            PDF2TXTConverter._convert_files(source, target_folder)
        else:
            print("Error: Unknown source")
            return

    # Private Functions

    @staticmethod
    def _convert_folder(source_folder, target_folder):
        source_files = FileSystemUtils.list_all_files_recursively(source_folder)
        PDF2TXTConverter._convert_files(source_files, target_folder)

    @staticmethod
    def _convert_files(source_files, target_folder):
        for file in source_files:
            try:
                PDF2TXTConverter._convert_file(file, target_folder)
            except PDFException as e:
                print("Error: Failed to parse PDF: " + file + ":")
                print(repr(e))

    @staticmethod
    def _convert_file(source_file, target_folder):

        if not PDF2TXTConverter._is_valid_pdf(source_file):
            print("Warning: File: " + source_file + ", is not valid PDF, ignored")
            return

        with open(source_file, 'rb') as pdf_fp:

            parser = PDFParser(pdf_fp)
            doc = PDFDocument()
            parser.set_document(doc)
            doc.set_parser(parser)
            doc.initialize()

            if not doc.is_extractable:
                print("Warning: PDF: " + source_file + ", is not extractable, ignored")
                return

            resmgr = PDFResourceManager()
            laparams = LAParams(all_texts=True, heuristic_word_margin=True)
            device = PDFPageAggregator(resmgr, laparams=laparams)
            interpreter = PDFPageInterpreter(resmgr, device)

            txt_filename = FileSystemUtils.get_file_name(source_file)
            txt_filepath = os.path.join(target_folder, txt_filename + '.txt')

            with open(txt_filepath, 'a', encoding='utf-8') as txt_fp:
                for page in doc.get_pages():
                    interpreter.process_page(page)
                    layout = device.get_result()
                    for widget in layout:
                        if isinstance(widget, LTTextContainer):
                            txt_fp.write(widget.get_text())
                        elif isinstance(widget, LTFigure):
                            txt_list = []
                            PDF2TXTConverter._get_texts_from_ltfigure(widget, txt_list)
                            for txt_string in txt_list:
                                txt_fp.write(txt_string)

    @staticmethod
    def _get_texts_from_ltfigure(ltfigure, result_list):
        objs = ltfigure._objs
        for obj in objs:
            if isinstance(obj, LTTextContainer):
                result_list.append(obj.get_text())
            elif isinstance(obj, LTFigure):
                PDF2TXTConverter._get_texts_from_ltfigure(obj, result_list)

    @staticmethod
    def _is_valid_pdf(file):
        return (FileSystemUtils.get_file_ext(file) == '.pdf') if True else False
