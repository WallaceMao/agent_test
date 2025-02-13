from .myswarm import FunctionResult

# from .myswarm import Swarm, Agent
# from dotenv import load_dotenv
#
# load_dotenv()
#
# client = Swarm()
#
# agent = Agent(
#     name="我的智能体",
#     instructions="你是一个有用的智能体"
# )

from typing import Callable, Union, List

# from pydantic import BaseModel
#
# #ClassA = Callable[[], Union[str, 'ClassB', dict]]
#
#
# class Child(BaseModel):
#     name: str
#     parent: 'Parent' = None
#
#
# class Parent(BaseModel):
#     name: str
#     child: Child = None
#
#
# parent = Parent(name="Wallace")
# child = Child(name="son", parent=parent)
#
# print(child.parent.name)

def test_modify(d: dict):
    d['from_test'] = "FROM_TEST"


map = {"abc": 123}

test_modify(map)

print(map)

# def test(a: str):
#     return 111
#
# print(test.__code__.co_name)
# sig = inspect.signature(test)
# print(test.__doc__)
# doc_tree = publish_doctree(test.__doc__.strip()).asdom()
# xml_string = doc_tree.toxml()
# print(xml_string)
# xml_tree = ET.parse(doc_tree.toxml())
# print(f"xml_tree: {xml_tree.getroot()}")
# field_list = xml_tree.findall("field_list")
# print(field_list)

# xml_string = '<?xml version="1.0" ?><document source="&lt;string&gt;"><paragraph>这是test函数的说明</paragraph><block_quote><field_list><field><fie>param a</field_name><field_body><paragraph>这是参数a</paragraph></field_body></field><field><field_name>return</field_name><field_body><paragraph>这是返回值</paragraph></f></field></field_list></block_quote></document>'
# xml_string = '<?xml version="1.0" ?><document source="&lt;string&gt;"><paragraph>这是test函数的说明</paragraph><block_quote><field_list><field><field_name>param a</field_name><field_body><paragraph>这是参数a</paragraph></field_body></field><field><field_name>return</field_name><field_body><paragraph>这是返回值</paragraph></field_body></field></field_list></block_quote></document>'
# tree = ET.parse(xml_string)

# doc_tree = etree.fromstring(doc_tree.toxml())
# print(doc_tree)
# print(doc_tree.getElementsByTagName("a"))
# for p in sig.parameters.values():
#     print(f"==> 参数：{p.name}\n{p.annotation}\n{p.default}")
# d = {}
# def_dict = defaultdict(str, {})
# print(f"字典中的取值是： {d['abc']}")


