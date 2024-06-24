# jd-union-sdk

此 SDK 根据京东联盟 API 文档封装。详情见：[京东联盟API接口文档](https://union.jd.com/searchResultDetail?articleId=108188)



## 使用示例

```python
client = JDClient('your app key', 'your app secret')
result = client.request(
    method='jd.union.open.category.goods.get',
    params={'goodsReqDTO': {'keyword': '鞋', 'pageIndex': 1}}
)
print(result.json())
```
