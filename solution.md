## Solition

### Approach:
  - Miner
    - Generate a hash with the subnet data received and random number to include four zeros at the beginning of the hash
    - Use the `sha512` algorithm by default but is possible to genrate hash with different algorithms
    - Hability to generate a multiple hash values with all available hash algorithms
  - Validator
    - Send the data to the miner (`step` in this case) and `time_elapse` to use as a time_out.
    - Sort the responses by the `execution_time` and then sent to the reward method to defined the amount
  - Reward
    - Set a reward in amount between 0-1, and check if the hash sent by the miner is apropiate
    - Check the number of zeros in the hash and set the reward amount depend of number of zeros
  - Dummy - Protocol
    - Define the data time that we pass between the `Validator` and `Miner`
      
