from binnacle.plugins.http import *

base_url("http://localhost:5001")

# Without API Key
get("/api/v1/folders", status=403)

# With wrong API Key
set_header("x-api-key", "ABC")
get("/api/v1/folders", status=401)

# With valid API Key
set_header("x-api-key", "user_26a5fa8c7d8ad3729d218bcecf38c3aa9a7d4e40106072b4fd3f313af5c0682f")
data = get("/api/v1/folders")
debug(data)
folders = validated_json(data)

compare_equal(len(folders), 4)
compare_not_equal(100, 100)

validated_json('{"name": 100}')

command_run("ls /tmp")

show_summary()
