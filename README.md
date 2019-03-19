# dummy-blockchain

> An implementation of a dummy blockchain with some very basic methods for registering nodes and resolving conflicts


## Install
- Clone the repository and enter the project directory.

- Create your virtual environment and install the required dependencies:

```
virtualenv -p `which python` venv
source venv/bin/activate
pip install Flask
pip install requests
```

## Run
Run some nodes:

```
python blockchain.py --port 5000
```

```
python blockchain.py --port 5001
```

etc.

See the current chain of a node by making a `GET` request:

```
http://127.0.0.1:5000/chain
```

Create a new transaction (which will be included in a new mined block) by making a `POST` request:

```
http://localhost:5000/transactions/new
```

with a sample body:

```
{
  "sender": "d4eeekijg98598654oigjldekg",
  "recipient": "an-example-address",
  "amount": 100
}
```

Mine a new block by making a `GET` request:

```
http://127.0.0.1:5000/mine
```

Register a node by making a `POST` request:
```
http://127.0.0.1:5001/nodes/register
```

with a body:

```
{
  "nodes": ["http://127.0.0.1:5000"]
}
```

Tell the other node to reach consensus by making a `GET` request:

```
http://127.0.0.1:5001/nodes/resolve
```

## License
The project is licensed under the MIT license.
