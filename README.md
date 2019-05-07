# dummy-blockchain

[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

> Dummy blockchain implementation.

An implementation of a dummy blockchain with some very basic methods for mining blocks, registering nodes and resolving conflicts.

## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [Support](#support)
- [Contributing](#contributing)
- [License](#license)


## Install
- Clone the repository and enter the project directory.

- Create your virtual environment and install the required dependencies:

```
virtualenv -p `which python` venv
source venv/bin/activate
pip install Flask
pip install requests
```

## Usage
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

## Support
If you're having any problem, please raise an issue on GitHub.

## Contributing
PRs accepted. Some general guidelines:

- Write a concise commit message explaining your changes.
- If applies, write more descriptive information in the commit body.
- Refer to the issue/s your pull request fixes (if there are issues in the github repo).
- Write a descriptive pull request title.
- Squash commits when possible.

Before your pull request can be merged, the following conditions must hold:

- All the tests passes (if any).
- The coding style aligns with the project's convention.
- Your changes are confirmed to be working.

Small note: If editing the Readme, please conform to the [standard-readme](https://github.com/RichardLitt/standard-readme) specification.

## License
The project is licensed under the MIT license.
