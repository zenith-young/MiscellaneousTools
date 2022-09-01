#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import copy
import time
from jirahelper.excel import JiraExcel
from jirahelper.jira import JiraClient


JIRA_EXCEL_FILE = "C:/Fate/Workplace/project/Greater_China/PI Documents/2022/PI 2022.4/PI 22.4 Planning.xlsx"

JIRA_URL = "https://acsjira.honeywell.com/"
JIRA_USERNAME = "h141074"
JIRA_PASSWORD = base64.b64decode("SE9OODk0MTl3ZWxs")


def main():

    run_start_time = time.time()
    print()
    print("Start Time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(run_start_time)))
    print()

    # process_jira_excel()
    process_jira_excel_with_actions()

    run_end_time = time.time()
    print()
    print("End Time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(run_end_time)))
    print()
    print("Time Cost: %ds" % int(round(run_end_time - run_start_time)))


def process_jira_excel():

    # Init Variables

    jira = JiraClient(JIRA_URL, JIRA_USERNAME, JIRA_PASSWORD)
    excel = JiraExcel(JIRA_EXCEL_FILE)
    excel.open()
    excel.backup()

    # Clear Excel Action Status

    items = excel.get_items()
    for i in range(len(items)):
        excel_item = items[i]
        excel_item.story_status = None
    excel.save(JIRA_EXCEL_FILE)

    # Ignore Excel Items

    for i in range(len(items) - 1, -1, -1):
        excel_item = items[i]
        if excel_item.story_action is not None and excel_item.story_action.lower() == "Ignore".lower():
            items.pop(i)

    # Process Excel

    for i in range(len(items)):
        excel_item = items[i]
        print("Processing (%s/%s), row %s" % (i + 1, len(items), excel_item.row))
        if excel_item.story_id is None:
            create_jira_issue(jira, excel_item)
        else:
            update_jira_issue(jira, excel_item)
        excel.set_item(excel_item)
        excel.save(JIRA_EXCEL_FILE)
    excel.close()


def process_jira_excel_with_actions():

    # Init Variables

    jira = JiraClient(JIRA_URL, JIRA_USERNAME, JIRA_PASSWORD)
    excel = JiraExcel(JIRA_EXCEL_FILE)
    excel.open()
    excel.backup()

    # Clear Excel Action Status

    items = excel.get_items()
    for i in range(len(items)):
        excel_item = items[i]
        excel_item.story_status = None
    excel.save(JIRA_EXCEL_FILE)

    # Ignore Excel Items

    for i in range(len(items) - 1, -1, -1):
        excel_item = items[i]
        if excel_item.story_action is None or excel_item.story_action.lower() == "Ignore".lower():
            items.pop(i)

    # Process Excel

    for i in range(len(items)):
        excel_item = items[i]
        print("Processing (%s/%s), row %s" % (i + 1, len(items), excel_item.row))
        if excel_item.story_action.lower() == "Create".lower():
            create_jira_issue(jira, excel_item)
        elif excel_item.story_action.lower() == "Update".lower():
            update_jira_issue(jira, excel_item)
        elif excel_item.story_action.lower() == "Read".lower():
            read_jira_issue(jira, excel_item)
        elif excel_item.story_action.lower() == "Remove".lower():
            remove_jira_issue(jira, excel_item)
        elif excel_item.story_action.lower() == "Delete".lower():
            delete_jira_issue(jira, excel_item)
        else:
            excel_item.story_status = "Failed: Invalid Action"
        excel.set_item(excel_item)
        excel.save(JIRA_EXCEL_FILE)
    excel.close()


def create_jira_issue(jira, excel_item):

    if excel_item.feature_id is None or excel_item.feature_name is None:
        excel_item.story_status = "Failed: No feature info"
        return False
    if excel_item.story_title is None:
        excel_item.story_status = "Failed: No story title"
        return False
    if excel_item.story_id is not None:
        excel_item.story_status = "Failed: Existing story id"
        return False

    jira_item = copy.copy(excel_item)
    if excel_item.story_description is None:
        jira_item.story_description = excel_item.story_title
    if excel_item.story_acceptance_criteria is None:
        jira_item.story_acceptance_criteria = excel_item.story_title

    jira_id = jira.create_issue(jira_item)
    if jira_id is not None:
        excel_item.story_status = "Success"
        excel_item.story_id = jira_id
        return True
    else:
        excel_item.story_status = "Failed: Server error"
        return False


def update_jira_issue(jira, excel_item):

    if excel_item.feature_id is None or excel_item.feature_name is None:
        excel_item.story_status = "Failed: No feature info"
        return False
    if excel_item.story_title is None:
        excel_item.story_status = "Failed: No story title"
        return False
    if excel_item.story_id is None:
        excel_item.story_status = "Failed: No story id"
        return False

    jira_item = copy.copy(excel_item)
    if excel_item.story_description is None:
        jira_item.story_description = excel_item.story_title
    if excel_item.story_acceptance_criteria is None:
        jira_item.story_acceptance_criteria = excel_item.story_title

    ok = jira.update_issue(excel_item.story_id, jira_item)
    if ok:
        excel_item.story_status = "Success"
        return True
    else:
        excel_item.story_status = "Failed: Server error"
        return False


def read_jira_issue(jira, excel_item):

    if excel_item.story_id is None:
        excel_item.story_status = "Failed: No story id"
        return False

    issue_details = jira.read_issue(excel_item.story_id, excel_item)
    if issue_details is not None:
        excel_item.story_title = issue_details.story_title
        excel_item.story_point = issue_details.story_point
        excel_item.story_description = issue_details.story_description
        excel_item.story_acceptance_criteria = issue_details.story_acceptance_criteria
        excel_item.story_components = issue_details.story_components
        excel_item.story_products = issue_details.story_products
        excel_item.story_fix_versions = issue_details.story_fix_versions
        excel_item.story_status = "Success"
        return True
    else:
        excel_item.story_status = "Failed: Server error"
        return False


def remove_jira_issue(jira, excel_item):

    if excel_item.story_id is None:
        excel_item.story_status = "Failed: No story id"
        return False

    ok = jira.remove_issue(excel_item.story_id)
    if ok:
        excel_item.story_status = "Success"
        return True
    else:
        excel_item.story_status = "Failed: Server error"
        return False


def delete_jira_issue(jira, excel_item):

    if excel_item.story_id is None:
        excel_item.story_status = "Failed: No story id"
        return False

    ok = jira.delete_issue(excel_item.story_id)
    if ok:
        excel_item.story_status = "Success"
        return True
    else:
        excel_item.story_status = "Failed: Server error"
        return False


# App

if __name__ == "__main__":
    main()
