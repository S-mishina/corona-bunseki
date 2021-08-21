# corona-bunseki
## 栃木県のコロナ発生状況を分析
栃木県のコロナ発生状況を分析するプログラムです.

## 動作環境

```
Macbook air(2020) intel python3.8
AWS Amazon Linax2 python3.7
```

## データセット
https://www.pref.tochigi.lg.jp/e04/welfare/hoken-eisei/kansen/hp/coronakensahasseijyoukyou.html

## データセットのファイル場所

```
data/
```
## アウトプットファイルの出力場所

```
output_data/
```
## 動作手順

```
1, みなさんが使っている環境（本プログラムはAWSを想定）にgit clone
2, pip list をインストール
3, bashファイルを実行
```

## 実行コマンド

```
./corona_bash.sh
```

## 注意点

### レポートを見る際の注意
このノートブック(アウトプット資料)は上記データセットに基づいて<br>
コードの内容で可視化を行っています.<br>
あくまでも参考程度にしていただけると幸いです.

### pushする際の注意
アウトプット資料（notebook）を更新する際に新しいライブラリを追加したら<br>

```
pip freeze > requirements.txt
```

を実施すること
実施しないと実行する際にライブラリがなく失敗する.

## notebookで使用しているpip list

```
appnope==0.1.2
attrs==21.2.0
backcall==0.2.0
bleach==4.0.0
certifi==2021.5.30
charset-normalizer==2.0.4
cycler==0.10.0
debugpy==1.4.1
decorator==5.0.9
defusedxml==0.7.1
entrypoints==0.3
et-xmlfile==1.1.0
idna==3.2
ipykernel==6.2.0
ipython==7.26.0
ipython-genutils==0.2.0
japanize-matplotlib==1.1.3
jedi==0.18.0
Jinja2==3.0.1
jsonschema==3.2.0
jupyter-client==7.0.1
jupyter-core==4.7.1
jupyterlab-pygments==0.1.2
kiwisolver==1.3.1
MarkupSafe==2.0.1
matplotlib==3.4.3
matplotlib-inline==0.1.2
mistune==0.8.4
nbclient==0.5.4
nbconvert==6.1.0
nbformat==5.1.3
nest-asyncio==1.5.1
numpy==1.21.2
openpyxl==3.0.7
packaging==21.0
pandas==1.3.2
pandocfilters==1.4.3
parso==0.8.2
pexpect==4.8.0
pickleshare==0.7.5
Pillow==8.3.1
prompt-toolkit==3.0.20
ptyprocess==0.7.0
Pygments==2.10.0
pyparsing==2.4.7
pyrsistent==0.18.0
python-dateutil==2.8.2
pytz==2021.1
pyzmq==22.2.1
requests==2.26.0
runipy==0.1.5
six==1.16.0
testpath==0.5.0
tornado==6.1
traitlets==5.0.5
urllib3==1.26.6
wcwidth==0.2.5
webencodings==0.5.1
```
## pip list install 

```
pip install -r requirements.txt
```

## 要点

### Excelファイルの取り扱い
エクセルファイルを開いた時に日付データがシリアル値になってしまう問題を対処しました.

```
for i in range(len(corona)):
    if type(corona['判明日'][i]) is int:
        corona['判明日'][i]=pandas.to_datetime('1900/1/1') + pandas.to_timedelta(corona['判明日'][i] - 1, unit='days')
```
## ファイルの自動収集

本コードを実行すると最新データがdownloadできる.

```
dt_now=dt.datetime.now()
file_day=dt_now - dt.timedelta(days=1)
file_day=file_day.strftime("%Y%m%d")
#ファイルのダウンロード
url='https://www.pref.tochigi.lg.jp/e04/welfare/hoken-eisei/kansen/hp/documents/'+str(file_day)+'hasseijoukyou.xlsx'
filename=str(file_day)+'hasseijoukyou.xlsx'
try:
  urlData = requests.get(url).content
except:
  file_day=dt_now - dt.timedelta(days=2)
  file_day=file_day.strftime("%Y%m%d")
  try:
    urlData = requests.get(url).content
  except:
    print('ファイルが存在しません')
  url='https://www.pref.tochigi.lg.jp/e04/welfare/hoken-eisei/kansen/hp/documents/'+str(file_day)+'hasseijoukyou.xlsx'
  filename=str(file_day)+'hasseijoukyou.xlsx'
with open('data/'+str(filename) ,mode='wb') as f: # wb でバイト型を書き込める
  f.write(urlData)
```

