print("=" * 50)
print(" Script by richbrianx")
print("=" * 50)

from web3 import Web3
import re
import time

# === RPC AND WEB3 SETUP ===
rpc_url = "https://carrot.megaeth.com/rpc"
w3 = Web3(Web3.HTTPProvider(rpc_url))

if not w3.is_connected():
    print("Failed to connect to MegaETH RPC!")
    exit()

# === LOAD PRIVATE KEYS ===
with open('pk.txt', 'r') as f:
    private_keys = f.read().splitlines()

print(f"Total private keys found: {len(private_keys)}\n")

# === TOKEN CONTRACTS AND ABI ===
contracts = {
    "MegaETH":  {"address": "0x10a6be7d23989d00d528e68cf8051d095f741145", "decimals": 18},
    "cUSD":     {"address": "0xE9b6e75C243B6100ffcb1c66e8f78F96FeeA727F", "decimals": 18},
    "tkETH":    {"address": "0x176735870dc6C22B4EBFBf519DE2ce758de78d94", "decimals": 18},
    "tkUSDC":   {"address": "0xFaf334e157175Ff676911AdcF0964D7f54F2C424", "decimals": 6},
    "tkWBTC":   {"address": "0xF82ff0799448630eB56Ce747Db840a2E02Cde4D8", "decimals": 8},
}

token_abi = [
    {
        "constant": True,
        "inputs": [{"name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"name": "to", "type": "address"},
            {"name": "value", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# === FUNCTIONS ===
def get_balance_of(contract_address, from_address, retry=3):
    contract = w3.eth.contract(address=contract_address, abi=token_abi)
    for attempt in range(retry):
        try:
            return contract.functions.balanceOf(from_address).call()
        except Exception as e:
            print(f"[!] Failed to get balance. Attempt {attempt + 1}: {e}")
            time.sleep(1.5 * (attempt + 1))
    return 0

def wei_to_token(balance, decimals):
    return balance / 10**decimals

def send_token(private_key, contract_address, to_address, amount, decimals, token_name):
    account = w3.eth.account.from_key(private_key)
    from_address = account.address

    contract = w3.eth.contract(address=contract_address, abi=token_abi)

    try:
        gas_estimate = contract.functions.transfer(to_address, amount).estimate_gas({'from': from_address})
        gas_price = w3.eth.gas_price
        nonce = w3.eth.get_transaction_count(from_address)
        gas_limit = gas_estimate + 10000

        tx = contract.functions.transfer(to_address, amount).build_transaction({
            'chainId': 6342,
            'gas': gas_limit,
            'gasPrice': gas_price,
            'nonce': nonce,
            'from': from_address
        })

        signed_tx = w3.eth.account.sign_transaction(tx, private_key)

        # Show raw transaction hex
        raw_data = signed_tx.raw_transaction.hex()
        print(f"[{token_name}] Raw transaction data: {raw_data}")

        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        hash_hex = w3.to_hex(tx_hash)

        print(f"✅ Success! Sent from {from_address} to {to_address}. TX Hash: {hash_hex}")
        with open("log_success.txt", "a") as log:
            log.write(f"{from_address} => {to_address} | {token_name} | {hash_hex}\n")
        return True
    except Exception as e:
        print(f"❌ Failed to send from {from_address} ({token_name}): {e}")
        with open("log_error.txt", "a") as log:
            log.write(f"{from_address} ({token_name}) ERROR: {e}\n")
        return False

# === GET RECIPIENT ADDRESS ===
to_address = input("Enter the recipient wallet address: ").strip()

# === PROCESS EACH PRIVATE KEY ===
for private_key in private_keys:
    private_key = private_key.strip()
    if not re.fullmatch(r"0x[0-9a-fA-F]{64}", private_key):
        print(f"[!] Invalid private key format: {private_key}. Skipped.")
        continue

    account = w3.eth.account.from_key(private_key)
    from_address = account.address
    print(f"\n🔍 Checking balances for: {from_address}\n")

    has_balance = False
    balances = {}

    for token_name, token_info in contracts.items():
        contract_address = Web3.to_checksum_address(token_info["address"])
        raw_balance = get_balance_of(contract_address, from_address)
        display_balance = wei_to_token(raw_balance, token_info["decimals"])
        balances[token_name] = (raw_balance, display_balance)

        print(f"{token_name}: {display_balance} ({raw_balance} {token_name})")

        if raw_balance > 0:
            has_balance = True

    if not has_balance:
        print(f"⚠️ No balance found in {from_address}. Skipping.")
        continue

    for token_name, token_info in contracts.items():
        raw_balance, display_balance = balances[token_name]
        if raw_balance > 0:
            print(f"\n🚚 Sending {display_balance} {token_name} from {from_address} to {to_address}")
            send_token(private_key, Web3.to_checksum_address(token_info["address"]), to_address, raw_balance, token_info["decimals"], token_name)
            time.sleep(1.2)  # Avoid rate limits
