# comic_spider
### 跑起来
1. 下载项目到本地
`git
git clone https://github.com/Amd794/kanleying   
`
   
2. 进入到项目目录
`
cd kanleying   
`
   
3. 安装python运行环境
`
pip install -r requirements.txt   
`
   
4. 安装node依赖, cd 到js目录。由于部分网站对返回的数据进行了加密，
   如果不下载这部分网站（腾讯动漫，沫沫漫画，coco漫画， 嗨皮漫画等），可以不用安装
`
node init   
`
   
5. 配置settings.py
   
6. 运行项目
`
python kanleying.py   
`
   
7. 按照提示输入漫画地址即可，例如：

- https://ac.qq.com/Comic/comicInfo/id/649185
- https://m.happymh.com/manga/douluodalu
- http://www.pufei8.com/manhua/7/
- https://www.kanman.com/107682/

```python
chars = {
     # 直接回车 下载最新章节，0 下载全部章节
    '+': 'detail_dicts[int(index[0]):]', # 2+， 下载第二章往后的所有
    '/': 'detail_dicts[int(index[0]): int(index[1])]', # 2/6， 下载第二章到第6章节
    '-': 'detail_dicts[int(index[0])-2::-1],', # 6- ， 下载第六章往下所有
    '*': str([detail_dicts[i - 1] for i in list(map(int, index))]), # 3*6*10 下载第三，第六，第九章节
}
```
### 运行结果预览
![avatar](https://image.amd794.com/17e1a5ff8b667bb1e1fb4d436670e6c1.png@blog)
![avatar](https://image.amd794.com/a75fd7ecea6f425b610e66321098d095.png@blog)
### 说明
文件中有4个辅助文件
- try_to_fix.py 可以修复pdf、压缩包、图片
- cut_watermark.py 去除图片水印
- Re_splicing_img.py 重构图片（某些网站会出现切割）
- Re_splicing_img_hz.py 重构图片（某些网站会出现切割）
- Refactoring_html.py 应用最新的模板

### 在线阅读
 https://amd794.com