# code pusher
code pushe 功能

## Install
pip install -r requirements.txt

## Run It
python3 main.py

## CMD
### 1. 新增大版本時要添加
app-add Goodnight-iOS-1_218_0
app-add Goodnight-Android-1_318_0

### 2. 查看當前版本發布情況
deployment Goodnight-iOS-1_218_0
deployment Goodnight-Android-1_318_0

### 3. 發到staging
release-staging Goodnight-iOS-1_218_0
release-staging Goodnight-Android-1_318_0

### 4. 發到正式版上
release-production Goodnight-iOS-1_218_0
release-production Goodnight-Android-1_318_0

### 5. 建立更新檔 update.json，會在 release 時同時建立好，要額外單獨建立也行。
build-staging Goodnight-iOS-1_218_0
build-production Goodnight-iOS-1_218_0

### 6. rollback
rollback Goodnight-iOS-1_218_0


## Note
### 1. 發大版本也需要 release-staging release-production
發大版本也要把 Bundle檔案上傳(如果之後v1 要rollback 才有東西)
