## amis-python
<p align="center">
    <a href="https://cdn.jsdelivr.net/gh/CMHopeSunshine/amis-python@master/LICENSE"><img src="https://img.shields.io/github/license/CMHopeSunshine/amis-python" alt="license"></a>
    <img src="https://img.shields.io/badge/Python-3.7+-yellow" alt="python">
    <img src="https://img.shields.io/pypi/v/amis-python" alt="version">
</p>

基于 [百度amis](https://github.com/baidu/amis) 前端框架的python pydantic模型封装。

由于[原版本](https://github.com/amisadmin/fastapi_amis_admin/tree/master/fastapi_amis_admin/amis)缺少大量amis新版本的组件或配置，因此本项目在其版本的基础上进行了扩充。

相比fastapi-amis-admin的版本：
- 涵盖amis截至3.1.0版本的所有组件
- 使用jinja2模板
- 支持修改主题
## 安装
```
pip install amis-python
```
## 简单使用
```python
from amis.components import Page

page = Page(title='新页面', body='Hello World')
# 输出为python字典
print(page.to_dict())
# 输出为json
print(page.to_json())
# 输出为str
print(page.render())
# 保存为html文件
with open('HelloWorld.html', 'w', encoding='utf-8') as f:
    f.write(page.render())
```

## 详细使用
详见[amis官方文档](https://aisuda.bce.baidu.com/amis/zh-CN/docs/index)

## 感谢
- [amis](https://github.com/baidu/amis)
- [fastapi-amis-admin](https://github.com/amisadmin/fastapi_amis_admin/tree/master/fastapi_amis_admin/amis)
