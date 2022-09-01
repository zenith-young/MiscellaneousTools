#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import traceback
from jira import JIRA


class JiraClient(object):

    PROJECT = "GCBCS"
    ISSUE_TYPE = "Story"
    PRIORITY = "None"
    STORY_TYPE = "User"
    TEAMS = "Skywalker"

    def __init__(self, url, username, password):
        self.__jira_url = url
        self.__jira_username = username
        self.__jira_password = password
        self.__jira = JIRA(url, basic_auth=(username, password))

    def create_issue(self, story_details):
        try:
            issue = self.__jira.create_issue({
                "project": {"key": JiraClient.PROJECT},
                "issuetype": {"name": JiraClient.ISSUE_TYPE},
                "summary": story_details.story_title,
            })
            self.update_issue(issue.key, story_details)
            return issue.key
        except Exception as ex:
            print("Failed to create issue:")
            print("-> story_details: %s" % story_details)
            print("-> exception: %s" % str(ex))
            traceback.print_exc()
            return None

    def update_issue(self, jira_id, story_details):
        try:
            issue = self.__jira.issue(jira_id)
            issue.update({
                "summary": story_details.story_title,
                "fixVersions": None if story_details.story_fix_versions is None else [{"name": story_details.story_fix_versions}],
                "priority": {"name": JiraClient.PRIORITY},
                "components": None if story_details.story_components is None else [{"name": story_details.story_components}],
                "labels": None,
                "customfield_38101": {"value": JiraClient.STORY_TYPE},
                "customfield_38102": {"value": JiraClient.TEAMS},
                "customfield_38103": None if story_details.story_products is None else {"value": story_details.story_products},
                "customfield_23541": story_details.story_acceptance_criteria,
                "customfield_11213": story_details.story_point,
                "description": story_details.story_description,
            })
            self.add_issues_to_epic(story_details.feature_id, [issue.key])
            self.specify_issue(issue)
            return True
        except Exception as ex:
            print("Failed to update issue:")
            print("-> jira_id: %s" % jira_id)
            print("-> story_details: %s" % story_details)
            print("-> exception: %s" % str(ex))
            traceback.print_exc()
            return False

    def read_issue(self, jira_id, story_details):
        try:
            issue = self.__jira.issue(jira_id)
            issue_details = copy.copy(story_details)
            issue_details.story_title = issue.fields.summary
            issue_details.story_point = None if issue.fields.customfield_11213 is None else int(issue.fields.customfield_11213)
            issue_details.story_description = None if issue.fields.description is None or issue.fields.description == "" else issue.fields.description
            issue_details.story_acceptance_criteria = None if issue.fields.customfield_23541 is None or issue.fields.customfield_23541 == "" else issue.fields.customfield_23541
            issue_details.story_components = None if issue.fields.components is None or len(issue.fields.components) == 0 else issue.fields.components[0].name
            issue_details.story_products = None if issue.fields.customfield_38103 is None else issue.fields.customfield_38103.value
            issue_details.story_fix_versions = None if issue.fields.fixVersions is None or len(issue.fields.fixVersions) == 0 else issue.fields.fixVersions[0].name
            return issue_details
        except Exception as ex:
            print("Failed to read issue:")
            print("-> jira_id: %s" % jira_id)
            print("-> story_details: %s" % story_details)
            print("-> exception: %s" % str(ex))
            traceback.print_exc()
            return None

    def remove_issue(self, jira_id):
        try:
            issue = self.__jira.issue(jira_id)
            issue.update({
                "fixVersions": [],
                "components": [],
                "labels": None,
                "customfield_38102": {"value": JiraClient.TEAMS},
                "customfield_38103": None,      # Products
                "customfield_13300": None,      # Epic Link
            })
            return True
        except Exception as ex:
            print("Failed to remove issue:")
            print("-> jira_id: %s" % jira_id)
            print("-> exception: %s" % str(ex))
            traceback.print_exc()
            return False

    def delete_issue(self, jira_id):
        try:
            issue = self.__jira.issue(jira_id)
            issue.delete()
            return True
        except Exception as ex:
            print("Failed to delete issue:")
            print("-> jira_id: %s" % jira_id)
            print("-> exception: %s" % str(ex))
            traceback.print_exc()
            return False

    def add_issues_to_epic(self, epic_id, story_ids):
        try:
            self.__jira.add_issues_to_epic(epic_id, story_ids)
            return True
        except Exception as ex:
            print("Failed to add issues to epic:")
            print("-> epic_id: %s" % epic_id)
            print("-> story_ids: %s" % story_ids)
            print("-> exception: %s" % str(ex))
            traceback.print_exc()
            return False

    def specify_issue(self, issue):
        if issue.fields.status.name == "Pending Approval":
            self.__jira.transition_issue(issue, "Specify")

    def show_issue_details(self, jira_id):
        try:
            issue = self.__jira.issue(jira_id)
            epic = None if issue.fields.customfield_13300 is None else self.__jira.issue(issue.fields.customfield_13300)
            story_points = None if issue.fields.customfield_11213 is None else int(issue.fields.customfield_11213)
            issue_details = '''
                Jira Id: %s,
                Project: %s,
                Summary: %s,
                Status: %s,
                Resolution: %s,
                Fix Version/s: %s,
                Priority: %s,
                Affects Version/s: %s,
                Component/s: %s,
                Labels: %s,
                Story Type: %s,
                Teams: %s,
                Products: %s,
                Epic Link: %s,
                Acceptance Criteria: %s,
                Planned Increment: %s,
                Story Points: %s,
                Description: %s
            ''' % (
                issue,
                issue.fields.project,
                issue.fields.summary,
                issue.fields.status,
                issue.fields.resolution,
                issue.fields.fixVersions,
                issue.fields.priority,
                issue.fields.versions,
                issue.fields.components,
                issue.fields.labels,
                issue.fields.customfield_38101,     # Story Type
                issue.fields.customfield_38102,     # Teams
                issue.fields.customfield_38103,     # Products
                epic.fields.summary,                # Epic Link
                issue.fields.customfield_23541,     # Acceptance Criteria
                issue.fields.customfield_38713,     # Planned Increment
                story_points,                       # Story Points
                issue.fields.description,
            )
            print(issue_details)
            return True
        except Exception as ex:
            print("Failed to show issue details:")
            print("-> jira_id: %s" % jira_id)
            print("-> exception: %s" % str(ex))
            traceback.print_exc()
            return False


# JIRA API Documents

# 项目基本信息 - 标题：

# issue.key = {str} GCBCS-8162
# issue.id = {str} 8464181
# issue.fields.project = {str} GCBCS
# issue.fields.summary = {str} SDD 更新：TimeDelay、RuntimeBalancer、Trigger

# 项目基本信息 - 状态：

# issue.fields.status = {Status} Accepted
# issue.fields.resolution = {Resolution} Fixed
# issue.fields.fixVersions = {list<JIRA Version>}
# issue.fields.fixVersions[0] = {JIRA Version} 81726-BEATs200-Conditional OKTS launch
# issue.fields.fixVersions[0].id = {str} 234732
# issue.fields.fixVersions[0].name = {str} 81726-BEATs200-Conditional OKTS launch

# 项目基本信息 - 属性：

# issue.fields.issueType = {IssueType} Story
# issue.fields.priority = {Priority} None
# issue.fields.versions = {list}
# issue.fields.components = {list<JIRA Component>}
# issue.fields.components[0] = {JIRA Component} Beats 200 Programming Tool
# issue.fields.components[0].id = {str} 178493
# issue.fields.components[0].name = {str} Beats 200 Programming Tool
# issue.fields.labels = {list}
# - Story Type:          issue.fields.customfield_38101 = {CustomFieldOption} User ( id = {str} 56576 )
# - Teams:               issue.fields.customfield_38102 = {CustomFieldOption} Skywalker ( id = {str} 62961 )
# - Products:            issue.fields.customfield_38103 = {CustomFieldOption} Programming Tool ( id = {str} 62996 )
# - Epic Link:           issue.fields.customfield_13300 = {str} GCBCS-6729
# - Acceptance Criteria: issue.fields.customfield_23541 = {str} Finish story
# - Planned Increment:   issue.fields.customfield_38713 = {CustomFieldOption} PI 2022.3 ( id = {str} 66856 )
# - Story Points:        issue.fields.customfield_11213 = {float} 2.0

# 项目基本信息 - 详细：

# issue.fields.description = {str} Fix Sprint 22.3.3 Demo Issues

# issue.fields.attachment = {list}
# issue.fields.issueLinks = {list<JIRA IssueLink>}
# issue.fields.subtasks = {list}
# issue.fields.comment.comments = {list<JIRA Comment>}

# 项目基本信息 - 人员：

# issue.fields.creator = {User}
# issue.fields.reporter = {User}
# issue.fields.assignee = {User} jax Wang
# issue.fields.assignee.displayName = {str} jax Wang
# issue.fields.assignee.emailAddress = {str} Yabin.Wang@Honeywell.com
# issue.fields.assignee.key = {str} JIRAUSER172256
# issue.fields.assignee.name = {str} h483677

# 项目基本信息 - 时间：

# issue.fields.created = {str} "2022-08-11T06:24:16.440+0000"
# issue.fields.updated = {str}


# API Functions

# jira.add_issues_to_epic("GCBCS-6735", ["GCBCS-6767"])
