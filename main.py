import mydb
import service
from envEnum import Environment

mydb.init()

# 新增大版本
def app_add(name):
    success = service.create_project(name)
    if not success:
        print("app-add failed")

# 查看當前發佈狀態
def deployment(name):
    staging = service.get_project_version(name, Environment.STAGING)
    production = service.get_project_version(name, Environment.PRODUCTION)

    def format_data(name, data):    
        if data:
            return [name, data.get("version", ""), data.get("created_at", ""), data.get("url", "")]
        else:
            return [name, "No updates released", "", ""]
        
    # 表頭 + 資料
    headers = ["Name", "Version", "Release Time", "Download URL"]
    rows = [
        format_data("Production", production),
        format_data("Staging", staging)
    ]

    # 計算欄寬
    col_widths = [max(len(str(row[i])) for row in [headers] + rows) for i in range(len(headers))]

    def format_row(row):
        return "| " + " | ".join(str(row[i]).ljust(col_widths[i]) for i in range(len(row))) + " |"

    def separator():
        return "+-" + "-+-".join("-" * w for w in col_widths) + "-+"

    # 印出表格
    print(separator())
    print(format_row(headers))
    print(separator())
    for row in rows:
        print(format_row(row))
    print(separator())

def release_staging(name, download_url):
    success = service.promote_project_version(name, Environment.STAGING, download_url)
    if not success:
        print("release_staging failed")
    else:
        print("release_staging success")
        build_json(name, Environment.STAGING)

def release_production(name, download_url):
    success = service.promote_project_version(name, Environment.PRODUCTION, download_url)
    if not success:
        print("release_production failed")
    else:
        print("release_production success")
        build_json(name, Environment.PRODUCTION)

def rollback(name):
    success = service.rollback_project_version(name, Environment.PRODUCTION)
    if not success:
        print("rollback failed")
    else:
        print("rollback success")

def build_json(name, env: Environment):
    success = service.build_project_version(name, env)
    if not success:
        print("build failed")
    else:
        print("build success: 請前往檔案夾尋找 update.json")

def check_cmd():
    user_input = input("請輸入指令:")

    parts = user_input.split()
    name = parts[1] if len(parts) > 1 else ""
    
    if "app-add" in user_input:
        action = "新增"
        app_add(name)

    elif "deployment" in user_input:
        action = "檢查"
        deployment(name)

    elif "release-staging" in user_input:
        download_url = input("請輸入Download URL:")
        action = "發佈測試"
        release_staging(name, download_url)

    elif "release-production" in user_input:
        download_url = input("請輸入Download URL:")
        action = "發佈正式"
        release_production(name, download_url)

    elif "rollback" in user_input:
        action = "回滾代碼"
        rollback(name)

    elif "build-staging" in user_input:
        action = "建立 staging JSON"
        build_json(name, Environment.STAGING)
    
    elif "build-production" in user_input:
        action = "建立 production JSON"
        build_json(name, Environment.PRODUCTION)

    else:
        action = print("請檢查指令是否正確!!!")

check_cmd()
