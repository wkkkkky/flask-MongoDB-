from flask import Flask,render_template,redirect,url_for,flash,abort,request
from flask_mongoengine.wtf import model_form
from flask_mongoengine import MongoEngine
from flask_bootstrap import Bootstrap
from datetime import datetime

from form import NewsForm


app = Flask(__name__)
#防止csrf攻击
app.config["SECRET_KEY"] = "123456"

app.config['MONGODB_SETTINGS'] = {
    'db': 'Mongo_news',
    'host': '127.0.0.1',
    'port': 27017
}
db = MongoEngine(app)
bootstrap = Bootstrap(app)

NEWS_TYPES = (
    ('推荐','推荐'),
    ('百家','百家'),
    ('本地','本地'),
    ('图片','图片')
)

class News(db.Document):
    '''新闻模型'''
    title = db.StringField(required=True)
    img_url = db.StringField()
    content = db.StringField(required=True)
    is_valid = db.BooleanField(default=True)
    news_type = db.StringField(required=True,choices=NEWS_TYPES)
    created_at = db.DateTimeField(default=datetime.now())
    updated_at = db.DateTimeField(default=datetime.now())
    meta = {
        'collection':'news',
        'ordering':['-created_at']
    }

    def clean(self):
        if '黄' in self.title:
            raise db.ValidationError('不能有黄字')

@app.route('/')
def index():

    '''新闻首页''' 
    news_list=News.objects.filter(is_valid=True)
    
    return render_template('index.html',news_list=news_list)

@app.route('/cat/<name>')
def cat(name):
    '''新闻类别'''
    '''查询类别为name的数据'''
    news_list=News.objects.filter(is_valid=True,news_type=name)
    return render_template('cat.html',name=name ,news_list=news_list)

@app.route('/detail/<pk>/')
def detail(pk):
    '''新闻详情信息'''
    news_obj=News.objects.filter(pk=pk).first_or_404()  
    return render_template('detail.html',news_obj=news_obj)

@app.route('/admin')
@app.route('/admin/<int:page>')
def admin(page=None):
    '''新闻管理首页'''
    if page == None:
        page = 1
    page_data = News.objects.filter(is_valid=True).paginate(page=page,per_page=5)
    return render_template('admin/index.html',page_data=page_data,page=page)

@app.route('/admin/add/',methods=('GET','POST'))
def add():
    '''新闻新增界面'''
    form = NewsForm()
    if form.validate_on_submit():
        new_obj = News(
            title = form.title.data,
            news_type=form.type.data,
            content=form.content.data,
            is_valid=1,
        )
        new_obj.save()
        flash('新增成功')
        #文字提示
        return redirect(url_for('admin'))
    return render_template('admin/add.html',form=form)


@app.route('/admin/update/<pk>/',methods=('GET','POST'))
def update(pk):
    '''新闻修改'''
    new_obj = News.objects.get_or_404(pk=pk)
    if not new_obj:
        return render_template(url_for('admin'))
    form = NewsForm(obj=new_obj)
    if form.validate_on_submit():
        new_obj.type=form.type.data
        new_obj.content=form.content.data
        new_obj.news_type=form.type.data
        new_obj.save()
        flash('修改成功')
        #成功后跳转到admin
        return redirect(url_for('admin'))
    return render_template('admin/update.html',form=form)

@app.route('/admin/delete/<pk>/',methods=["POST"])
def delete(pk):
    '''新闻删除'''
    new_obj = News.objects.filter(pk=pk).first()
    if not new_obj:
        return "no"

    #逻辑删除
    new_obj.is_valid=False
    new_obj.save()
   
    #物理删除
    # new_obj.delete()
    
    return "yes"

if __name__ == '__main__':
    app.run(debug=True)