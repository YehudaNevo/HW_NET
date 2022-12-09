import re

regular_exp_valid_get = "^GET.*HTTP\/1\.1\r$"

req = "GET / HTTP/1.1\r"

res = re.search(regular_exp_valid_get, req)
print(res)
