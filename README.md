# intellinet-pdu-exporter
Prometheus Exporter to extract the data of Intellinet 19" Intelligent 8-Port PDUs and publish them in a format compatible for Prometheus.

## Installation
Initialize the Python Virtual Environment first.

```
jgilla@Zerberus % bash initialize.sh
Dropping old environment...
Recreate new virtual environment...
Install requirements...
Collecting certifi==2022.9.24
  Using cached certifi-2022.9.24-py3-none-any.whl (161 kB)
Collecting charset-normalizer==2.1.1
  Using cached charset_normalizer-2.1.1-py3-none-any.whl (39 kB)
Collecting idna==3.4
  Using cached idna-3.4-py3-none-any.whl (61 kB)
Collecting prometheus-client==0.14.1
  Using cached prometheus_client-0.14.1-py3-none-any.whl (59 kB)
Collecting PyYAML==6.0
  Using cached PyYAML-6.0.tar.gz (124 kB)
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
    Preparing wheel metadata ... done
Collecting requests==2.28.1
  Using cached requests-2.28.1-py3-none-any.whl (62 kB)
Collecting urllib3==1.26.12
  Using cached urllib3-1.26.12-py2.py3-none-any.whl (140 kB)
Collecting xmltodict==0.13.0
  Using cached xmltodict-0.13.0-py2.py3-none-any.whl (10.0 kB)
Building wheels for collected packages: PyYAML
  Building wheel for PyYAML (PEP 517) ... done
  Created wheel for PyYAML: filename=PyYAML-6.0-cp38-cp38-macosx_10_14_arm64.whl size=45338 sha256=ba4e63062003c3be2ed32f644bad066dc9dbdaed80a43c5efa94072c362dcb46
  Stored in directory: /Users/jgilla/Library/Caches/pip/wheels/52/84/66/50912fd7bf1639a31758e40bd4312602e104a8eca1e0da9645
Successfully built PyYAML
Installing collected packages: certifi, charset-normalizer, idna, prometheus-client, PyYAML, urllib3, requests, xmltodict
Successfully installed PyYAML-6.0 certifi-2022.9.24 charset-normalizer-2.1.1 idna-3.4 prometheus-client-0.14.1 requests-2.28.1 urllib3-1.26.12 xmltodict-0.13.0
WARNING: You are using pip version 20.2.3; however, version 22.2.2 is available.
You should consider upgrading via the '/Users/jgilla/Documents/Visual Studio Code/intellinet_pdu_exporter/.venv/bin/python3 -m pip install --upgrade pip' command.
Initialization finished! Activate virtual environment via: source .venv/bin/activate
```

Update the [configuration-file](configuration.yml) to include the IP-addresses to your PDUs and customize the other options in case needed. As the status-file is world-readable, there is no need to know the credentials of the PDU 🤦.