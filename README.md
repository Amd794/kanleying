### 跑起来
0. 安装python和nodejs
- https://github.com/coreybutler/nvm-windows/releases 下载安装nvm。打开CMD，输入命令 `nvm` 输出版本信息表示安装成功，接着`nvm install 14.16.1`。
- https://www.python.org/downloads/ 下载安装python
1. 下载项目到本地 `git clone https://github.com/Amd794/kanleying    `
2. 进入到项目目录 `cd kanleying   `
3. 打开cmd安装python运行环境 `pip install -r requirements.txt   `
4. 安装node依赖, cd 到js目录。由于部分网站对返回的数据进行了加密， 如果不下载这部分网站（腾讯动漫，沫沫漫画，coco漫画， 嗨皮漫画等），可以不用安装 
```shell
cd js
npm i  // 安装node依赖
```
5. 配置settings.py
6. 运行bin目录下的 `run.py   `
7. 按照提示输入漫画地址即可，例如：
```shell
https://ac.qq.com/Comic/ComicInfo/id/652254
https://www.imoemh.com/manhua/bailianchengshen/
https://www.dashumanhua.com/comic/qinghuanxu/
```

8. 适配更多的漫画网站，可以在expand目录下创建