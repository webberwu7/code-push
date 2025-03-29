# app-add Goodnight-iOS-1_218_0
# deployment Goodnight-iOS-1_218_0
# release-staging Goodnight-iOS-1_218_0
# release-production Goodnight-iOS-1_218_0
# rollback Goodnight-iOS-1_218_0

def check_cmd():
    user_input = input("請輸入指令:")

    parts = user_input.split()
    version = parts[1] if len(parts) > 1 else ""
    
    if "app-add" in user_input:
        action = "新增"

    elif "deployment" in user_input:
        action = "檢查"

    elif "release-staging" in user_input:
        action = "發佈測試"

    elif "release-production" in user_input:
        action = "發佈正式"

    elif "rollback" in user_input:
        action = "回滾代碼"

    else:
        action = print("請檢查指令是否正確!!!")

    print(f"{action} {version}")

check_cmd()