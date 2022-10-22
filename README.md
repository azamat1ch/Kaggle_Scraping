### Scraping Kaggle profiles with TOR browser
This is a script to scrape Kaggle user profiles. It uses TOR browser, which helps to avoid getting blocked when scraping.

Why a webscraper can be blocked?

* IPs are blocked: when scraping, your IP address can be seen. An unusually high amount of requests coming from the same IP will be blocked.
* No User Agents or User Agents are blocked: A user agent tells the server which web browser is being used, for example, “Mozilla/5.0 (X11; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0”. If the user agent is not set, the server won’t allow access. If an unusually high amount of requests coming from the same user agent, it will be blocked.
* The same user login requested too many times.

**With TOR we can change our IP address each time we get a HTTP error code.**

###  Usage
1.	Download [TOR Browser](https://www.torproject.org/download/) , [Installation guide](https://tb-manual.torproject.org/installation/)

2.	Edit **Torrc** file to open 9051 port

    WARNING: Do NOT follow random advice instructing you to edit your **torrc**! Doing so can allow an attacker to compromise your security and anonymity through malicious configuration of your **torrc**. The **torrc** is in the Tor Browser Data directory at Browser/TorBrowser/Data/Tor inside your Tor Browser directory. Add those lines to the torcc file:
    1.	ControlPort 9051
    2.	HashedControlPassword 16:05834BCEDD478D1060F1D7E2CE98E9C13075E8D3061D702F63BCD674DE
    
    This hashed password corresponds to “password” string. For different password, you will need different hash.

3. Install required packages and run python script.  
    a.	pip install stem (https://pypi.org/project/stem/) 

    b.	pip install fake-useragent (https://pypi.org/project/fake-useragent/)Run

### Useful Links
* https://stackoverflow.com/questions/30286293/make-requests-using-python-over-tor
* https://medium.com/analytics-vidhya/use-tor-to-avoid-getting-blocked-when-scraping-704c360cb7d1