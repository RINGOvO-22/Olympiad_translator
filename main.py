# main.py
from src.extractor import IMOShortlistExtractor
from src.translator import IMOShortListTranslator
import json
import os

def main():
    extractor = IMOShortlistExtractor("resources/full.md")
    preamble, items = extractor.extract()
    # print(f"\n Test: preable:\n{preamble}")

    # 转为目标 JSON 格式（暂不翻译，final_answer 设为 null）
    json_output = []
    for item in items:
        json_output.append({
            "label": item["label"],
            "problem": item["problem"],
            "solutions": item["solutions"],
            # "final_answer": None  # 可后续从 solutions 中提取
        })

    # 保存到 results/ 
    os.makedirs("results", exist_ok=True)
    with open("results/item_list.json", "w", encoding="utf-8") as f:
        json.dump(json_output, f, ensure_ascii=False, indent=2)

    print(f"✅ 成功解析 {len(json_output)} 道题目，结果已保存至 results/item_list.json")

    translator = IMOShortListTranslator("results/item_list.json", preamble=preamble)
    full_zh_md, structured_items = translator.translate()
    print(translator.get_token_report())

    # 确保 results 目录存在
    os.makedirs("results", exist_ok=True)

    # 保存 full_zh.md 和 full_zh.json 文件
    with open("results/full_zh.md", "w", encoding="utf-8") as f:
        f.write(full_zh_md)
    with open("results/full_zh.json", "w", encoding="utf-8") as f:
        json.dump(structured_items, f, ensure_ascii=False, indent=2)

    print("✅ 已保存 results/full_zh.md 和 results/full_zh.json")


if __name__ == "__main__":
    main()