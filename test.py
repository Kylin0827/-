#正则表达式
import re
#1- .  通配符--除换行符之外的符号----一个元素
# str1 = 'songqins\n'
# #re.findall(‘正则表达式’，需要处理的字符串)
# res = re.findall('s.',str1)#查找所有符合要求的内容：有时候不止一个---返回值---list
# print(res)

#2- *    前面元素出现过0次或者n次
# str1 = 'songqins'
# res = re.findall('so*',str1)#
# print(res)
#
# #3- +    前面元素出现过1次或者n次
# str1 = 'songqinso'
# res = re.findall('so.+',str1)#
# print(res)

#4- ?  组合用法--------------- a1111b  -----  a(.*?)b

#5- \w----匹配字母数字及下划线---一个元素
# str1 = 'songqin*ab'
# res = re.findall('\w{3}',str1)#
# print(res)

#6- \W    匹配非字母数字及下划线

# str1 = 'songqin*ab'
# res = re.findall('\W',str1)#
# print(res)

#---\S 匹配任意非空字符
# str1 = 'abc'
# res = re.findall('\S',str1)#
# print(res)

#7- \d 匹配任意数字，等价于 [0-9]

# str1 = 'abc29171934523563263465634564574572743deg'
# res = re.findall('\d.+\d',str1)#
# print(res)


#修饰符
#re.I----大小写不敏感
str1 = 'songqinS\n'
res = re.findall('s.',str1,re.I|re.S)#
print(res)
#设置读取网页的头部，该行代码主要用于模拟浏览器来访问网站
# _header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
#https://search.51job.com/
#51job

#目标：获取符合要求的岗位
'''
excel存储初始化：
   1- 新建一个excel文件
   2- 创建一个子表

'''
import xlwt
import requests,re
#1- 新建一个excel文件
workBook = xlwt.Workbook(encoding='uft-8')#缓存里
#2- 创建一个子表
workSheet = workBook.add_sheet('51job')
colName = ['岗位名称','公司名称','地址','薪资','发布时间']
#3- 写进去
for one in range(0,len(colName)):# 0 1 2 3 4
   #写单元格
   workSheet.write(0,one,colName[one])#(行编号，列编号，内容)


#---获取页数：
# <span class="td">共28页，到第</span>
def get_pageNum():
   web_url = 'https://search.51job.com/list/020000,000000,0000,00,9,99,%25E8%2587%25AA%25E5%258A%25A8%25E5%258C%2596%25E6%25B5%258B%25E8%25AF%2595,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
   resp = requests.get(web_url)
   resp.encoding = 'gbk'
   pages = int(re.findall('<span class="td">共(.*?)页，到第</span>',resp.text,re.S)[0])
   return pages

row = 1#初始化=1
#----------------------1、构建请求----------------------
for one in range(1,get_pageNum()+1):
   web_url = f'https://search.51job.com/list/020000,000000,0000,00,9,99,%25E8%2587%25AA%25E5%258A%25A8%25E5%258C%2596%25E6%25B5%258B%25E8%25AF%2595,2,{one}.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
   resp = requests.get(web_url)
   resp.encoding = 'gbk'
   #1- 想查看发出去的请求头 或者 请求体：fiddler抓包，
   # print(resp.request.headers)#请求头
   # print(resp.request.body)#请求体
   #----------------------2、解析响应数据------------------
   # print(resp.text)
   #----------------------3、提取有效数据------------------
   info = re.findall('<div class="el">(.*?)</div>',resp.text,re.S)#list
   for line in info:
      #1- 获取岗位名称
      temp = re.findall('<a target="_blank" title="(.*?)" href',line,re.S)
      jobName = temp[0].strip()
      workSheet.write(row, 0, jobName)
      #2- 获取公司名称
      company = temp[1].strip()
      workSheet.write(row, 1, company)
      #3- 获取地址
      address = re.findall('<span class="t3">(.*?)</span>',line,re.S)[0]
      workSheet.write(row, 2, address)
      #4- 获取薪资
      salary= re.findall('<span class="t4">(.*?)</span>', line, re.S)[0]
      workSheet.write(row, 3, salary)
      #5- 发布时间
      jobTime= re.findall('<span class="t5">(.*?)</span>', line, re.S)[0]
      workSheet.write(row, 4, jobTime)
      row += 1
#----------------------4、存储数据----------------------
#4- 保存
workBook.save('g:\\res_51job.xls')
