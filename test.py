# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import requests
import datetime as dt
import pandas
import warnings
import japanize_matplotlib
warnings.simplefilter('ignore')


# %%

dt_now=dt.datetime.now()
file_day=dt_now - dt.timedelta(days=1)
file_day=file_day.strftime("%Y%m%d")
#ファイルのダウンロード
try:
  url='https://www.pref.tochigi.lg.jp/e04/welfare/hoken-eisei/kansen/hp/documents/'+str(file_day)+'hasseijoukyou.xlsx'
  urlData = requests.get(url).content
  filename=str(file_day)+'hasseijoukyou.xlsx'
  print('0')
  if urlData.decode().startswith('<?xml'):
    print('1')
    file_day=dt_now - dt.timedelta(days=2)
    file_day=file_day.strftime("%Y%m%d")
    url='https://www.pref.tochigi.lg.jp/e04/welfare/hoken-eisei/kansen/hp/documents/'+str(file_day)+'hasseijoukyou.xlsx'
    urlData = requests.get(url).content
    filename=str(file_day)+'hasseijoukyou.xlsx'
    if urlData.decode().startswith('<?xml'):
      print('2')
      file_day=dt_now - dt.timedelta(days=1)
      file_day=file_day.strftime("%Y%m%d")
      url='https://www.pref.tochigi.lg.jp/e04/welfare/hoken-eisei/kansen/hp/documents/'+str(file_day)+'hasseijkyou_1.xlsx'
      urlData = requests.get(url).content
      filename=str(file_day)+'hasseijkyou_1.xlsx'
    else:
      file_day=dt_now - dt.timedelta(days=2)
      file_day=file_day.strftime("%Y%m%d")
      url='https://www.pref.tochigi.lg.jp/e04/welfare/hoken-eisei/kansen/hp/documents/'+str(file_day)+'hasseijkyou_1.xlsx'
      urlData = requests.get(url).content
      filename=str(file_day)+'hasseijkyou_1.xlsx'
  else:
    print('終了')
except:
  file_day=dt_now - dt.timedelta(days=2)
  file_day=file_day.strftime("%Y%m%d")
  try:
    urlData = requests.get(url).content
  except:
    print('ファイルが存在しません')
  url='https://www.pref.tochigi.lg.jp/e04/welfare/hoken-eisei/kansen/hp/documents/'+str(file_day)+'hasseijkyou.xlsx'
  filename=str(file_day)+'hasseijkyou.xlsx'
with open('data/'+str(filename) ,mode='wb') as f: # wb でバイト型を書き込める
  f.write(urlData)
print(filename)


# %%
#本来はExcelデータを入力するようにする.
print(str(filename))
corona=pandas.read_excel('data/'+str(filename), header=1)
corona=corona[['番号','年代','性別','居住地','発症日','判明日','その他（＊）']]
corona=corona[corona['番号']!='※居住地にかかわらず、感染症の予防及び感染症の患者に対する医療に関する法律に基づき、栃木県及び宇都宮市に届け出のあった患者について掲載しています。（他県や検疫所に届け出があった患者は、他県等で公表されます。）\n※患者・御家族の人権尊重・個人情報保護に御理解と御配慮をお願いします。\n※退院日等の「退院」には、感染症法上の入院勧告等の解除及び県外保健所への入院等の対応依頼を含みます。\n(＊) 陽性者との接触の有無、感染に関与すると考えられる行動歴等  ']
corona=corona[corona['判明日']!='調査中']
corona=corona[corona['判明日']!='現在調査中']
corona=corona.reset_index()
for i in range(len(corona)):
    if type(corona['判明日'][i]) is int:
        corona['判明日'][i]=pandas.to_datetime('1900/1/1') + pandas.to_timedelta(corona['判明日'][i] - 1, unit='days')
#データの整形
corona=corona.dropna(how='all')
corona = corona.dropna(axis=0, subset=['番号'])
corona[corona['番号'].isnull()]
corona=corona[corona['番号']!=' ']
corona=corona.reset_index()
#当面の最終的な目標は, 2020年のデータと2021年のデータの区別ができるようにする.(暫定方法)
corona['Year']=0
corona['Month']=0
corona['判明日']=pandas.to_datetime(corona['判明日'], format='%Y-%m-%d %H:%M:%S')
corona['Year']=corona['判明日'].dt.year
corona['Month']=corona['判明日'].dt.month

# %% [markdown]
# <h1>全体データ</h1>

# %%
corona

# %% [markdown]
# <h2>最新データ</h2>

# %%
corona_s=corona[corona['判明日']==corona['判明日'][0]]
print(str(corona['判明日'][0])+'のデータの件数')
print(str(len(corona_s))+'件')


# %%
corona_s

# %% [markdown]
# <h2>居住地についての可視化</h2>
# <pre>
# 多い順に10件に絞って可視化する.
# </pre>

# %%
corona_place=corona_s.groupby('居住地').count().sort_values('番号',ascending=False)['番号'][0:10]
corona_place.plot.pie(subplots=True)


# %%
corona_place

# %% [markdown]
# <h2>年齢についての可視化</h2>

# %%
corona_nen=corona_s.groupby('年代').count().sort_values('番号',ascending=False)['番号'][0:10]
corona_nen.plot.pie(subplots=True)


# %%
corona_nen

# %% [markdown]
# <h2>性別についての可視化</h2>

# %%
corona_sei=corona_s.groupby('性別').count().sort_values('番号',ascending=False)['番号'][0:10]
corona_sei.plot.pie(subplots=True)

# %% [markdown]
# <h2>月別コロナ数推移</h2>
# <pre>
# 現状, 発症日をベースにすると調査中のデータが多い為判明日をベースにカウントする.
# ※発症数をcountで取る.
# </pre>

# %%
#2021年のデータを対象とする.
corona=corona[corona['Year']==2021]
corona.groupby(pandas.Grouper(key='判明日', freq='M')).count()['Year'].plot()


# %%
corona.groupby(pandas.Grouper(key='判明日', freq='M')).count()['番号']

# %% [markdown]
# <h2>居住地についての可視化</h2>
# <pre>
# 多い順に10件に絞って可視化する.
# </pre>

# %%
corona_place=corona.groupby('居住地').count().sort_values('番号',ascending=False)['番号'][0:10]
corona_place.plot.pie(subplots=True)


# %%
corona_place

# %% [markdown]
# <h2>年齢についての可視化</h2>

# %%
corona_nen=corona.groupby('年代').count().sort_values('番号',ascending=False)['番号'][0:10]
corona_nen.plot.pie(subplots=True)


# %%
corona_nen

# %% [markdown]
# <h2>性別についての可視化</h2>

# %%
corona_sei=corona.groupby('性別').count().sort_values('番号',ascending=False)['番号'][0:10]
corona_sei.plot.pie(subplots=True)


# %%
corona_sei

# %% [markdown]
# <h2>日別コロナ数推移</h2>
# <pre>
# 現状, 発症日をベースにすると調査中のデータが多い為判明日をベースにカウントする.
# ※発症数をcountで取る.
# </pre>

# %%
corona.groupby(pandas.Grouper(key='判明日', freq='D')).count()['番号'].plot()


# %%
corona.groupby(pandas.Grouper(key='判明日', freq='D')).count()['番号']

# %% [markdown]
# <h1>今月のデータ</h1>

# %%
dt_now = dt.datetime.now()
dt_now.month
corona_toYear=corona[corona['Year']==2021]
corona_toYear=corona_toYear[corona_toYear['Month']==8]

# %% [markdown]
# <h2>日別データ(今月)</h2>

# %%
corona_toYear.groupby(pandas.Grouper(key='判明日', freq='D')).count()['発症日'].plot()

# %% [markdown]
# <h2>居住地についての可視化(今月)</h2>
# <pre>
# 多い順に10件に絞って可視化する.
# </pre>

# %%
corona_place=corona_toYear.groupby('居住地').count().sort_values('番号',ascending=False)['番号'][0:10]
corona_place.plot.pie(subplots=True)


# %%
corona_place

# %% [markdown]
# <h2>年齢についての可視化(今月)</h2>

# %%
corona_nen=corona_toYear.groupby('年代').count().sort_values('番号',ascending=False)['番号'][0:10]
corona_nen.plot.pie(subplots=True)


# %%
corona_nen

# %% [markdown]
# <h2>性別についての可視化(今月)</h2>

# %%
corona_sei=corona_toYear.groupby('性別').count().sort_values('番号',ascending=False)['番号'][0:10]
corona_sei.plot.pie(subplots=True)


