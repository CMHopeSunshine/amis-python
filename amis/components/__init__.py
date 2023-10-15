from amis.event import (
    AjaxAction,
    CopyAction,
    DialogAction,
    DrawerAction,
    EventAction as EventAction,
)

from .data_input import *
from .data_presentation import *
from .feature import *
from .feedback import *
from .layout import *
from .other import *
from .types import *

# update forward refs
CRUD.update_forward_refs(Form=Form, Action=Action, AmisAPI=AmisAPI, Tpl=Tpl)
Table.update_forward_refs(Action=Action, PopOver=PopOver, Badge=Badge)
Calendar.update_forward_refs(Action=Action)
Card.update_forward_refs(Action=Action)
GridNav.update_forward_refs(Action=Action, Badge=Badge)
AmisList.update_forward_refs(Action=Action, AmisAPI=AmisAPI)
Panel.update_forward_refs(Action=Action, Tpl=Tpl)

PageSchema.update_forward_refs(Iframe=Iframe, Page=Page, AmisAPI=AmisAPI, Tpl=Tpl)
Action.update_forward_refs(Badge=Badge, Tpl=Tpl)
Nav.update_forward_refs(Badge=Badge, AmisAPI=AmisAPI, Tpl=Tpl)
Icon.update_forward_refs(Badge=Badge)

Tabs.update_forward_refs(Icon=Icon, Tpl=Tpl)
Portlet.update_forward_refs(Icon=Icon, Tpl=Tpl)

Page.update_forward_refs(Remark=Remark, AmisAPI=AmisAPI, Tpl=Tpl)

AjaxAction.update_forward_refs(API=API, AmisAPI=AmisAPI)
DialogAction.update_forward_refs(Dialog=Dialog)
DrawerAction.update_forward_refs(Drawer=Drawer)
CopyAction.update_forward_refs(Tpl=Tpl)
