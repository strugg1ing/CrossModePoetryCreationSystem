## 下载Qwen模型
```
https://www.modelscope.cn/models/Embedding-GGUF/gte-Qwen2-7B-instruct-Q5_K_M-GGUF/resolve/master/gte-qwen2-7b-instruct-q5_k_m.gguf

## 下载完成后放入bot_model/
```
## 下载BLIP模型 
```
git clone https://github.com/salesforce/BLIP

# 之后将demo.py移动到BLIP-main文件夹

python demo.py #自动下载模型文件model_base_capfilt_large.pth（下载后可将model_url改为model_path，本地使用）

```
## 开启Qwen模型
```
进入bot_model文件夹，参考readme启动模型，占用端口8000；
```

## Apache Http Server部署前后端分离项目
```
安装apache2服务 # html文件夹包含项目的所有前端文件，Ubuntu系统将html文件夹放置在/var/www/
python main.py
```

## 项目文件目录参考如下（Python版本3.8）
```
BLIP-main
│   ├── bert-base-chinese
│   ├── bert-base-uncased
│   ├── BLIP.gif
│   ├── CODE_OF_CONDUCT.md
│   ├── CODEOWNERS
│   ├── cog.yaml
│   ├── configs
│   ├── data
│   ├── demo.py
│   ├── eval_nocaps.py
│   ├── eval_retrieval_video.py
│   ├── LICENSE.txt
│   ├── model_base_capfilt_large.pth
│   ├── models
│   ├── output_key.txt
│   ├──  output_temp.txt
│   ├── output_temp.txt
│   ├── Pic_text.py
│   ├── predict.py
│   ├── pretrain.py
│   ├── README.md
│   ├── requirements.txt
│   ├── SECURITY.md
│   ├── train_caption.py
│   ├── train_nlvr.py
│   ├── train_retrieval.py
│   ├── train_vqa.py
│   ├── transform
│   └── utils.py
├── bot_model
│   ├── qwen2-7b-instruct-q5_k_m.gguf
│   └── readme.md
├── html
│   ├── Comment.html
│   ├── Company.html
│   ├── Contact.html
│   ├── css
│   ├── fonts
│   ├── images
│   ├── index.html
│   ├── js
│   ├── presentimg
│   ├── pro
│   ├── product.html
│   ├── result.html
│   ├── test.html
│   └── uploads
├── main.py
├── output_key.txt
├── output_temp.txt
├── README.md
├── split_text.py
├── translate_chinese_to_english.py
├── uploads
└── whisper-main
    ├── approach.png
    ├── CHANGELOG.md
    ├── data
    ├── demo.py
    ├── language-breakdown.svg
    ├── LICENSE
    ├── MANIFEST.in
    ├── model-card.md
    ├── notebooks
    ├── pyproject.toml
    ├── README.md
    ├── requirements.txt
    ├── setup.py
    ├── tests
    └── whisper
```
