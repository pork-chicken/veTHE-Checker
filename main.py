from web3 import Web3
import time
import streamlit as st
import yaml
import requests

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

# THE Price
params = {
    "from": "0xF4C8E32EaDEC4BFe97E0F595AdD0f4450a863a11",
    "to": "0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56",
    "amount": "1000000000000000000",
}

try:
    response = requests.get("https://router.firebird.finance/bsc/route", params=params)
    THE_price = round(
        response.json()["maxReturn"]["tokens"][
            "0xf4c8e32eadec4bfe97e0f595add0f4450a863a11"
        ]["price"],
        2,
    )
except Exception as e:
    print(e)

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

    # Total Supply
    totalSupply = contract_instance.functions.totalSupply().call() / 1000000000000000000

    # creating a single-element container
    placeholder = st.empty()

    # Empty Placeholder Filled
    with placeholder.container():
        if tokenid:
            st.markdown("🔒 Locked THE: " + str(locked))
            st.markdown("🧾 veTHE Balance: " + str(bal))
            st.markdown("🤑 Estimated BUSD Value: $" + str(THE_price * locked))
            st.markdown("⏲️ Lock End Date: " + str(lockend))
            st.markdown(
                "🗳️ Vote Share: " + str(round(bal / totalSupply * 100, 4)) + "%"
            )
            st.markdown("✔️ Vote Reset: " + ["No" if voted == True else "Yes"][0])

    # Note
    st.markdown("#")
    st.markdown("#")
    st.caption(
        """
NFA, DYOR -- This web app is in beta, I am not responsible for any information on this page.
        
BUSD Value is just an estimate of THE Price pulled from Firebird API.
        
:red[If "Vote Reset" is No you cannot sell your veTHE unless you reset your vote.]
        """
    )

except Exception as e:
    print(e)
    st.markdown("Error Please Try Again")
