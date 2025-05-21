import json

# 输入和输出文件路径
input_file = "/Users/chenandong/Documents/哈工大2024-2025/投稿/IBUT生成能力与翻译/code_submitted/data/commonsense.jsonl"  # 请替换成你的 JSONL 文件名
zh_output = "/Users/chenandong/Documents/哈工大2024-2025/投稿/IBUT生成能力与翻译/code_submitted/data/common.zh"
en_output = "/Users/chenandong/Documents/哈工大2024-2025/投稿/IBUT生成能力与翻译/code_submitted/data/common.en"

with open(input_file, 'r', encoding='utf-8') as fin, \
     open(zh_output, 'w', encoding='utf-8') as fzh, \
     open(en_output, 'w', encoding='utf-8') as fen:
    
    for line in fin:
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
            src = data.get("src", "").strip()
            tgt = data.get("tgt", "").strip()
            if src and tgt:
                fzh.write(src + "\n")
                fen.write(tgt + "\n")
        except json.JSONDecodeError as e:
            print(f"解析错误：{e}，跳过该行")