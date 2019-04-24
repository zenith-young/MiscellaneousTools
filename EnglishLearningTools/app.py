#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from english_word_frequency_statistics import EnglishWordFrequencyStatistics


# Main Entry

def main():

    print("")

    stat = EnglishWordFrequencyStatistics(
        r'C:\Fate\Documents\学习资料\美语资料\ESLPod\ESL Podcast\分类 PDF\Daily Life\EP164 - Seeing a Specialist [2006-05-15].pdf'
    )
    stat.initialize()
    normal_result, lemmed_result = stat.calculate()

    print("\nNormal result:", normal_result)
    print("\nLemmed result:", lemmed_result)


# App

if __name__ == '__main__':
    main()
