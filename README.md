# corona-bunseki
## 栃木県のコロナ発生状況を分析
栃木県のコロナ発生状況を分析するプログラムです.

## データセット
https://www.pref.tochigi.lg.jp/e04/welfare/hoken-eisei/kansen/hp/coronakensahasseijyoukyou.html

## データセットのファイル場所

```
data/
```

## 注意点

このノートブック(アウトプット資料)は上記データセットに基づいて<br>
コードの内容で可視化を行っています.<br>
あくまでも参考程度にしていただけると幸いです.


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

## 実行コマンド

```
jupyter nbconvert --execute COVID.ipynb --to html
```
