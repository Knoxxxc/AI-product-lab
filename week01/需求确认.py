def classify_requirement(question):
    if '知识' in question or '资料' in question or '知识库' in question:
        return '知识问答'
    elif '自动' in question or '流程' in question:  
        return '流程自动化'
    elif '数据' in question or '分析' in question or '报表' in question:
        return '数据分析'
    else:
        return '需要进一步沟通'

def identify_industry(question):
    if '金融' in question or '银行' in question or '证券' in question:
        return '金融业'
    elif '医疗' in question or '医院' in question or '健康' in question:
        return '医疗行业'
    elif '教育' in question or '学校' in question or '培训' in question:
        return '教育业'
    elif '工厂' in question or '制造' in question or '生产' in question:
        return '制造业'
    else:
        return '未知行业'

def generate_followup(industry,requirement_type):
    if industry=='金融业' and requirement_type=='知识问答':
        return '请提供具体的金融知识问题，我们将为您提供详细解答。'
    elif industry=='金融业' and requirement_type=='数据分析':
        return '请提供金融数据，我们将为您进行深入分析。'
    elif industry=='医疗行业' and requirement_type=='流程自动化':
        return '请描述您希望自动化的医疗流程，我们将为您提供解决方案。'
    elif industry=='医疗行业' and requirement_type=='数据分析':
        return '请提供医疗数据，我们将为您进行深入分析。'
    elif industry=='教育业' and requirement_type=='数据分析':
        return '请提供教育数据，我们将为您进行深入分析。'
    elif industry=='教育业' and requirement_type=='知识问答':
        return '请提出具体的教育知识问题，我们将为您提供详细解答。'
    elif industry=='制造业' and requirement_type=='流程自动化':
        return '请描述您希望自动化的制造流程，现有流程和预期效果。'
    else:
        return '请提供更多信息，以便我们更好地理解您的需求。'

    
question=input('请输入你的问题:')
requirement_type=classify_requirement(question)
industry=identify_industry(question)
followup=generate_followup(industry,requirement_type)
print('需求类型', requirement_type)
print('行业类型', industry)
print('追问', followup)