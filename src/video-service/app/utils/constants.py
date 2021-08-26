# -*- coding: utf-8 -*-
"""
@Time    : 10/28/20 11:10 PM
@Author  : Lucky
@Email   : lucky_soft@163.com
@File    : constants.py
@Desc    : Description about this file
"""
from enum import Enum, unique

# 阿里云OSS配置
ACCESS_KEY = 'LTAI4GEzHGWXfv4CKPVdG4j9'
ACCESS_KEY_SECRET = 'h4KbEzYYlM8Hmzamu4GlLpy9hBCfvZ'

USE_CACHE = True

# HTTP status code
@unique
class StatusCode(Enum):
    OK = {0: 'error'}
    SUCCESS = {1: 'success'}
    FAILED = {2: '操作失败'}
    PARAM_ERROR = {3: '参数错误'}
    UNLOGIN = {5: '未登录'}
    LOGIN_TIMEOUT = {6: '登录超时'}
    USER = {7: '用户 '}
    SIGN_UP_SUCCESS = {1001: '注册成功'}
    LOGIN_SUCCESS = {1002: '登录成功'}
    SEND_SMS_SUCCESS = {1003: '短信发送成功'}
    BIND_SUCCESS = {1004: '绑定成功'}
    MODIFY_SUCCESS = {1005: '修改成功'}
    MOBILE_VERIFY_FAILED = {1006: '手机号验证失败'}
    DELETE_SUCCESS = {1007: '删除成功'}
    ADD_SUCCESS = {1008: '添加成功'}
    ADD_ARRAY_SUCCESS = {1009: '数据组添加成功'}
    SET_TAG_SUCCESS = {1010: '标签设置成功'}
    SEND_EMAIL_VERIFY = {1011: '邮箱验证已发送'}
    EMAIL_VERIFY_FAILED = {1012: '邮箱验证失败'}
    ACTION_FREQUENTLY = {1013: '操作频繁稍后重试'}
    SEND_EMAIL_INVITATION = {1014: '邮件邀请已发送'}
    ACCOUNT_TIMEOUT = {1015: '账号已到期'}
    FREE_TRIAL_TIMEOUT = {1016: '您的账号的免费试用期即将到期，若要继续使用请续费'}
    EMAIL_FORMAT_ERROR = {2001 : '邮箱格式不正确'}
    PASSWORD_EMPTY_ERROR = {2002 : '密码不能为空'}
    EMAIL_EXIST = {2003 : '邮箱已存在'}
    USERNAME_EMPTY_ERROR = {2004 : '用户名不能为空'}
    ACCOUNT_NOT_EXIST = {2005 : '账号不存在'}
    ACCOUNT_FORMAT_ERROR = {2006 : '账号格式有误'}
    TRY_LATER = {2007 : '稍后再试'}
    MSG_ALREADY_SEND = {2008 : '信息已发送'}
    VERIFICATION_ERROR = {2009 : '验证码错误'}
    MOBILE_ALREADY_BIND = {2010 : '用户已绑定此手机号'}
    MOBILE_BIND_OTHER = {2011 : '手机号已经绑定其他帐号'}
    PASSWORD_SAME = {2012 : '与原密码相同'}
    OLD_PASSWORD_ERROR = {2013 : '原密码错误'}
    BIND_MOBILE = {2014 : '请绑定手机号'}
    PASSWORD_ERROR = {2015 : '密码错误'}
    USER_UNNORMAL = {2016 : '用户异常'}
    LEAVE_EMAIL = {2017 : '请填写邮箱'}
    USER_NOT_GROUP = {2018 : '该用户不属于此用户组'}
    GROUP_EXIST = {2019 : '组名已存在'}
    USER_NOT_IN_GROUP = {2020 : '部分成员不在集合中'}
    USERNAME_FORMAT_ERROR = {2023 : '用户名格式错误'}
    USER_NOT_IN_ORGNIZATION = {2025 : '用户不在组织下'}
    MOBILE_EXIST = {2026 : '该手机号已存在'}
    ACCOUNT_NUM_FULL = {2027 : '你可创建的账号数已满，可删除后创建'}
    LEVEL_ERROR = {2029 : '权限等级不足'}
    CONTACT_INFO = {2030 : '暂不对外提供注册服务，如若需要请联系我们：18699108210'}

    PROJECT_NOT_EXIST = {3001 : '项目不存在'}
    PROJECT_DELETED  = {3002 : '项目已删除'}
    NO_PERMISSION = {3003 : '没有权限'}
    PROJECT_NAME_EMPTY = {3004 : '项目名不能为空'}
    PROJECT_NAME_EXIST = {3005 : '名称已存在'}
    ALREADY_IN_GROUP = {3006 : '已经是该组成员，请勿重复添加'}
    PROJECT_ULTRA_VIRES = {3007 : '项目权限逾越'}
    CHOOSE_PERMISSION = {3008 : '请选择权限'}
    USER_NOT_IN_PROJECT = {3009 : '用户不在项目中'}
    DATA_PROCESSING = {3010 : '数据处理中'}
    DATA_EXIST = {3011 : '数据已经存在'}
    DATA_NOT_EXIST = {3012 : '数据不存在'}
    DATA_NOT_INITIAL = {3013 : '数据状态非初审状态'}
    DATA_FORMAT_ERROR = {3014 : '数据格式错误'}
    NO_DATA = {3015 : '没有数据'}
    ANN_TIME_ERROR = {3016 : '标注时间有误'}
    QUEUE_NO_DATA = {3017 : '队列无数据，不能提交'}
    DATA_ALREADY_CHECK = {3018 : '数据已审核'}
    PROJECT_NO_TEMPLATE = {3019 : '项目模板不存在'}
    INPUT_FILE_NAME = {3020 : '请输入文件名'}
    DEMO_PROJECT = {3021 : '示例项目'}
    CHECK_DEMO = {3022 : '查看示例项目，快速掌握LabelHub使用方式。'}
    ACCEPT_NUM_LESS_CHECK = {3023 : '验收数量不可大于质检通过数量'}
    ACCEPT_NUM_MAX = {3024 : '验收数量已超出默认的最大值'}

    UPLOAD_FILE_LIMIT = {4001 : '只允许上传jpeg,jpg,gif,png格式的文件'}
    UPLOAD_FILE_SIZE_LIMIT = {4002 : '请上传5M以内的文件'}
    UPLOAD_FAILED = {4003 : '上传失败'}
    FILE_DELETE = {4004 : '文件已删除'}
    PERMISSION_UNUSUAL = {4005 : '权限异常，请联系管理员处理'}
    PERMISSION_LESS = {4006 : '权限不足，请联系管理员处理'}
    PERMISSION_SET_ERROR = {4007 : '权限设置有误'}
    NOT_GOURP_MEMBER = {4009 : '非该组用户，不可修改'}
    DATA_STRUCTURE_ERROR = {4010 : '数据结构有误'}
    ADD_DATA_PERMISSION_ERROR = {4011 : '权限数据添加有误'}
    PROJECT_PERMISSION_ERROR = {4012 : '项目权限出错'}
    VERIFY_ERROR = {4014 : '验证错误'}
    DATA_INVALID = {4015 : '数据无效'}
    SYSTEM_UNUSUAL = {4017 : '系统异常'}
    DATA_UNUSUAL = {4018 : '数据异常'}
    NO_PROJECT_IN_GROUP = {4021 : '组织下没有项目'}
    UPLOAD_FILE = {4022 : '请上传文件'}
    STORAGE_OUT = {4023 : '上传存储已用完，如若需要请联系运营人员：18699108210'}
    UPLOAD_SUCCESS = {4024 : '上传成功'}
    FILE_DAMAGE = {4026 : '图片已损坏，无法上传'}
    TAG_EXIST = {5001 : '标签已经存在'}
    TAG_NOT_EXIST = {5002 : '标签不存在'}
    TAG_NUM_OVERSIZE = {5003 : '标签数量已达上限'}
    TAG_TEMP_NOT_EXIST = {5004 : '标注模板不存在'}
    LIKED = {6001 : '您已点赞'}
    CANCELED = {6002 : '已取消'}
    NO_PERMISSION_FILE_ACTION = {7002 : '不存在对此类别文件的操作权限'}
    DATA_REPEAT = {7003 : '数据已重复'}

    PENDING = {9002 : '待质检'}
    ADOPT = {9003 : '通过'}
    UNADOPT = {9004 : '未通过'}
    MODIFIED = {9005 : '已修改'}
    PENDING_ANN = {9006 : '待标注'}
    SUBMIT = {9007 : '提交'}
    SKIP = {9008 : '跳过'}
    SUPER_ADMIN = {9009 : '超级管理员'}
    ADMIN = {9010 : '管理员'}
    PROJECT_ADMIN = {9011 : '项目管理员'}
    QA_USER = {9012 : '质检员'}
    ANNOTATOR = {9013 : '标注着'}
    GUEST = {9014 : '访客'}
    OTHERS = {9015 : '其他'}
    INVITE_COMEIN = {9016 : '邀请入驻:'}
    INVITE_URL = {9017 : '邀请入驻链接:'}
    IMAGE_ANNOTATION = {9018 : '图片标注'}
    BASIC_VERSION = {9019 : '基础版'}
    HIGHER_VERSION = {9020 : '进阶版'}
    ENTERPRISE_VERSION = {9021 : '企业版'}
    TEXT_ANNOTATION = {9022 : '文本标注'}
    VIDEO_ANNOTATION = {9023 : '视频标注'}
    LOGIN_ACCOUNT = {9025 : '  登录账号'}
    PASSWORD = {9026 : '  密码'}
    VERIFY = {9027 : '验证'}

    # 地址路由配置

    NEW_MEMBER = {10001 : '新成员'}
    PROJECT_PERMISSION = {10002 : '项目权限'}
    ANNOTATE_TEMP = {10003 : '标注模板'}
    FQ = {10004 : '互动问答'}
    WORK_DAIRY = {10005 : '工作笔记'}
    SUGGESTION = {10006 : '建议反馈'}
    ANNOTATE_RULE = {10007 : '标注规则'}
    EXPORT = {10008 : '导出'}
    QA = {10009 : '质检'}
    CREATED = {20001 : '创建了'}
    UPDATED = {20002 : '更新了'}
    DELETED = {20003 : '删除了'}
    REPLIED = {20004 : '回复了'}
    UPLOADED = {20005 : '上传了'}
    ADDED = {20006 : '添加了'}
    XML = {20007 : 'XML'}
    JSON = {20008 : 'JSON'}
    CSV = {20009 : 'CSV'}
    XML_IMAGE = {200010 : 'XML+图片'}
    SEGMENTATION = {200011 : '语义分割'}
    ICDAR = {200013 : 'ICDAR'}
    VIA = {200014 : 'VIA'}
    PAY_ATTENSION = {200015 : 'LabelHub付费通知'}

    # 邮件msg

    WELCOME_INFO = {30001 : '欢迎使用Labelhub!'}
    ACCOUNT_INFO = {30002 : '您已经成功注册Labelhub数据标注平台，以下是您的账号信息'}
    USERNAME_IS = {30003 : '用户名：'}
    PASSWORD_IS = {30004 : '密码：'}
    GOTO_SIGN_IN = {30005 : '前往登录'}
    VERIFY_INFO = {30006 : '以下是您的验证码信息'}
    VERIFY_CODE = {30007 : '验证码：'}

    # 成员绩效导出问题
    USERNAME = {40001 : '用户名'}
    ANNOTATE_IMAGE = {40002 : '标注图片'}
    AVERAGE_TIME = {40003 : '平均时长'}
    MID_TIME = {40004 : '中位时长'}
    QA_TIMES = {40005 : '质检次数'}
    TOTAL_TIME = {40006 : '总工时'}
    TAG_NUM = {40007 : '标签数量'}
    ANNOTATE_ADOPT_PERCENTAGE = {40008 : '标注通过率'}
    TOTAL_RATE = {40009 : '完成总量排名'}
    QA_IMAGE = {400010 : '质检图片'}
    SECONDARY_TAG = {400012 : '二级标签'}

    def get_code(self):
        return list(self.value.keys())[0]

    def get_msg(self):
        return list(self.value.values())[0]

