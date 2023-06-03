from typing import Dict, Any, Union, List, Literal

try:
    import ujson as json
except ImportError:
    import json
from pydantic import BaseModel, Extra

Expression = str
Template = Union[str, "Tpl", dict]
SchemaNode = Union[Template, "AmisNode", List["AmisNode"], dict]
OptionsNode = Union[List[dict], List[str]]


class BaseAmisModel(BaseModel):
    class Config:
        extra = Extra.allow
        json_loads = json.loads
        json_dumps = json.dumps

    def to_json(self):
        return self.json(exclude_none=True, by_alias=True, ensure_ascii=False, indent=4)

    def to_dict(self):
        return self.dict(exclude_none=True, by_alias=True)

    def update_from_dict(self, kwargs: Dict[str, Any]):
        for k, v in kwargs.items():
            setattr(self, k, v)
        return self

    def update_from_kwargs(self, **kwargs):
        return self.update_from_dict(kwargs)


class BaseAmisApiOut(BaseAmisModel):
    """api接口输出数据格式"""
    status: int = 0
    """状态码，0代表成功，其他代表失败"""
    msg: str = ''
    """提示信息"""
    data: dict = None
    """回传数据"""


class AmisNode(BaseAmisModel):
    """组件配置"""
    type: str = None
    """组件类型"""
    visible: bool = None
    """是否显示，True为显示,False为隐藏，默认为True"""
    hidden: bool = None
    """是否隐藏，True为隐藏,false为显示，默认为False"""
    visibleOn: Expression = None
    """显示表达式"""
    hiddenOn: Expression = None
    """隐藏表达式"""
    id: str = None
    """组件ID"""
    name: str = None
    """组件字段名"""
    value: str = None
    """组件字段值"""
    onEvent: dict = None
    """组件事件"""


class AmisAPI(BaseAmisModel):
    url: Template = None
    """当前接口 Api 地址"""
    method: Literal["get", "post", "put", "delete"] = None
    """请求方式 支持：get、post、put、delete"""
    data: Union[str, dict] = None
    """请求的数据体,支持数据映射"""
    dataType: str = "json"
    """
    - 默认为 json 可以配置成 form 或者 form-data
    - 当 data 中包含文件时，自动会采用 form-data（multipart/form-data） 格式。
    - 当配置为 form 时为 application/x-www-form-urlencoded 格式
    """
    qsOptions: Union[str, dict] ={ "arrayFormat": 'indices', "encodeValuesOnly": True }
    """
    - 当 dataType 为 form 或者 form-data 的时候有用
    - 具体参数请参考这里，默认设置为: { arrayFormat: 'indices', encodeValuesOnly: true }
    """
    headers: Dict[str, Any] = None
    """请求的头部信息"""
    sendOn: Expression = None
    """配置请求条件"""
    cache: int = None
    """
    - 设置cache来设置缓存时间，单位是毫秒，在设置的缓存时间内，同样的请求将不会重复发起，而是会获取缓存好的请求响应数据。
    - 发送适配器 , amis 的 API 配置，如果无法配置出你想要的请求结构，那么可以配置requestAdaptor发送适配器
    """
    requestAdaptor: str = None
    """如果接口返回的数据结构不符合预期，可以通过配置 responseData来修改，同样支持数据映射"""
    responseData: Dict[str, Any] = None
    """
    - 可用来映射的数据为接口的实际数据（接口返回的 data 部分），额外加 api 变量。
    - 其中 api.query 为接口发送的 query 参数，api.body 为接口发送的内容体原始数据
    """
    replaceData: bool = False
    """返回的数据是否替换掉当前的数据，默认为 false，即：追加，设置成 true 就是完全替换"""
    adaptor: str = None
    """
    - 接收适配器名称, 如果接口返回不符合要求，可以通过配置一个适配器来处理成 amis 需要的。
    - 同样支持 Function 或者 字符串函数体格式
    """
    responseType: str = None
    """返回类型 ,如果是下载需要设置为 'blob'"""
    autoRefresh: bool = None
    """配置是否需要自动刷新接口"""
    trackExpression: str = None
    """
    配置跟踪变量表达式,当开启自动刷新的时候，默认是 api 的 url 来自动跟踪变量变化的。
    如果你希望监控 url 外的变量，请配置 traceExpression。
    """
    messages: Dict[str, Any] = None
    """
    - 配置接口请求的提示信息，
    - messages.success 表示请求成功提示信息
    - messages.failed 表示请求失败提示信息
    """


API = Union[str, AmisAPI, dict]


class Tpl(AmisNode):
    type: str = "tpl"
    """指定为 Tpl 组件"""
    tpl: Template = None
    """配置模板"""
    className: str = None
    """外层 Dom 的类名"""
    showNativeTitle: bool = None
    """是否设置外层 DOM 节点的 title 属性为文本内容"""


class Event(BaseAmisModel):
    actionType: str = None
    """动作名称"""
    args: dict = None
    """动作参数{key:value}，支持数据映射"""
    data: Dict[str, Any] = None
    """追加数据{key:value}，支持数据映射，如果是触发其他组件的动作，则该数据会传递给目标组件，> 2.3.2 及以上版本"""
    dataMergeMode: str = "merge"
    """当配置了 data 的时候，可以控制数据追加方式，支持合并(merge)和覆盖(override)两种模式，> 2.3.2 及以上版本"""
    preventDefault: Union[bool, Expression] = False
    """阻止事件默认行为，> 1.10.0 及以上版本支持表达式，> 2.9.0 及以上版本支持ConditionBuilder"""
    stopPropagation: Union[bool, Expression] = False
    """停止后续动作执行，> 1.10.0 及以上版本支持表达式，> 2.9.0 及以上版本支持ConditionBuilder"""
    expression: Union[bool, Expression] = None
    """执行条件，不设置表示默认执行，> 1.10.0 及以上版本支持表达式，> 2.9.0 及以上版本支持ConditionBuilder"""
    outputVar: str = None
    """输出数据变量名"""
