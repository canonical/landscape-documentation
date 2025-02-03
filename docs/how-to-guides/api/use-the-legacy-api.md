(how-to-guides-api-use-the-legacy-api)=
# How to use the legacy API


Landscape's API lets you perform many Landscape tasks from the command line or a shell script, or a Python module. You can also use the API in HTTPS calls.

The only means to install Landscape API is via snap:
```
sudo snap install landscape-api
```
Once the `landscape-api` command is installed you can get help on all Landscape API commands by typing: 
```
landscape-api -h
```
Before you use Landscape API, you must retrieve your API credentials from the Landscape dashboard. Specifically, you will need to retrieve the API access key and API secret key. To do so, click on your account name in the upper right corner of the Landscape dashboard. The keys can be passed as command-line options, but it's easier to export them as a shell variable with commands like:
```
export LANDSCAPE_API_KEY="{API access key}"
export LANDSCAPE_API_SECRET="{API secret key}"
export LANDSCAPE_API_URI="https://{landscape-hostname}/api/"
```
If you use a custom Certificate Authority (CA), you also need to export the path to your certificate:
```
export LANDSCAPE_API_SSL_CA_FILE="/path/to/ca/file"
```

