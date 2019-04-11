from .decompiler_factory import DecompilerFactory
from .utils import send_result, get_sample


# This function should by called by redis queue (rq command).
def worker(task):
    decompiler = DecompilerFactory().create(task['config'])
    sample_id = task['sample_id']
    sample = get_sample(sample_id)
    result = decompiler.process(sample)
    send_result(result)
