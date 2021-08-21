#!/bin/sh

#git pull
git pull

#ファイル名をここで決める
to_day=$(date +"%Y%m%d")
echo $to_day
#pipの更新
pip install -r requirements.txt
#python jupiter出力
jupyter nbconvert --execute COVID.ipynb --output $to_day  --to html