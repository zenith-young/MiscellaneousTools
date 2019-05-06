#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from english_word_frequency_statistics import EnglishWordFrequencyStatistics


# Main Entry

def main():

    print("")

    stat = EnglishWordFrequencyStatistics(
        # r'C:\Fate\Documents\学习资料\美语资料\ESLPod\ESL Podcast\Learnt'
        r'C:\Fate\Documents\学习资料\美语资料\ESLPod\ESL Podcast\PDF'
    )
    stat.initialize()
    normal_results, lemmed_results = stat.calculate()

    print("Total words:", normal_results.total_words)
    print("Total words distinct:", normal_results.total_words_distinct)
    print("Total words distinct & lemmed:", lemmed_results.total_words_distinct)

    stat.plot_word_frequency(normal_results, 'english_word_frequency_statistics.html')
    stat.plot_word_frequency(lemmed_results, 'english_word_frequency_statistics_lemmatized.html')
    stat.plot_word_learning_curve([normal_results, lemmed_results], ['Normal', 'Lemmatized'], 'english_word_learning_curve.html')


# App

if __name__ == '__main__':
    main()
