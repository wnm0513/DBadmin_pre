import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# 用户表
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.String(20), nullable=False, unique=True, )  # comment='账户')
    name = db.Column(db.String(20), nullable=False, default='', )
    passwd = db.Column(db.String(100), nullable=False, )  # comment='密码')
    email = db.Column(db.String(30), nullable=False, default='', )  # comment='邮箱')
    phone = db.Column(db.String(30), nullable=False, default='', )  # comment='手机')
    ding = db.Column(db.String(64), nullable=False, default='', )  # comment='dingding')
    deptId = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False, default=0, )  # comment='id')
    answer = db.Column(db.String(64), nullable=False, default='banksteel', )  # comment='密保答案')
    issuper = db.Column(db.SmallInteger, nullable=False, default=0, )  # comment='超管0普通，1超管')
    ismanager = db.Column(db.SmallInteger, nullable=False, default=0, )  # comment='经理0普通，1经理')
    ctime = db.Column(db.DATETIME, nullable=False, default=datetime.datetime.now(), )  # comment='创建时间')
    utime = db.Column(db.DATETIME, nullable=False, default=datetime.datetime.now(), )  # comment='修改时间')
    last_login = db.Column(db.DATETIME, nullable=False, default=datetime.datetime.now(), )  # comment='最近登录')
    profile = db.Column(db.String(64), nullable=False, default='#', )  # comment='头像')
    role_name = db.Column(db.String(32), db.ForeignKey('users_roles.role_name'), nullable=False, unique=True,
                          default='', )  # comment='角色名')


    def __repr__(self):
        return '<User %r>' % self.account

    @property
    def is_start(self):
        # 判断用户是否启用，如果不启用，什么都不能操作
        user = User.query.filter_by(account=self.account).first()
        if user.status == 1:
            return True
        else:
            return False

    def is_super(self):
        # 判断用户是否为管理员
        user = User.query.filter_by(account=self.account).first()
        if user.issuper == 1:
            return True
        else:
            return False

    def get_id(self):
        # 取id值
        return str(self.id)

    def is_manager(self):
        # 判断用户是否为经理
        user = User.query.filter_by(account=self.account).first()
        if user.ismanager == 1:
            return True
        else:
            return False

    def is_exists(self):
        # 判断账号是否存在
        user = User.query.filter_by(account=self.account).first()
        if user.id:
            return True
        else:
            return False


# 部门表
class Departments(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    deptname = db.Column(db.String(64), nullable=False, default='', )  # comment='部门名称')
    managerid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, default=0, )  # comment='经理id')

    def __repr__(self):
        return '<Departments %r>' % self.id


# 职位
class UsersRoles(db.Model):
    '''工作表'''
    __tablename__ = 'users_roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, )
    role_name = db.Column(db.String(64), nullable=False, default='', index=True)

    def __repr__(self):
        return '<UsersRoles %r>' % self.id


# 权限表
class PrigroupUsersDbs(db.Model):
    '''工作表'''
    __tablename__ = 'prigroup_users_dbs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prigroupid = db.Column(db.Integer, nullable=False, default=0, )  # comment='权限id')
    uid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, default=0, )  # comment='用户id')
    dbid = db.Column(db.Integer, db.ForeignKey('dbs.id'), nullable=False, default=0, )  # comment='DBid')
    note = db.Column(db.String(50), nullable=False, default='', )  # comment='备注')

    def __repr__(self):
        return '<PrigroupUsersDbs %r>' % self.id


class PrivilegeGroup(db.Model):
    '''工作表'''
    __tablename__ = 'privilege_group'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    groupid = db.Column(db.Integer, nullable=False, default=0, )  # comment='权限组id')
    priid = db.Column(db.Integer, db.ForeignKey('privilege.id'), nullable=False, default=0, )  # comment='权限id')
    name = db.Column(db.String(50), nullable=False, default='', )  # comment='权限组名称')
    note = db.Column(db.String(50), nullable=False, default='', )  # comment='备注')

    def __repr__(self):
        return '<PrivilegeGroup %r>' % self.id


class Privilege(db.Model):
    '''工作表'''
    __tablename__ = 'privilege'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, default='', )  # comment='权限组名称')
    note = db.Column(db.String(50), nullable=False, default='', )  # comment='备注')

    def __repr__(self):
        return '<Privilege %r>' % self.id


# 数据库表
class Dbs(db.Model):
    '''工作表'''
    __tablename__ = 'dbs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(20), nullable=False, default='', )  # comment='ip')
    port = db.Column(db.Integer, nullable=False, default=0, )  # comment='端口')
    name = db.Column(db.String(50), nullable=False, default='', )  # comment='数据库名称')
    note = db.Column(db.String(50), nullable=False, default='', )  # comment='备注')

    def __repr__(self):
        return '<Dbs %r>' % self.id


class DbsDept(db.Model):
    '''工作表'''
    __tablename__ = 'dbs_dept'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dbid = db.Column(db.Integer, db.ForeignKey('dbs.id'), nullable=False, default=0, )  # comment='DBid')
    deptid = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False, default=0, )  # comment='部门id')
    note = db.Column(db.String(50), nullable=False, default='', )  # comment='备注')

    def __repr__(self):
        return '<DbsDept %r>' % self.id