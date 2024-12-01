from threading import Thread
from queue import Queue as ThreadQueue
from multiprocessing import Process, Queue
import time

def search_keywords_in_file(file_path, keywords):
    try:
        with open(file_path, 'r') as file:
            results = {}
            for _, line in enumerate(file):
                for keyword in keywords:
                    if keyword in line:
                        if keyword not in results:
                            results[keyword] = []
                        results[keyword].append(file_path)
    except Exception as e:
        print(f"Error for {file_path}: {e}")
    return results

def search_keywords(file_paths, keywords, queue):
    for file_path in file_paths:
        results = search_keywords_in_file(file_path, keywords)
        queue.put(results)

def search_with_threads(file_paths, keywords):
    threads = []
    threads_qty = 2
    paths_batch_size = len(file_paths) // threads_qty
    queue = ThreadQueue()

    for i in range(threads_qty):
        paths_batch = file_paths[i * paths_batch_size:(i + 1) * paths_batch_size]
        thread = Thread(target=search_keywords, args=(paths_batch, keywords, queue))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    final_result = {}

    while not queue.empty():
        result = queue.get()
        for keyword, file_paths in result.items():
            for file_path in file_paths:
                final_result.setdefault(keyword, []).append(file_path)

    return final_result

def search_with_processes(file_paths, keywords):
    processes = []
    processes_qty = 2
    paths_batch_size =  len(file_paths) // processes_qty
    queue = Queue()

    for i in range(processes_qty):
        paths_batch = file_paths[i * paths_batch_size:(i + 1) * paths_batch_size]
        process = Process(target=search_keywords, args=(paths_batch, keywords, queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    final_result = {}

    while not queue.empty():
        result = queue.get()
        for keyword, file_paths in result.items():
            for file_path in file_paths:
                final_result.setdefault(keyword, []).append(file_path)

    return final_result


if __name__ == "__main__":
    keywords = ["Lorem", "literature", "European", "Alphabet", "standard"]
    file_paths = [f"test_files/{i}.txt" for i in list(map(chr, range(ord('a'), ord('j')+1)))]
    start = time.perf_counter()
    threasds_result = search_with_threads(file_paths, keywords)
    end = time.perf_counter()
    elapsed = end - start
    print('Threads result: ', threasds_result)
    print(f'Threads time taken: {elapsed:.6f} seconds')

    start = time.perf_counter()
    processes_result = search_with_processes(file_paths, keywords)
    end = time.perf_counter()
    elapsed = end - start
    print('Processes result: ', processes_result)
    print(f'Processes time taken: {elapsed:.6f} seconds')
