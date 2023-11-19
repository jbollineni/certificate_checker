# certificate_checker

## Introduction 

Python script to get TLS certificate information from endpoints and generate a HTML document.

Sample
![certinfo](/assets/img/cert_info.png)

## How to?

### Clone the repo

```bash
git@github.com:jbollineni/certificate_checker.git
cd certificate_checker
```
### Create and activate a python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install python packages

```python
pip install -r requirements.txt
```

### Run Script

Add FQDNs to the `fqdn_list.yml` file and then run the script.

```bash
python certchecker.yml
```