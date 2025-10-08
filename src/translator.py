import json
import re
import base64
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from src import apiLoader

IMG_PATTERN = re.compile(r"!\$$images/([a-f0-9]{64}\.jpg)\$$")

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

        # 2. 定义结构化解析器
        response_schemas = [
            ResponseSchema(name="problem_zh", description="题干的中文翻译，保留 __MATH_i__ 占位符"),
            ResponseSchema(name="solution_zh", description="题解的中文翻译列表，每个元素是一段解法，保留 __MATH_i__ 占位符"),
            ResponseSchema(name="final_answer", description="最终答案的中文表述，若无则为 null"),
            ResponseSchema(name="others", description="题解中的独立补充部分, 如评论, 常用表达等一切非题解本身但又独立的段落")
        ]

        # 3. 创建一个 output parser
        self.output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

        # 4. 获取一个 `format_instructions`
        self.format_instructions = self.output_parser.get_format_instructions()

        # 5. 构建用于结构化输出的翻译提示模板
        self.structured_prompt = ChatPromptTemplate.from_template(
            """你是一位专业的数学竞赛翻译与解析专家。请根据以下英文题目和解答，严格按 JSON 格式输出结构化结果。

            要求：
            - 仅翻译自然语言，所有 `__MATH_i__` 占位符必须原样保留；
            - `solution_zh` 是一个字符串列表，每个元素对应一个完整解法, 要注意第一个解法的开头要去除题干部分, 且不要包含独立出来的评论, 常用表达等模块;
            - 同时, 题目不同解法的标题如 `解法 1`, `解法 2` 等用粗体表示; 且题解中不要再出现标题如`# (3)`.
            - `others` 是一个字符串, 包含英文题解中的评论, 题解开头'常用表达'等非 solution 本身的单独段落. 这些段落的小标题如`评论`, `常用表达` 等用中文, 粗体表示
            - `final_answer` 提取最终结论（如数值、表达式、存在性等），若无明确答案则为 null；
            - 不要添加任何额外说明或 Markdown。
            - 其他情况下, 每个字符串内部保留原始段落结构和换行；
            - 使用正式、准确的数学术语。

            题目标签：{label}
            英文题干：{problem_clean}
            英文题解：{solutions_clean}

            {format_instructions}
            """
        )

        # 初始化 Token 统计
        self.token_usage = {
            "preamble": 0,
            "problems": 0,
            "solutions": 0,
            "total_input": 0,
            "total_output": 0,
            "call_count": 0
        }

    def _record_token_usage(self, resp, category: str):
        """从 LLM 响应中提取 token usage 并累加"""
        usage = resp.response_metadata.get("token_usage", {})
        input_tokens = usage.get("input_tokens", 0)
        output_tokens = usage.get("output_tokens", 0)
        
        self.token_usage["total_input"] += input_tokens
        self.token_usage["total_output"] += output_tokens
        self.token_usage["call_count"] += 1
        if category in ["preamble", "problems", "solutions"]:
            self.token_usage[category] += input_tokens

    def translate(self):
        """
        返回 (full_text: str, structured_items: list)
        - full_text: preamble + 所有题目的 solution_zh（按原 Problems/Solutions 结构）
        - structured_items: 每题的结构化数据
        """
        # 翻译 preamble
        preamble_clean = self.extract_math_placeholders(self.preamble)
        if preamble_clean.strip():
            # 使用普通翻译 prompt（非结构化）
            simple_prompt = ChatPromptTemplate.from_template(
                """你是一位专业的数学文献翻译专家。请将以下英文数学文本准确翻译为中文，要求：
                - 仅翻译自然语言部分；
                - 所有形如 `__MATH_0__`、`__MATH_1__` 等占位符必须原样保留；
                - 保留原始段落结构和换行；
                - 使用正式、准确的数学术语。

                英文文本：
                ```text
                {text}
                中文翻译："""
            )
            messages = simple_prompt.format_messages(text=preamble_clean)
            resp = self.chat.invoke(messages)
            self._record_token_usage(resp, "preamble")  # 记录 token 消耗
            preamble_zh = self.restore_math_placeholders(resp.content.strip())
        else:
            preamble_zh = self.preamble

        problems_lines = ["# Problems"]
        solutions_lines = ["# Solutions"]
        structured_items = []

        prev_category = None
        round = 0
        for item in self.items:
            round += 1
            if round == 2:  # 测试用
                break

            label = item["label"]
            category = self._get_category(label)

            # 提取占位符
            prob_clean = self.extract_math_placeholders(item["problem"])
            sols_clean = [self.extract_math_placeholders(sol) for sol in item["solutions"]]

            # 调用结构化 LLM
            try:
                messages = self.structured_prompt.format_messages(
                    label=label,
                    problem_clean=prob_clean,
                    solutions_clean="\n\n---\n\n".join(sols_clean),
                    format_instructions=self.format_instructions
                )
                resp = self.chat.invoke(messages)
                self._record_token_usage(resp, "solutions")  # 记录 token 消耗
                output_dict = self.output_parser.parse(resp.content)
            except Exception as e:
                print(f"⚠️ 解析失败 {label}: {e}")
                # 回退到普通翻译
                prob_zh = self._fallback_translate(prob_clean)
                sols_zh = [self._fallback_translate(sc) for sc in sols_clean]
                output_dict = {
                    "problem_zh": prob_zh,
                    "solution_zh": sols_zh,
                    "final_answer": None,
                    "others": None
                }

            # 还原数学公式
            prob_zh = self.restore_math_placeholders(output_dict["problem_zh"])
            sols_zh = [self.restore_math_placeholders(s) for s in output_dict["solution_zh"]]
            final_answer_zh = output_dict.get("final_answer")
            others_zh = self.restore_math_placeholders(output_dict.get("others"))

            # 构建 Markdown（只在 category 变化时加标题）
            if category != prev_category:
                category_zh = self.CATEGORY_EN_TO_ZH.get(category, category)
                problems_lines.append(f"# {category_zh}")
                solutions_lines.append(f"# {category_zh}")
                prev_category = category

            problems_lines.extend([f"## {label}.", prob_zh, ""])
            solutions_lines.extend([
                f"## {label}.",
                prob_zh,
                *sols_zh,
                others_zh or "",
                ""
            ])
            # 保存结构化条目
            structured_items.append({
                "problem_zh": prob_zh,
                "solution_zh": sols_zh,
                "final_answer": final_answer_zh
            })

        full_text = "\n".join([
            preamble_zh.strip(),
            "",
            "\n".join(problems_lines),
            "",
            "\n".join(solutions_lines)
        ]).strip()

        return full_text, structured_items

    def _fallback_translate(self, text: str) -> str:
        """回退翻译方法（当结构化解析失败时使用）"""
        if not text.strip():
            return text
        simple_prompt = ChatPromptTemplate.from_template(
            """翻译为中文（保留 __MATH_i__）：{text}"""
        )
        messages = simple_prompt.format_messages(text=text)
        resp = self.chat.invoke(messages)
        self._record_token_usage(resp, "solutions")  # 记录 token 消耗
        return resp.content.strip()

    def extract_math_placeholders(self, text: str) -> str:
        self.math_blocks = []
        def replace_match(match):
            formula = match.group(0)
            self.math_blocks.append(formula)
            return f"__MATH_{len(self.math_blocks) - 1}__"
        pattern = r"\$\$.*?\$\$|\$.*?\$"
        return re.sub(pattern, replace_match, text, flags=re.DOTALL)

    def restore_math_placeholders(self, text: str) -> str:
        for i, formula in enumerate(self.math_blocks):
            text = text.replace(f"__MATH_{i}__", formula)
        return text
    
    def get_token_report(self) -> str:
        """返回 Token 使用报告字符串"""
        u = self.token_usage
        report = (
            f"\n{'='*50}\n"
            f"📊 Token 使用报告\n"
            f"{'='*50}\n"
            f"总调用次数: {u['call_count']}\n"
            f"输入 Token: {u['total_input']:,}\n"
            f"输出 Token: {u['total_output']:,}\n"
            f"总 Token: {u['total_input'] + u['total_output']:,}\n"
            f"{'-'*30}\n"
            f"  Preamble: {u['preamble']:,}\n"
            f"  Problems: {u['problems']:,}\n"
            f"  Solutions: {u['solutions']:,}\n"
            f"{'='*50}\n"
        )
        return report

    @staticmethod
    def _get_category(label: str) -> str:
        mapping = {"A": "Algebra", "C": "Combinatorics", "G": "Geometry", "N": "Number Theory"}
        return mapping.get(label[0], "Unknown")
    
    CATEGORY_EN_TO_ZH = {
        "Algebra": "代数",
        "Combinatorics": "组合",
        "Geometry": "几何",
        "Number Theory": "数论"
        }

    SECTION_TITLES = {
        "Problems": "题目",
        "Solutions": "解答"
    }
    
