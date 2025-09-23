import os
import concurrent.futures
import threading
from typing import List, Any, Optional
import logging


# Configure logging to see which thread processes which file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(threadName)s - %(message)s'
)


def get_workers_count(multiplier = 1.0):
    """
    Get the number of CPU cores available.
    If CPU count fails to be determined, fallback value is 4.

    Note for threading vs multiprocessing:
    - Threading: For I/O-bound tasks (file reading), you can often use 2-4x more threads
                 than CPU cores since threads spend time waiting for disk I/O
    - Multiprocessing: For CPU-bound tasks, stick closer to the actual CPU core count

    Since file processing is likely I/O-bound, using 1.5-2x the CPU count for threads
    is often optimal. But(!) make sure the bottle neck really is I/O ops and not some
    image processing on the just opened files (in which case it becomes CPU-bound).
    """
    cpu_count = os.cpu_count()
    if cpu_count is None:
        return 4  # Fallback default
    return max(1, int(multiplier * cpu_count))



# setup for multithreaded processing:
#
# list of input "data"           -- can be a tuple data+params, or just (several) params
# list of output "data"          -- initialized with Nones,
#                                   at least flag that the given position has been processed
# process_fun(index_to_the_list) -- a routine that consumes input "data" at 'index_to_the_list',
#                                   "processes" it and returns a result (or at least a flag)
#                                   to the output "data" at 'index_to_the_list'

def example_process_item(input: Any) -> Any:
    logging.info(f"active thread {threading.current_thread().name} working on:  {input}")
    # this will become the output; in this case it works merely as a flag
    return "resolved"


def process_with_multithreading(inputs: List[Any],
                                process_fun,
                                num_threads: int,
                                thread_names: str = 'pyProcessors',
                                timeout: Optional[float] = None) -> List[Any]:
    """
    Process 'inputs' items, each item consumed with 'process_fun()', using a
    thread pool of size 'num_threads', but wait no longer than 'timeout' seconds.
    Thread workers can be optionally labeled with 'thread_names'.
    Default waiting time is 'None' -- meaning infinity, no set timeout.

    Returns:
        List of 'outputs' (can be either a flag) from processing each 'input' item.
    """
    outputs = [ None for _ in range(len(inputs)) ]

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads,
                                               thread_name_prefix=thread_names) as executor:

        # Submit all tasks to the executor, noting done to where outputs shall belong
        future_to_index = { executor.submit(process_fun, inputs[index]): index  for index in range(len(inputs)) }

        # Collect results as they complete
        try:
            for future in concurrent.futures.as_completed(future_to_index, timeout=timeout):
                index = future_to_index[future]
                try:
                    outputs[index] = future.result()
                except Exception as e:
                    logging.error(f"Exception occurred while fetching result for index {index}: {e}")
                    outputs[index] = ('FAIL', str(e))

        except concurrent.futures.TimeoutError:
            logging.error(f"Operation timed out after {timeout} seconds")
            # Cancel remaining futures (doesn't hurt to cancel already finished ones...)
            for future in future_to_index: future.cancel()

    return outputs



def example():
    files_to_process = [
        "file1.txt",
        "file2.txt",
        "file3.txt",
        "data/file4.txt",
        "logs/file5.txt"
    ]

    def file_processor(fn:str):
        logging.info(f"active thread {threading.current_thread().name} on process {os.getpid()} working on:  {input}")
        return 'seen '+fn

    # Number of worker threads
    NUM_THREADS = get_workers_count(0.8)
    NUM_THREADS = 3

    outputs = process_with_multithreading(files_to_process, file_processor, NUM_THREADS, timeout=3)
    for o in outputs: print("status:",o)


def example__very_simple_files_processor(file_list: List[str], num_threads: int) -> List[Any]:
    """
    Alternative, simplified implementation using executor.map() - good when
    you don't need per-task error handling or timeout control.
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        # 'process_file' probably takes items from the 'file_list', and
        # its products are appended() to form an output list 'results'
        #
        # the processing order (and thus the order of appearance in the results) is not guaranteed!
        results = list(executor.map(process_file, file_list))
    return results

