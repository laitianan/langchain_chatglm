# # 中文
# review_template = """\
# 对于以下文本，请从中提取以下信息：
#
# 礼物：该商品是作为礼物送给别人的吗？ \
# 如果是，则回答 是的；如果否或未知，则回答 不是。
#
# 交货天数：产品需要多少天\
# 到达？ 如果没有找到该信息，则输出-1。
#
# 价钱：提取有关价值或价格的任何句子，\
# 并将它们输出为逗号分隔的 Python 列表。
#
# 使用以下键将输出格式化为 JSON：
# 礼物
# 交货天数
# 价钱
#
# 文本: {text}
# """
#
# # 中文
# review_template_2 = """\
# 对于以下文本，请从中提取以下信息：：
#
# 礼物：该商品是作为礼物送给别人的吗？
# 如果是，则回答 是的；如果否或未知，则回答 不是。
#
# 交货天数：产品到达需要多少天？ 如果没有找到该信息，则输出-1。
#
# 价钱：提取有关价值或价格的任何句子，并将它们输出为逗号分隔的 Python 列表。
#
# 文本: {text}
#
# {format_instructions}
# """

# 中文
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser

gift_schema = ResponseSchema(name="礼物",
                             description="这件物品是作为礼物送给别人的吗？\
                            如果是，则回答 是的，\
                            如果否或未知，则回答 不是。")

delivery_days_schema = ResponseSchema(name="交货天数",
                                      description="产品需要多少天才能到达？\
                                      如果没有找到该信息，则输出-1。")

price_value_schema = ResponseSchema(name="价钱",
                                    description="提取有关价值或价格的任何句子，\
                                    并将它们输出为逗号分隔的 Python 列表")


response_schemas = [gift_schema,
                    delivery_days_schema,
                    price_value_schema]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()
print(format_instructions)
