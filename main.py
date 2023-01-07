from web3 import Web3
import pandas as pd
from datetime import datetime
import time
import streamlit as st  # data web app development
import yaml

# App
st.set_page_config(
    page_title="veTHE Checker",
    page_icon="icons/thena.png",
    layout="wide",
)

# Params
params_path = "params.yaml"


def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


config = read_params(params_path)

# Title
st.title("veTHE Checker")

tokenid = st.number_input("Your veTHE Token ID", min_value=1, format="%d")

# Read Data
try:
    provider_url = config["data"]["provider_url"]
    w3 = Web3(Web3.HTTPProvider(provider_url))

    abi = config["data"]["abi"]
    contract_address = config["data"]["contract_address"]

    contract_instance = w3.eth.contract(address=contract_address, abi=abi)

    # Balance veTHE
    bal = round(
        contract_instance.functions.balanceOfNFT(tokenid).call() / 1000000000000000000,
        2,
    )

    # Locked veTHE
    locked = round(
        contract_instance.functions.locked(tokenid).call()[0] / 1000000000000000000, 2
    )

    # Lock End Date
    lockend = time.strftime(
        "%Y-%m-%d",
        time.localtime(int(contract_instance.functions.locked(tokenid).call()[1])),
    )

    # Voted Last Epoch
    voted = contract_instance.functions.voted(tokenid).call()

    # creating a single-element container
    placeholder = st.empty()

    st.markdown("🔒 Locked THE: " + str(locked))

    st.markdown("🧾 veTHE Balance: " + str(bal))

    st.markdown("⏲️ Lock End Date: " + str(lockend))

    st.markdown("🗳️ Voted: " + ["Yes" if voted == True else "No"][0])

except Exception as e:
    print(e)
    st.markdown("Error Please Try Again")
