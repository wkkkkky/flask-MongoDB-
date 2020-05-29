from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

class NewsForm(FlaskForm):
    '''新闻表单'''
    title = StringField('新闻标题',validators=[DataRequired("请输入标题")],
        description="请输入标题",
        render_kw={"required":"required","class":"form-control"})
    type = StringField('新闻类型',validators=[DataRequired("请输入类型")],
        description="请输入类型",
        render_kw={"required":"required","class":"form-control"})
    content = StringField('新闻内容',validators=[DataRequired("请输入内容")],
        description="请输入内容",
        render_kw={"required":"required","class":"form-control"})
    submit = SubmitField('提交')