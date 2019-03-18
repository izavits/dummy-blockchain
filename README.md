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


## License
The project is licensed under the MIT license.
