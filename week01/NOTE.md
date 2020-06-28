学习笔记

bs4筛选元素用法：

```
bs_info = bs(result.text, 'html.parser')
movie_list_source = bs_info.findAll('div', attrs={'class': 'movie-hover-info'})[:10]
```

XPath: [xpath 中文文档](https://www.w3school.com.cn/xpath/index.asp)

- `//`  从匹配选择的当前节点选择文档中的节点，而不考虑它们的位置。
- `/`   绝对路径
- `.`   从当前匹配层次继续匹配
- `..`  从上层匹配层次继续匹配
- `text()`  查找文字
- `@href`   查找href属性的值


scrapy.Request(xxxxx, dont_filter=True)     //允许跨域爬取