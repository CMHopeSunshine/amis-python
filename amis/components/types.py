from typing import List, Literal, Optional, TYPE_CHECKING, TypeAlias, Union
from typing_extensions import NotRequired, TypedDict

from amis.base import AmisNode, BaseAmisModel
from amis.typing import DictStrAny, Expression

if TYPE_CHECKING:
    from .data_presentation import Tpl

API: TypeAlias = Union[str, "AmisAPI"]
Template: TypeAlias = Union[str, "Tpl", DictStrAny]
SchemaNode: TypeAlias = Union[AmisNode, List[Union[AmisNode, Template]], Template]


class AmisAPI(BaseAmisModel):
    """API 类型用于配置请求接口的格式，涉及请求方式、请求地址、请求数据体等等相关配置

    link: https://aisuda.bce.baidu.com/amis/zh-CN/docs/types/api"""

    class Messages(TypedDict):
        success: NotRequired[str]
        """请求成功提示信息"""
        failed: NotRequired[str]
        """请求失败提示信息"""

    url: Template
    """当前接口 Api 地址"""
    method: Literal["get", "post", "put", "delete"] = "get"
    """请求方式 支持：get、post、put、delete"""
    data: Optional[Union[str, DictStrAny]] = None
    """请求的数据体,支持数据映射"""
    dataType: Optional[Literal["json", "form", "form-data"]] = None
    """
    - 默认为 json 可以配置成 form 或者 form-data
    - 当 data 中包含文件时，自动会采用 form-data（multipart/form-data） 格式。
    - 当配置为 form 时为 application/x-www-form-urlencoded 格式
    """
    qsOptions: Union[str, DictStrAny, None] = None
    """
    - 当 dataType 为 form 或者 form-data 的时候有用
    - 具体参数请参考这里，默认设置为: { arrayFormat: 'indices', encodeValuesOnly: true }
    """
    headers: Optional[DictStrAny] = None
    """请求的头部信息"""
    sendOn: Optional[Expression] = None
    """配置请求条件"""
    cache: Optional[int] = None
    """
    - 设置cache来设置缓存时间，单位是毫秒，在设置的缓存时间内，
    同样的请求将不会重复发起，而是会获取缓存好的请求响应数据。
    - 发送适配器 , amis 的 API 配置，如果无法配置出你想要的请求结构，那么可以配置requestAdaptor发送适配器
    """
    requestAdaptor: Optional[str] = None
    """如果接口返回的数据结构不符合预期，可以通过配置 responseData来修改，同样支持数据映射"""  # noqa: E501
    responseData: Optional[DictStrAny] = None
    """
    - 可用来映射的数据为接口的实际数据（接口返回的 data 部分），额外加 api 变量。
    - 其中 api.query 为接口发送的 query 参数，api.body 为接口发送的内容体原始数据
    """
    replaceData: bool = False
    """返回的数据是否替换掉当前的数据，默认为 false，即：追加，设置成 true 就是完全替换"""
    adaptor: Optional[str] = None
    """
    - 接收适配器名称, 如果接口返回不符合要求，可以通过配置一个适配器来处理成 amis 需要的。
    - 同样支持 Function 或者 字符串函数体格式
    """
    responseType: Optional[Literal["blob"]] = None
    """返回类型 ,如果是下载需要设置为 'blob'"""
    autoRefresh: Optional[bool] = None
    """配置是否需要自动刷新接口"""
    trackExpression: Optional[str] = None
    """
    配置跟踪变量表达式,当开启自动刷新的时候，默认是 api 的 url 来自动跟踪变量变化的。
    如果你希望监控 url 外的变量，请配置 traceExpression。
    """
    messages: Optional[Messages] = None
    """
    - 配置接口请求的提示信息，
    - messages.success 表示请求成功提示信息
    - messages.failed 表示请求失败提示信息
    """


class Horizontal(TypedDict):
    """配置页面占比"""

    left: NotRequired[int]
    """左边 label 的宽度占比"""
    right: NotRequired[int]
    """右边控制器的宽度占比。"""
    offset: NotRequired[int]
    """当没有设置 label 时，右边控制器的偏移量"""
    justify: NotRequired[bool]
    """是否两端对齐"""


class Validation(BaseAmisModel):
    """值检验"""

    isEmail: Optional[bool] = None
    """必须是 Email。"""
    isUrl: Optional[bool] = None
    """必须是 Url。"""
    isNumeric: Optional[bool] = None
    """必须是 数值。"""
    isAlpha: Optional[bool] = None
    """必须是 字母。"""
    isAlphanumeric: Optional[bool] = None
    """必须是 字母或者数字。"""
    isInt: Optional[bool] = None
    """必须是 整形。"""
    isFloat: Optional[bool] = None
    """必须是 浮点形。"""
    isLength: Optional[int] = None
    """是否长度正好等于设定值。"""
    minLength: Optional[int] = None
    """最小长度。"""
    maxLength: Optional[int] = None
    """最大长度。"""
    maximum: Optional[int] = None
    """最大值。"""
    minimum: Optional[int] = None
    """最小值。"""
    equals: Optional[str] = None
    """当前值必须完全等于 xxx。"""
    equalsField: Optional[str] = None
    """当前值必须与 xxx 变量值一致。"""
    isJson: Optional[bool] = None
    """是否是合法的 Json 字符串。"""
    isUrlPath: Optional[bool] = None
    """是 url 路径。"""
    isPhoneNumber: Optional[bool] = None
    """是否为合法的手机号码"""
    isTelNumber: Optional[bool] = None
    """是否为合法的电话号码"""
    isZipcode: Optional[bool] = None
    """是否为邮编号码"""
    isId: Optional[bool] = None
    """是否为身份证号码，没做校验"""
    matchRegexp: Optional[str] = None
    """必须命中某个正则。 /foo/"""


__all__ = [
    "API",
    "Template",
    "SchemaNode",
    "AmisAPI",
    "Horizontal",
    "Validation",
]
