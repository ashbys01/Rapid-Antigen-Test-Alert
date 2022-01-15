# Rapid-Antigen-Test-Alert
A script to scrape the https://findarat.com.au/ site to alert you via Pushover if a RAT test is in stock within X kilometers of your suburb reported within the last hour.

## Dependencies

 1. [chrome driver](https://sites.google.com/chromium.org/driver/) executable in your PATH variable
 2. Python3 with Selenium with msedge.selenium_tools, http.client and urllib, requests installed

## Usage

Clone the repo
```
git clone https://github.com/ashbys01/Rapid-Antigen-Test-Alert.git
```

Set your working directory to the repo
```
cd Rapid-Antigen-Test-Alert
```

Copy and modify the sample settings file
```
cp settings_sample.json settings.json
```

Firstly, acquire a 'Pushover User Key' from https://pushover.net/. Create a new application and aquire the applications 'API Token/Key'.
Add your suburb details. Note: all three parameters are required in order to only return one suburb.
Include the search raduis in Kms.
Wait timer is how long the script will wait for the site to load in seconds.
Refresh timer is how often (after searching through suburbs) that the script should restart in minutes.

Run the script (for bash based systems e.g. mac/linux/WSL)
```
./rat.py
```

Run the script (for windows) 
```
python3 rat.py
```

This has been tested to work in my system but there are numerous edge cases 
where this might fail.
 - Find a Rat changes their website.
 - Your IP is blocked

## Disclaimer:

 - For personal use only. 
 - Dont break the law or cause disruption using this.
 - Using automated scripts irresponsibily can cause booking loss, disruption of services etc. be careful and know what you are doing.
 - You are responsible for your actions.
