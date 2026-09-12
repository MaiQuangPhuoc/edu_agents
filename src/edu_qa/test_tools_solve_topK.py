# import re
# import json
# from pathlib import Path

# import re
# import json
# import ast


# def normalize_tool_name(tool_name: str) -> str:
#     return tool_name.replace("_tool", "").strip()


# def build_result_tool(result_file):

#     with open(result_file, encoding="utf-8") as f:
#         content = f.read()

#     blocks = re.findall(
#         r"(Query \d+:.*?)(?=Query \d+:|$)",
#         content,
#         flags=re.DOTALL
#     )

#     output_file = result_file.replace(".md", "_tool.md")

#     with open(output_file, "w", encoding="utf-8") as f:

#         for block in blocks:

#             # Query gốc
#             query_match = re.search(
#                 r"Query\s+(\d+):\s*(.*)",
#                 block
#             )

#             if not query_match:
#                 continue

#             query_id = query_match.group(1)
#             query_text = query_match.group(2).strip()

#             # Tool đúng nằm trong (...)
#             gt_match = re.search(
#                 r"\((.*?)\)",
#                 query_text
#             )

#             gt_tool = gt_match.group(1).strip() if gt_match else ""

#             # Lấy metadata top 1 2 3
#             metadata_blocks = re.findall(
#                 r"metadata:\s*(\{.*?\})",
#                 block,
#                 flags=re.DOTALL
#             )

#             pred_tools = []

#             for meta_str in metadata_blocks[:3]:

#                 try:
#                     meta = ast.literal_eval(meta_str)
#                 except:
#                     try:
#                         meta = json.loads(meta_str)
#                     except:
#                         meta = {}

#                 tool_name = normalize_tool_name(
#                     meta.get("tool_name", "")
#                 )

#                 pred_tools.append(tool_name)

#             while len(pred_tools) < 3:
#                 pred_tools.append("")

#             results = [
#                 "✅" if t == gt_tool else "❌"
#                 for t in pred_tools
#             ]

#             f.write(f"Query {query_id}: {query_text}\n\n")
#             f.write(f"Tool 1: {pred_tools[0]}\n")
#             f.write(f"Tool 2: {pred_tools[1]}\n")
#             f.write(f"Tool 3: {pred_tools[2]}\n\n")
#             f.write(f"Result Tool: {' '.join(results)}\n")
#             f.write("=" * 80 + "\n\n")

#     print(f"Saved: {output_file}")


# build_result_tool(r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\chunk\tools\test_tools_result.md")

# --------------------
import re

def update_result_tool(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = re.split(r"(?=Query \d+:)", content)

    new_blocks = []

    for block in blocks:

        if not block.strip():
            continue

        # Query 1: ... (xet_menh_de)
        query_match = re.search(r"Query\s+\d+:\s+.*\((.*?)\)", block)
        if not query_match:
            new_blocks.append(block)
            continue

        gt_tool = query_match.group(1).strip()

        tool1 = re.search(r"Tool 1:\s*(.+)", block)
        tool2 = re.search(r"Tool 2:\s*(.+)", block)
        tool3 = re.search(r"Tool 3:\s*(.+)", block)

        tools = [
            tool1.group(1).strip() if tool1 else "",
            tool2.group(1).strip() if tool2 else "",
            tool3.group(1).strip() if tool3 else ""
        ]

        results = [
            "✅" if tool == gt_tool else "❌"
            for tool in tools
        ]

        new_result = f"Result Tool: {' '.join(results)}"

        block = re.sub(
            r"Result Tool:\s*.*",
            new_result,
            block
        )

        new_blocks.append(block)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("".join(new_blocks))

    print("Done")


if __name__ == "__main__":

    update_result_tool(
        r"D:\VKU\Nam_3\thuc_tap_doanh_nghiep_he_eSTI\EDUAGENT\src\modules\documents\doc_git\books\10\chunk\tools\test_tools_result_tool.md"
    )