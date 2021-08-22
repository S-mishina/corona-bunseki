#!/bin/sh

#git pull
git pull

#ファイル名をここで決める
to_day=$(date +"%Y%m%d")
echo $to_day
#pipの更新
pip3 install -r ../../home/ssm-user/corona-bunseki/requirements.txt
#python jupiter出力
jupyter nbconvert --execute ../../home/ssm-user/corona-bunseki/test.ipynb --output output/$to_day  --to html
#aws s3アップロード
aws s3 cp ../../home/ssm-user/corona-bunseki/output s3://corona-out-put-log/ --recursive