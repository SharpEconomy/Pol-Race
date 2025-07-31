# POL Race

POL Race is a car racing game that integrates a simple Polygon wallet using [Web3.py](https://github.com/ethereum/web3.py). Players pay a small entry fee in MATIC and the winner receives a reward.

## Installation

Clone the repository and install the requirements:

```bash
git clone <repo-url>
cd Pol-Race
pip install -r requirements.txt
```

Set the environment variable `ALCHEMY_POLYGON_RPC_URL` with your Alchemy Polygon mainnet RPC endpoint and start the server:

```bash
export ALCHEMY_POLYGON_RPC_URL="https://polygon-mainnet.g.alchemy.com/v2/YOUR_KEY"
python manage.py runserver
```

Open `UNITY/The Strax Race/index.html` to play the game. The web wallet can be accessed through the in‑game interface.

**Note:** To play you will need some MATIC in the generated wallet.
