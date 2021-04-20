
## These are the steps you need to run in manual mode ( and are executed by the CI automatically)

1. run `source sourcefile`
2. run `bash chrome.sh`
3. run `pip3 install -r requirements.txt`. incase of error run `pip3 install BeautifulSoup4 lxml selenium requests fake_useragent`

4. run `python3 scratch_pad/prothomalo_links.py` to fetch latest story links
5. run `python3 scrapers/bulk_crawl_prothomalo.py` to make each stories
6. run `python3 scratch_pad/link_make.py` to update README with new story links