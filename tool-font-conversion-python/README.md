# 使用 Python 进行字体格式转换

## 环境准备
- 1. 确保安装了 Python 3.7+ 执行：`python --version`
- 2. 安装 fonttools 执行：`pip install fonttools`
- 3. 开发代码：`convert.py`
- 补充：
    - 如果需要转换woff2格式转换失败，需要额外安装 brotli 库，执行：`pip install brotli`
    - 验证是否安装成功，执行：`python -c "import brotli; print('Brotli 库已成功安装，版本:', brotli.__version__)"`

## 字体格式转换命令
- 执行脚本进行字体转换：`python convert.py myfont.otf` 或 `python convert.py myfont.otf myfont_converted.ttf`

## 使用pyftsubset命令进行子集化
- 执行脚本打包指定字符集【指定文字】：`pyftsubset myfont_converted.ttf --text="测试" --output-file=output_small.ttf`
- 执行脚本打包指定字符集【直接从 txt 文件读取文字】：`pyftsubset myfont_converted.ttf --text-file=3500常用字.txt --output-file=output_common_3500.ttf`

## 使用记录
- 执行：`python convert.py SourceHanSansSC-Medium.otf`
- 执行：`pyftsubset SourceHanSansSC-Medium.ttf --text="测试" --output-file=output_small.ttf`
- 执行：`pyftsubset SourceHanSansSC-Medium.ttf --text-file=3500常用字.txt --output-file=output_common_3500.ttf`
- 执行：`python convert.py FZYANS_ZHONGJW--GB1-0.woff`
- 执行：`pyftsubset FZYANS_ZHONGJW--GB1-0.ttf --text="测试" --output-file=output_small.ttf`
- 执行：`pyftsubset FZYANS_ZHONGJW--GB1-0.ttf --text-file=3500常用字.txt --output-file=output_common_3500.ttf`

- 执行：`python convert.py aaa.otf`
- 执行：`pyftsubset aaa.ttf --text="测试" --output-file=output_small.ttf`
- 执行：`pyftsubset aaa.ttf --text-file=3500常用字.txt --output-file=output_common_3500.ttf`

- 执行：`python convert.py SourceHanSansSC-VF.woff2`
- 执行：`pyftsubset SourceHanSansSC-VF.ttf --text="测试" --output-file=output_small.ttf`
- 执行：`pyftsubset SourceHanSansSC-VF.ttf --text-file=3500常用字.txt --output-file=output_common_3500.ttf`
- 执行：`pyftsubset 1.otf --text="测试" --output-file=output_small.otf`