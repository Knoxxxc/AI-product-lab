def identify_industry(question):
    industry_rules = {
        '金融业': ['银行', '证券', '券商', '基金', '保险', '信托', '期货', '资管', '私募'],
        '医疗健康': ['医院', '医疗', '医生', '患者', '药企'],
        '制造业': ['工厂', '制造', '生产', '设备', '产线'],
        '教育行业': ['学校', '教育', '教师', '学生', '培训'],
        '专业服务': ['咨询', '律所', '会计师事务所', '审计']
    }

    for industry, keywords in industry_rules.items():
        for keyword in keywords:
            if keyword in question:
                return industry

    return '未知行业'

def classify_requirement(question):
    requirement_rules = {
        '知识问答': ['知识', '资料', '制度', '文档', '问答'],
        '流程自动化': ['自动', '流程', '审批', '处理'],
        '数据分析': ['数据', '分析', '报表', '指标']
    }

    for requirement_type, keywords in requirement_rules.items():
        for keyword in keywords:
            if keyword in question:
                return requirement_type

    return '需要进一步沟通'


def create_analysis_template(question):
    analysis = {
        'customer_input': question,
        'industry': identify_industry(question),
        'requirement_type': classify_requirement(question),
        'business_goal': '待分析',
        'pain_points': [],
        'constraints': [],
        'unknowns': [],
        'followup_questions': [],
        'initial_solution': '待分析',
        'risks': []
    }

    return analysis


question = input('请输入客户需求：')
result = create_analysis_template(question)

print('客户原始需求：', result['customer_input'])
print('行业：', result['industry'])
print('需求类型：', result['requirement_type'])
print('待确认信息：', result['unknowns'])