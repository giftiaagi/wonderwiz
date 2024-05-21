# wonderwiz

## 脚本

scripts/parse_sections.py 可以将《十万》的 XHTML 解析成 Section 列表，每个 Section 是一个章节。

将《十万》的 epub 解压缩，会得到一个 OEBPS 目录，把该目录放到 data/ 下。

```bash
mkdir data && cd data/
unzip ../十万个为什么数据集-天文.epub
cd ..
```

执行以下脚本，即可得到结构化的章节列表。

```bash
export PYTHONPATH=$(pwd)
python scripts/parse_sections.py
```

现在是将解析后的数据打印到控制台，可以将其保存到文件或DB，供后续使用。
