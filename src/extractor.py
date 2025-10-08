# src/extractor.py
import re
from typing import List, Dict, Optional

class IMOShortlistExtractor:
    def __init__(self, md_path: str):
        with open(md_path, "r", encoding="utf-8") as f:
            self.text = f.read()

        # 题目标题的鲁棒正则（匹配行首，容忍空格和 LaTeX 包裹）
        self.title_pattern = re.compile(
            r"""
            ^\s*                                    # 行首空白
            (?:
                ([ACGN])\s*(\d+)\s*\.\s*            # 普通格式: A4. 或 A 4 .
                |
                \$\\left\(\s*\\mathbf\s*\{\s*([ACGN])\s*(\d+)\s*\.\s*\}\s*\\right\)\$\s+  # \mathbf{A4.}
                |
                \$\\left\(\s*\\mathbf\s*\{\s*([ACGN])\s*\}\s*(\d+)\s*\.\s*\\right\)\$\s+  # \mathbf{A}4.
                |
                \#\s*([ACGN])\s*(\d+)\s*\.\s*       # # 开头: # A4.
            )
            """,
            re.MULTILINE | re.VERBOSE
        )

    def _split_sections(self) -> tuple[str, str]:
        """切分 Problems 和 Solutions 区块"""
        problems_match = re.search(r"^# Problems\s*$(.*?)^# Solutions\s*$", self.text, re.DOTALL | re.MULTILINE)
        solutions_match = re.search(r"^# Solutions\s*$(.*)", self.text, re.DOTALL | re.MULTILINE)

        if not problems_match or not solutions_match:
            raise ValueError("未能找到 # Problems 或 # Solutions 区块")

        return problems_match.group(1).strip(), solutions_match.group(1).strip()

    def _parse_section(self, section_text: str) -> List[Dict[str, str]]:
        """解析一个区块（Problems 或 Solutions），返回题目列表"""
        lines = section_text.splitlines()
        items = []
        current_label = None
        current_content_lines = []

        i = 0
        while i < len(lines):
            line = lines[i]
            match = self.title_pattern.search(line)

            if match:
                # 保存上一题
                if current_label is not None:
                    items.append({
                        "label": current_label,
                        "content": "\n".join(current_content_lines).strip()
                    })

                # 提取 label：四个分支 → (1,2), (3,4), (5,6), (7,8)
                letter = match.group(1) or match.group(3) or match.group(5) or match.group(7)
                number = match.group(2) or match.group(4) or match.group(6) or match.group(8)
                if letter is None or number is None:
                    raise ValueError(f"无法解析题目标题: {line.strip()}")
                current_label = letter + number

                # 提取标题之后的内容
                after_title = line[match.end():].strip()
                current_content_lines = [after_title] if after_title else []
                i += 1
            else:
                # 普通内容行（包括空行、公式、图片等）
                current_content_lines.append(line)
                i += 1

        # 保存最后一题
        if current_label is not None:
            items.append({
                "label": current_label,
                "content": "\n".join(current_content_lines).strip()
            })

        return items

    def extract(self) -> List[Dict[str, str]]:
        """主入口：返回按顺序对齐的题目列表（每题含 problem + solutions）"""
        problems_text, solutions_text = self._split_sections()

        problem_items = self._parse_section(problems_text)
        solution_items = self._parse_section(solutions_text)

        # 构建 label -> solutions 映射
        sol_map = {}
        for item in solution_items:
            label = item["label"]
            if label not in sol_map:
                sol_map[label] = []
            sol_map[label].append(item["content"])

        # 按 Problems 顺序输出（确保 31 题顺序正确）
        result = []
        for prob in problem_items:
            label = prob["label"]
            solutions = sol_map.get(label, [])
            result.append({
                "label": label,
                "problem": prob["content"],
                "solutions": solutions
            })

        return result