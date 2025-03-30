import mydb
import service
from envEnum import Environment

mydb.init()
# success = service.promote_project_version("Goodnight-iOS-1_218_0", "staging", "ooxxV2.com")
# if not success:
#     print("promote failed")

# success = service.rollback_project_version("Goodnight-iOS-1_218_0", "staging")
# if not success:
#     print("rollback failed")

# success = service.get_project_version("Goodnight-iOS-1_218_0", Environment.STAGING)
# if not success:
#     print("get version failed")
# print(success)

success = service.build_project_version("Goodnight-iOS-1_218_0", "staging")
if not success:
    print("build failed")