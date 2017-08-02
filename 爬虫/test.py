str = "//abc/aaaaaaaaaaaaa/bbbbbbbbbbb/cccccccccc"
str_list = str.split('/')
print(str_list)
print(len(str_list))
for i in range(len(str_list)):
    str_real = str_real + '/' + str_list[i]
    print(str_real)
