import json
import re
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from src import apiLoader

class IMOShortListTranslator:
    def __init__(self, item_list_path: str, preamble: str):
        """
        初始化翻译器
        :param item_list_path: results/item_list.json 路径
        :param preamble: 文档开头到 # Problems 之前的内容
        """
        with open(item_list_path, "r", encoding="utf-8") as f:
            self.items = json.load(f)  # List[{"label", "problem", "solutions"}]
        self.preamble = preamble

        # 用于公式占位
        self.math_blocks = []

        # 1. 初始化 LLM
        self.chat = ChatOpenAI(
            api_key=apiLoader.load_key(),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            model="qwen-plus",
            temperature=0.3,  # 数学翻译适合更低 temperature
        )

        # 2. 构建翻译提示模板
        self.translation_prompt = ChatPromptTemplate.from_template(
            """你是一位专业的数学文献翻译专家。请将以下英文数学文本准确翻译为中文，要求：
            - 仅翻译自然语言部分；
            - 所有形如 `__MATH_0__`、`__MATH_1__` 等占位符必须原样保留，不得改动、删除或翻译；
            - 题目不同解法的标题如 `解法 1`, `解法 2` 等用粗体表示
            - 保留原始段落结构和换行；
            - 使用正式、准确的数学术语。

            英文文本：
            ```text
            {text}
            中文翻译："""
        )

    def translate(self):
        """
        逐 item 翻译，返回 (full_zh_md: str, structured_items: list)
        """
        # 翻译 preamble
        preamble_clean = self.extract_math_placeholders(self.preamble)
        if preamble_clean.strip():
            messages = self.translation_prompt.format_messages(text=preamble_clean)
            resp = self.chat.invoke(messages)
            preamble_zh = self.restore_math_placeholders(resp.content.strip())
        else:
            preamble_zh = self.preamble

        problems_lines = ["# Problems"]
        solutions_lines = ["# Solutions"]
        structured_items = []

        round = 0   
        prev_category = None
        for item in self.items:

            # test 测试两道题
            round += 1
            if round == 3:
                break

            label = item["label"]
            category = self._get_category(label)

            # 翻译 problem
            prob_clean = self.extract_math_placeholders(item["problem"])
            if prob_clean.strip():
                messages = self.translation_prompt.format_messages(text=prob_clean)
                resp = self.chat.invoke(messages)
                prob_zh = self.restore_math_placeholders(resp.content.strip())
            else:
                prob_zh = item["problem"]

            # 翻译 solutions
            sols_zh = []
            for sol in item["solutions"]:
                sol_clean = self.extract_math_placeholders(sol)
                if sol_clean.strip():
                    messages = self.translation_prompt.format_messages(text=sol_clean)
                    resp = self.chat.invoke(messages)
                    sol_zh = self.restore_math_placeholders(resp.content.strip())
                else:
                    sol_zh = sol
                sols_zh.append(sol_zh)

            # === 只在 category 变化时添加 # Category ===
            if category != prev_category:
                problems_lines.append(f"# {category}")
                solutions_lines.append(f"# {category}")
                prev_category = category  # 更新

            # 添加题目
            problems_lines.extend([
                f"{label}.",
                prob_zh,
                ""
            ])
            
            solutions_lines.extend([
                f"# {category}",
                f"# {label}.",
                *sols_zh,
                ""
            ])

            # 构建结构化条目
            structured_items.append({
                "problem": prob_zh,
                "solutions": sols_zh,
                "final_answer": None
            })

        full_zh_md = "\n".join([
            preamble_zh.strip(),
            "",
            "\n".join(problems_lines),
            "",
            "\n".join(solutions_lines)
        ]).strip()

        return full_zh_md, structured_items


    def extract_math_placeholders(self, text: str) -> str:
        """
        目的: 将数学公式用占位符替换, 以防止误翻译以及JSON解析干扰.
        函数作用: 将 text 中的所有 $...$ 和 $$...$$ 替换为 __MATH_i__，
        并将原始公式按顺序存入 self.math_blocks。
        """
        self.math_blocks = []  # 每次调用前清空，避免污染

        def replace_match(match):
            formula = match.group(0)
            self.math_blocks.append(formula)
            return f"__MATH_{len(self.math_blocks) - 1}__"

        # 匹配 $$...$$ 或 $...$，且$$ 优先（避免被 $ 拆开）
        # 使用非贪婪模式 .*?
        pattern = r"\$\$.*?\$\$|\$.*?\$"
        result = re.sub(pattern, replace_match, text, flags=re.DOTALL)
        return result

    def restore_math_placeholders(self, text: str) -> str:
        """
        将 text 中的 __MATH_i__ 还原为对应的原始公式。
        """
        for i, formula in enumerate(self.math_blocks):
            placeholder = f"__MATH_{i}__"
            text = text.replace(placeholder, formula)
        return text
    
    @staticmethod
    def _get_category(label: str) -> str:
        mapping = {"A": "Algebra", "C": "Combinatorics", "G": "Geometry", "N": "Number Theory"}
        return mapping.get(label[0], "Unknown")