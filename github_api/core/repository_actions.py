from datetime import timedelta
from functools import lru_cache

import requests

from ..cli.env import HEADERS
from ..consts import GithubConclusion
from ..utils import between_datetime
from ..utils import is_before_date
from ..utils import log
from ..utils import parse_datetime


class ActionInfo:

    @property
    @lru_cache(1)
    def duration_seconds(self):
        return self.duration_time.total_seconds()

    @property
    @lru_cache(1)
    def total_billable_seconds(self):
        return self.total_billable_time.total_seconds()

    @property
    @lru_cache(1)
    def total_execution_seconds(self):
        return self.total_execution_time.total_seconds()


class ActionsAttribute:

    DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.000%z'

    def __init__(self, args, gh, repo):
        self.args = args
        self.gh = gh
        self.repo = repo

    def get_run_timing(self, run):
        total_milliseconds = 0
        timing = run.timing()
        for platform in timing.billable.values():
            milliseconds = platform.get('total_ms', 0)
            total_milliseconds += milliseconds
        total_seconds = total_milliseconds / 1000
        return {
            'total_billable_time': timedelta(seconds=total_seconds),
            'duration_time': timedelta(seconds=timing.run_duration_ms / 1000),
        }

    def get_job_steps_info(self, job):
        total_milliseconds = 0
        steps = job.get('steps', [])
        for step in steps:
            s_completed_at = step.get('completed_at')
            s_started_at = step.get('started_at')
            if (s_completed_at is None or s_started_at is None):
                milliseconds = 0
            else:
                completed_at = parse_datetime(s_completed_at, self.DATE_FORMAT)
                started_at = parse_datetime(s_started_at, self.DATE_FORMAT)
                execution_time = completed_at - started_at
                milliseconds = execution_time.total_seconds() * 1000
            if milliseconds == 0:
                # FIXME: handle as 1 second since no milliseconds in steps
                # https://github.com/kazamori/github-api-tools/issues/2#issuecomment-1073051639
                milliseconds = 1000
            total_milliseconds += milliseconds
        total_seconds = timedelta(seconds=total_milliseconds / 1000)
        return {
            'name': job['name'],
            'steps': steps,
            'total_execution_time': total_seconds,
        }

    def get_workflow_jobs(self, jobs_url):
        r = requests.get(jobs_url, headers=HEADERS)
        data = r.json()
        for job in data['jobs']:
            yield job

    def get_workflow_actions(self):
        for run in self.repo.get_workflow_runs():
            if run.conclusion != GithubConclusion.SUCCESS.value:
                continue

            if not between_datetime(run.created_at,
                                    self.args.datefrom, self.args.dateto):
                log.debug(f'not between dates: {run.created_at}')
                if is_before_date(run.created_at, self.args.datefrom):
                    return
                continue

            workflow = self.repo.get_workflow(run.workflow_id)
            if (self.args.workflow_path is not None
                    and self.args.workflow_path != workflow.path):
                continue

            total_execution_time = timedelta()
            jobs = []
            for job in self.get_workflow_jobs(run.jobs_url):
                info = self.get_job_steps_info(job)
                jobs.append(info)
                total_execution_time += info['total_execution_time']

            if all(len(job['steps']) == 0 for job in jobs):
                # maybe no logs for some reason, so ignore
                continue

            run_timing = self.get_run_timing(run)

            info = ActionInfo()
            info.created_at = run.created_at
            info.duration_time = run_timing['duration_time']
            info.html_url = run.html_url
            info.id = run.id
            info.jobs = jobs
            info.total_billable_time = run_timing['total_billable_time']
            info.total_execution_time = total_execution_time
            info.updated_at = run.updated_at
            info.workflow_name = workflow.name
            info.workflow_path = workflow.path
            yield info

    def get_actions(self):
        for action in self.get_workflow_actions():
            log.info(f'workflow name: {action.workflow_name}')
            log.info(f'  - created at: {action.created_at}')
            log.info(f'  - url: {action.html_url}')
            log.debug(f' - path: {action.workflow_path}')
            log.debug(f' - execution time: {action.total_execution_time}')
            log.debug(f' - billable time: {action.total_billable_time}')
            log.debug(f' - duration time: {action.duration_time}')
            yield action

    def get_workflows(self):
        for workflow in self.repo.get_workflows():
            log.info(f'workflow name: {workflow.name}')
            log.info(f' - created at: {workflow.created_at}')
            log.info(f' - url: {workflow.html_url}')
            log.info(f' - path: {workflow.path}')
            log.info(f' - id: {workflow.id}')
