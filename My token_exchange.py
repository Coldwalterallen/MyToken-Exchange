
from web3 import Web3

# Connect to a local Ethereum node
web3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

# Get the latest block number
latest_block = web3.eth.blockNumber
print("Latest block number:", latest_block)

# Get the balance of an Ethereum address
address = "0x1234567890abcdef"
balance = web3.eth.getBalance(address)
print("Balance:", web3.fromWei(balance, 'ether'), "ETH")
```

Developing a smart contract using Solidity:

```solidity
// Define a simple ERC20 token contract
contract MyToken {
    string public name;
    string public symbol;
    uint8 public decimals;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;

    event Transfer(address indexed from, address indexed to, uint256 value);

    constructor(uint256 _totalSupply) public {
        name = "MyToken";
        symbol = "MYT";
        decimals = 18;
        totalSupply = _totalSupply;
        balanceOf[msg.sender] = _totalSupply;
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        require(balanceOf[msg.sender] >= _value);
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }
}
```

Building a web interface using Flask:

```python
from flask import Flask, render_template, request
from web3 import Web3

app = Flask(__name__)

# Connect to a local Ethereum node
web3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

# Load the smart contract ABI
with open('MyToken.abi') as f:
    abi = f.read()

# Load the smart contract bytecode
with open('MyToken.bin') as f:
    bytecode = f.read()

# Deploy the smart contract
MyToken = web3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = MyToken.constructor(1000000).transact()
tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
contract_address = tx_receipt.contractAddress

@app.route('/')
def index():
    # Get the balance of the contract address
    balance = web3.eth.getBalance(contract_address)
    balance_eth = web3.fromWei(balance, 'ether')
    # Render the template with the balance
    return render_template('index.html', balance_eth=balance_eth)

@app.route('/transfer', methods=['POST'])
def transfer():
    # Get the form data
    to_address = request.form['to_address']
    amount_eth = float(request.form['amount_eth'])
    # Convert ETH to Wei
    amount_wei = int(amount_eth * 1e18)
    # Transfer tokens to the specified address
    MyToken.functions.transfer(to_address, amount_wei).transact()
    # Redirect back to the index page
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
