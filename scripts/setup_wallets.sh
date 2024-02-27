#!/bin/bash

# Start a new tmux session and create a new pane, but do not switch to it
echo "FEATURES='pow-faucet runtime-benchmarks' BT_DEFAULT_TOKEN_WALLET=$(cat ~/.bittensor/wallets/$wallet/coldkeypub.txt | grep -oP '"ss58Address": "\K[^"]+') bash scripts/localnet.sh" >> setup_and_run.sh
chmod +x setup_and_run.sh
tmux new-session -d -s localnet -n 'localnet'
tmux send-keys -t localnet 'bash ../subtensor/setup_and_run.sh' C-m

wallet=owner

btcli subnet create --wallet.name $wallet --wallet.hotkey default --subtensor.chain_endpoint ws://127.0.0.1:9946 --no_prompt

export BT_VALIDATOR_TOKEN_WALLET=$(cat ~/.bittensor/wallets/validator/coldkeypub.txt | grep -oP '"ss58Address": "\K[^"]+')
export BT_MINER_TOKEN_WALLET=$(cat ~/.bittensor/wallets/miner/coldkeypub.txt | grep -oP '"ss58Address": "\K[^"]+')

btcli wallet transfer --subtensor.network ws://127.0.0.1:9946 --wallet.name $wallet --dest $BT_VALIDATOR_TOKEN_WALLET --amount 100 --no_prompt
btcli wallet transfer --subtensor.network ws://127.0.0.1:9946 --wallet.name $wallet --dest $BT_MINER_TOKEN_WALLET --amount 100 --no_prompt


# Register miner
btcli subnet register --wallet.name miner --netuid 1 --wallet.hotkey default --subtensor.chain_endpoint ws://127.0.0.1:9946 --no_prompt

# Reister the Validator
btcli subnet register --wallet.name validator --netuid 1 --wallet.hotkey default --subtensor.chain_endpoint ws://127.0.0.1:9946 --no_prompt

# Stake
btcli stake add --wallet.name validator --wallet.hotkey default --subtensor.chain_endpoint ws://127.0.0.1:9946 --amount 99 --no_prompt

# Run miner
python neurons/miner.py --netuid 1 --subtensor.chain_endpoint ws://127.0.0.1:9946 --wallet.name miner --wallet.hotkey default --logging.debug

# Run Validator
python neurons/validator.py --netuid 1 --subtensor.chain_endpoint ws://127.0.0.1:9946 --wallet.name validator --wallet.hotkey default --neuron.sample_size 1 --logging.debug

# Register Validator
btcli root register --wallet.name validator --wallet.hotkey default --subtensor.chain_endpoint ws://127.0.0.1:9946