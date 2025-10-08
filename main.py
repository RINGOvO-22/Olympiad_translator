# main.py
from src.extractor import IMOShortlistExtractor
import json
import os

def main():
    extractor = IMOShortlistExtractor("resources/full.md")
    items = extractor.extract()

    # 转为目标 JSON 格式（暂不翻译，final_answer 设为 null）
    json_output = []
    for item in items:
        json_output.append({
            "label": item["label"],
            "problem": item["problem"],
            "solutions": item["solutions"],
            "final_answer": None  # 可后续从 solutions 中提取
        })

    # 保存到 results/
    os.makedirs("results", exist_ok=True)
    with open("results/full_zh.json", "w", encoding="utf-8") as f:
        json.dump(json_output, f, ensure_ascii=False, indent=2)

    print(f"✅ 成功解析 {len(json_output)} 道题目，结果已保存至 results/full_zh.json")

if __name__ == "__main__":
    main()