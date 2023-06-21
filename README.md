### 跑起来

1. 下载项目到本地 `git git clone https://github.com/Amd794/kanleying    `
2. 进入到项目目录 `cd kanleying   `
3. 安装python运行环境 `pip install -r requirements.txt   `
4. 安装node依赖, cd 到js目录。由于部分网站对返回的数据进行了加密， 如果不下载这部分网站（腾讯动漫，沫沫漫画，coco漫画， 嗨皮漫画等），可以不用安装 `npm i  // 安装node依赖`
5. 配置settings.py
6. 运行项目 `python kanleying.py   `
7. 按照提示输入漫画地址即可，例如：

```shell
https://ac.qq.com/Comic/ComicInfo/id/652254
https://www.imoemh.com/manhua/bailianchengshen/
https://www.dashumanhua.com/comic/qinghuanxu/
```

​	8. 适配更多的漫画网站，可以在expand目录下创建