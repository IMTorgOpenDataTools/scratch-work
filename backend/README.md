# Examples


### Flask: basic

View on `http://127.0.0.1:5000`

```
python3 -m flask --app flask_simple.py run
```


### Flask: static files

View on `http://127.0.0.1:5000/static/index.html`

```
python3 -m flask --app flask_static.py run
```


### Flask: website url to pdf


Install `pyppeteer` dependencies by installing chromium, [ref](https://stackoverflow.com/questions/57217924/pyppeteer-errors-browsererror-browser-closed-unexpectedly):

* check dependencies needed with: `ldd ~/.local/share/pyppeteer/local-chromium/588429/chrome-linux/chrome | grep 'not found'`
* install chromium

```
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update 
sudo apt install google-chrome-stable
```

Install `wkhtmltopdf` using:

* get os version `cat /etc/os-release`
* download the correct wkhtmltopdf: `https://wkhtmltopdf.org/downloads.html`
* steps to [install](https://computingforgeeks.com/install-wkhtmltopdf-on-ubuntu-debian-linux/)
* env vars may be needed: `source .bashrc`, [notes](https://stackoverflow.com/questions/59790350/qstandardpaths-xdg-runtime-dir-not-set-defaulting-to-tmp-runtime-aadithyasb)

Install GoogleAPI: `pipenv run pip install git+https://github.com/abenassi/Google-Search-API`

TODO:determin how to do this^^^ with pipenv.  This doesn't seem to work: `pipenv install -e  git+https://github.com/abenassi/Google-Search-API.git@main#egg=googlepai`


View on `http://127.0.0.1:5000/static/latest/Tool_v*.*.html`

```
python3 -m pipenv shell
python3 -m flask --app flask_vue_api.py run
```