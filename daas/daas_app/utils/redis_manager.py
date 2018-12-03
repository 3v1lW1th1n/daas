from .singleton import ThreadSafeSingleton
from rq import Queue
from redis import Redis
from .configuration_manager import ConfigurationManager
from ..tests.mocks.redis_job import MockJob


class RedisManagerException(Exception):
    pass


class RedisManager(metaclass=ThreadSafeSingleton):
    def __init__(self):
        self.connection = Redis(host='daas_redis_1')
        self.worker_path = 'decompilers.worker.worker'
        self.queues = {}
        for configuration in ConfigurationManager().get_configurations():
            # We need only one Queue per config, so this should be in the init to
            # ensure that no duplicated Queue instances will be created.
            self.queues[configuration.identifier] = Queue(configuration.queue_name,
                                                          connection=self.connection)

    def get_queue(self, identifier):
        return self.queues[identifier]

    def get_job(self, identifier, job_id):
        return self.get_queue(identifier).fetch_job(job_id)

    def submit_sample(self, sample):
        configuration = ConfigurationManager().get_config_for_sample(sample)
        if configuration is not None:
            queue = self.get_queue(configuration.identifier)
            job = queue.enqueue(self.worker_path,
                                args=({'sample': sample, 'config': configuration.as_dictionary()},),
                                timeout=configuration.timeout + 60)
            return configuration.identifier, job.id
        else:
            raise RedisManagerException('No filter for the given sample')

    def cancel_job(self, identifier, job_id):
        job = self.get_job(identifier, job_id)
        if job is not None:
            job.cancel()

    """ Test methods: """
    def __mock__(self, identifier='pe', job_id='i-am-a-job'):
        self.__mock_job = MockJob()
        self.__mock_identifier = identifier
        self.__mock_job_id = job_id
        self.get_job = lambda x=None, y=None: self.__mock_job
        self.submit_sample = self.__submit_sample_mock__
        self.cancel_job = lambda x=None, y=None: None

    def __submit_sample_mock__(self, sample):
        if ConfigurationManager().get_config_for_sample(sample) is not None:
            return self.__mock_identifier, self.__mock_job_id
        else:
            raise RedisManagerException('No filter for the given sample')
