# youtube-predictor
CS1951A Data Science

## Getting Started:
#### install Google Cloud sdk:
1. [might not need] download sdk from <a href="https://cloud.google.com/sdk/docs/">https://cloud.google.com/sdk/docs/</a>
2. [might not need] double click `install.sh` to install 
3. run `curl https://sdk.cloud.google.com | bash`, follow commands to install. Will need to authenticate via browser and then choose a project.

## Running the Downloader:
#### invoke the proxy:
`./cloud_sql_proxy -instances=youtube-data-science-233522:us-east4:youtubepredictor=tcp:3305 &` (keep this open in a separate terminal window)

#### run the file:
`python3 youtube_download.py` -- be sure to change the user/channel id in question before running!