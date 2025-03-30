import repository
import os
import json
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
    project_version = repository.get_project_version_by_name(name, env.value)
    if len(project_version) == 0:
        return None

    project_version = project_version[0]

    response = {
        "version": project_version['version'],
        "url": project_version['url'],
        "created_at": project_version['created_at']
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
        "Version": f"{projectVersion['version']}",
        "Url": f"{projectVersion['url']}",
    }

    # 檢查並建立資料夾
    dir_path = os.path.join("output", name, env.value)
    os.makedirs(dir_path, exist_ok=True)

    # 儲存成 JSON 檔案
    with open(f"{dir_path}/update.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return True
