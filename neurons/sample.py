import hashlib
import time

def hashing_data(data: str, time_elapse: int):
    start_time = time.monotonic()
    hashes = []
    if data is None:
        print("Empty data to process..")
        return hashes

    time_end = start_time + time_elapse
    for hash_method in hashlib.algorithms_available:
        try:
            if time.monotonic() > time_end:
                print("finish time")
                break

            response = generate_hash(data, time_elapse, hash_method=hash_method)
            hashes.append(response)
        except:
            continue

    execution_time = time.monotonic() - start_time

    return { "response": hashes, "execution_time": execution_time }

def generate_hash(data: int, time_elapse: int, hash_method = "sha512"):
    start_time = time.monotonic()
    hashed_data = ""
    nonce = ""
    iteration = 0

    time_end = start_time + time_elapse
    if data is None:
        print("Empty data to process..")
        return None

    while not hashed_data.startswith("000"):
        if time.monotonic() > time_end:
            print("finish time")
            break

        nonce = f"{data}{iteration}"
        algorithm = hashlib.new(hash_method)
        algorithm.update(nonce.encode())
        hashed_data = algorithm.hexdigest()
        iteration += 1

    execution_time = time.monotonic() - start_time

    return { "hash": hashed_data, "nonce": nonce,  "execution_time": execution_time }


# miner_uids = get_random_uids(self, k=self.config.neuron.sample_size)

# axons = [self.metagraph.axons[uid] for uid in miner_uids]