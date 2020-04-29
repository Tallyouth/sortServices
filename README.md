# sortSservices
排行榜服务

## 安装
### 建立虚拟环境
```
conda create -n py36 python=3.6 
source/conda activate py36
```
### django
```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```
## 启动
```
python manage.py runserver 8000
```
