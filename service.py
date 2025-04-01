import repository
import os
import json
import re
from envEnum import Environment


# 新增一個專案
# 一次會幫建立兩個環境 staging and production
def create_project(name) -> bool:
    # 一次新增兩個project 進去
    # environment staging and production
    repository.insert_project(name, Environment.STAGING.value)
    repository.insert_project(name, Environment.PRODUCTION.value)

    return True


def get_project_version(name, env: Environment) -> dict:
    project = repository.get_project_by_name(name, env.value)
    if len(project) == 0:
        return False
    project = project[0]

    projectVersion = repository.get_project_versioin(
        project['current_version_id'])
    if len(projectVersion) == 0:
        return False
    projectVersion = projectVersion[0]

    response = {
        "version": projectVersion['version'],
        "url": projectVersion['url'],
        "created_at": projectVersion['created_at']
    }

    return response


def promote_project_version(name, env: Environment, url) -> bool:
    # 先搜尋是否有此專案
    project = repository.get_project_by_name(name, env.value)
    if len(project) == 0:
        print("project not found")
        return False

    # 有此專案
    project = project[0]
    # 準備下一個版號
    next_version = 0
    if project['current_version_id'] != -1:
        cpv = repository.get_project_versioin(project['current_version_id'])
        # 有下一個版本
        if len(cpv) != 0:
            # 新增下一個版本
            next_version = cpv[0]['version'] + 1

    # 特例當env為production的時候 url 要從staging拿
    if env == Environment.PRODUCTION:
        # 取得staging最新版本
        stageProject = repository.get_project_by_name(name, Environment.STAGING.value)
        if len(stageProject) == 0:
            print("stage project not found")
            return False
        stageProject = stageProject[0]
        spv = repository.get_project_versioin(stageProject['current_version_id'])
        if len(spv) == 0:
            print("staging project version not found")
            return False
        spv = spv[0]
        url = spv['url']

    npvId = repository.insert_project_version(
        project['id'], next_version, url, project['current_version_id'], None)

    # 更新原本版本
    repository.update_project_version_next(
        project['current_version_id'], npvId)

    # 更新專案
    repository.update_project_current_version(project['id'], npvId)

    return True


def rollback_project_version(name, env: Environment) -> bool:
    # 先搜尋是否有此專案
    project = repository.get_project_by_name(name, env.value)
    if len(project) == 0:
        return False

    # 有此專案
    project = project[0]
    if project['current_version_id'] == -1:
        return False

    # 有當前版本
    cpv = repository.get_project_versioin(project['current_version_id'])
    if len(cpv) == 0:
        return False
    cpv = cpv[0]

    # 有上一個版本
    lpv = repository.get_project_versioin(cpv['last_id'])
    if len(lpv) == 0:
        return False
    lpv = lpv[0]

    # 準備下一個版號
    next_version = cpv['version'] + 1
    npvId = repository.insert_project_version(
        project['id'], next_version, lpv['url'], project['current_version_id'], None)

    # 更新原本版本
    repository.update_project_version_next(
        project['current_version_id'], npvId)

    # 更新專案
    repository.update_project_current_version(project['id'], npvId)

    return True


def build_project_version(name, env: Environment) -> bool:
    project = repository.get_project_by_name(name, env.value)
    if len(project) == 0:
        return False
    project = project[0]

    projectVersion = repository.get_project_versioin(
        project['current_version_id'])
    if len(projectVersion) == 0:
        return False
    projectVersion = projectVersion[0]

    data = {
        "version": f"{projectVersion['version']}",
        "bundleUrl": f"{projectVersion['url']}",
    }

    # 取得專案名稱
    match = re.search(r'([A-Za-z]+)-(\d+(?:_\d+)*)', name.strip())
    if match:
        platform = match.group(1)               # 取得 iOS
        raw_version = match.group(2)            # 取得 1_218_0
        platform_version = raw_version.replace('_', '.') # 轉成 1.218.0

    # 檢查並建立資料夾
    dir_path = os.path.join("output", platform)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, "update.json")

    # 檢查檔案是否存在
    if os.path.exists(file_path):
        # 如果存在,則讀取 JSON 檔案
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                update_data = json.load(f)
            except json.JSONDecodeError:
                update_data = {}
    else:
        update_data = {}

    # 初始化巢狀 dict
    if env.value not in update_data:
        update_data[env.value] = {}

    # 建立 / 更新 該版本的內容
    update_data[env.value][platform_version] = {
        "version": projectVersion['version'],
        "bundleUrl": f"{projectVersion['url']}",
    }

    # 儲存成 JSON 檔案
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(update_data, f, ensure_ascii=False, indent=4)

    return True
