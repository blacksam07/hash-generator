# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# TODO(developer): Set your name
# Copyright © 2023 <your name>

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from hashlib import sha512
import torch
from typing import List


def reward(query: int, response: object) -> float:
    """
    Reward the miner response to the dummy request. This method returns a reward
    value for the miner, which is used to update the miner's score.

    Returns:
    - float: The reward value for the miner.
    """
    reward: float = 1.0
    if response is None:
        return 0

    # Check the requirement that contain the number of zeros taht we need
    # and check the response based on the nonce
    if response and response["hash"].startswith("0000"):
        encoded = sha512(response["nonce"].encode()).hexdigest()
        if response["hash"] == encoded:
            return reward
        else:
            return reward / 2
    elif response and response["hash"].startswith("0"):
        # Check the number of zeros that miner found and set a reward based on that
        zero_count = len(response["hash"]) - len(response["hash"].lstrip('0'))
        return reward * (zero_count * 0.01)
    else:
        return 0


def get_rewards(
    self,
    query: int,
    responses: List[float],
) -> torch.FloatTensor:
    """
    Returns a tensor of rewards for the given query and responses.

    Args:
    - query (int): The query sent to the miner.
    - responses (List[objects]): A list of responses from the miner.

    Returns:
    - torch.FloatTensor: A tensor of rewards for the given query and responses.
    """
    # Get all the reward results by iteratively calling your reward() function.
    # Sort all miner response to get the faster response
    # filter_responses = list(filter(lambda item: item is not None, responses))
    # sorted_response = sorted(responses, key=lambda res: res["execution_time"])
    return torch.FloatTensor(
        [reward(query, response) for response in responses]
    ).to(self.device)
