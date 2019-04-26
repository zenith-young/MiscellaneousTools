#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from english_word_frequency_statistics import EnglishWordFrequencyStatistics, StatisticsCharts


# Main Entry

def main():

    print("")

    stat = EnglishWordFrequencyStatistics(
        r'C:\Users\h141074\Desktop\New folder'
    )
    stat.initialize()
    normal_results, lemmed_results = stat.calculate()

    StatisticsCharts.plot_word_frequency(normal_results)


# App

if __name__ == '__main__':
    main()
