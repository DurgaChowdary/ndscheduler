"""Base class for a job."""

import logging
import os
import socket

from ndscheduler import constants
from ndscheduler import utils
from ndscheduler.core import scheduler_manager
from ndscheduler import url_request
from ndscheduler.server.handlers import jobs


logger = logging.getLogger(__name__)


class JobBase:

    def __init__(self, job_id, execution_id):
        self.job_id = job_id
        self.execution_id = execution_id

    @classmethod
    def create_test_instance(cls):
        """Creates an instance of this class for testing."""
        return cls(None, None)

    @classmethod
    def get_scheduled_description(cls):
        # Returns string containing the hostname of the machine where the Python interpreter is currently exevuting
        hostname = socket.gethostname()
        pid = os.getpid()
        return 'hostname: %s | pid: %s' % (hostname, pid)

    @classmethod
    def get_scheduled_error_description(cls):
        return utils.get_stacktrace()

    @classmethod
    def get_running_description(cls):
        hostname = socket.gethostname()
        pid = os.getpid()
        return 'hostname: %s | pid: %s' % (hostname, pid)

    @classmethod
    def get_failed_description(cls):
        
        return utils.get_stacktrace()

    @classmethod
    def get_succeeded_description(cls):
        hostname = socket.gethostname()
        pid = os.getpid()
        
        return 'hostname: %s | pid: %s' % (hostname, pid)

    @classmethod
    def meta_info(cls):
        """Returns meta info for this job class.

        For example:
            {
                'job_class_string': 'myscheduler.jobs.myjob.MyJob',
                'arguments': [
                    {'type': 'string', 'description': 'name of this channel'},
                    {'type': 'string', 'description': 'what this channel does'},
                    {'type': 'int', 'description': 'created year'}
                ],
                'example_arguments': '["music channel", "it's an awesome channel", 1997]',
                'notes': 'need to specify environment variable API_KEY first'
            }
        The arguments property should be consistent with the run() method.

        This info will be used in web ui for explaining what kind of arguments is needed for a job.

        You should override this function if you want to make your scheduler web ui informative :)

        :return: meta info for this job class.
        :rtype: dict
        """
        return {
            'job_class_string': '%s.%s' % (cls.__module__, cls.__name__),
            'arguments': [],
            'example_arguments': '',
            'notes': ''
        }

    @classmethod
    def run_job(cls, job_id, execution_id, *args, **kwargs):
        """Wrapper to run this job.

        It updates the execution state, i.e., running, succeeded or failed.

        :param str job_id: Job id.
        :param str execution_id: Execution id.
        :param args:
        :param kwargs:
        """
        scheduler = scheduler_manager.SchedulerManager.get_instance()
        datastore = scheduler.get_datastore()
        try:
            
            datastore.update_execution(execution_id, state=constants.EXECUTION_STATUS_RUNNING,
                                       hostname=socket.gethostname(), pid=os.getpid(),
                                       description=cls.get_running_description())
            job = cls(job_id, execution_id)
            j = JobBase(job_id , execution_id)
            job.run(*args, **kwargs)
            datastore.update_execution(execution_id, state=constants.EXECUTION_STATUS_SUCCEEDED,
                                       description=cls.get_succeeded_description())
            
            """h = jobs.Handler()
            job1 = h._build_job_dict(j)
            job_name = job1['name']"""
            
            #jo = utils.get_cron_strings(j)
            job_name = url_request.jobname(str(job_id))
            url_request.callurl("Job ID : " + str(job_id)+"Job Name : "+ str(job_name)+ " : Success")
            
            
        except Exception as e:
            logger.exception(e)
            datastore.update_execution(execution_id,
                                       state=constants.EXECUTION_STATUS_FAILED,
                                       description=cls.get_failed_description())
            """h = jobs.Handler()
            job1 = h._build_job_dict(j)
            job_name = job1['name']"""
            #jo = utils.get_cron_strings(j)
            job_name = url_request.jobname(str(job_id))
            url_request.callurl("Job ID : " + str(job_id)+"Job Name : "+ str(job_name)+ " : Failure")
            
    def run(self, *args, **kwargs):
        """The "main" function for a job.

        Any subclass has to implement this function.

        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError('Please implement this function')
