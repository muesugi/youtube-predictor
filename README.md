# youtube-predictor
CS1951A Data Science

## Getting Started:
#### Install Google Cloud sdk:
1. [might not need] download sdk from <a href="https://cloud.google.com/sdk/docs/">https://cloud.google.com/sdk/docs/</a>
2. [might not need] double click `install.sh` to install 
3. run `curl https://sdk.cloud.google.com | bash`, follow commands to install. Will need to authenticate via browser and then choose a project. Once it tells you in the browser that you're authenticated,
4. re-run `curl https://sdk.cloud.google.com | bash`

## Running the Downloader:
#### Invoke the proxy:
`./cloud_sql_proxy -instances=youtube-data-science-233522:us-east4:youtubepredictor=tcp:3305 &` (keep this open in a separate terminal window)

#### Run the file: Command-line arguments recommended
* if you have a channel id: `python3 youtube_download.py -c <channel-id>`
* if you have a user id: `python3 youtube_download.py -u <user-id>`

If you have multiple channel or user ids, you can now run them all at once! Use youtube\_multiple\_download.py instead.
ie; `python3 youtube_multiple_download.py -c <channel-id1> <channel-id2> -u <user-id1>`
