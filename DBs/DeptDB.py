from flask import (
    g, render_template, redirect, url_for
)
from sqlalchemy import and_

from login_required import login_required
from useddb.models import db, User, Departments, DbsDept, Dbs
from . import DeptDBs


@DeptDBs.route('/DeptDB', methods=['GET', 'POST'])
@login_required
def DeptDB():
    deptdbs = []
    if g.user.is_super():
        depts = Departments.query.all()
    elif g.user.is_manager():
        depts = db.session.query(Departments).filter(Departments.id == g.user.deptId)
    else:
        depts = []
    for dept in depts:
        manager = db.session.query(User.id, User.account, User.name).join(Departments,
                                                                          User.id == Departments.managerid).filter(
            and_(User.deptId == dept.id, User.ismanager == 1)).first()
        ducount = DbsDept.query.filter_by(deptid=dept.id).count()
        dbids = db.session.query(DbsDept.id, Dbs.name, Dbs.ip, Dbs.port, Dbs.note, DbsDept.deptid) \
            .join(DbsDept, DbsDept.dbid == Dbs.id) \
            .filter(DbsDept.deptid == dept.id) \
            .all()
        # 存储各个部门数据库的信息
        dbsinfo = []
        for dbs1 in dbids:
            dbinfo = {
                "dbsdeptid": dbs1.id,
                "name": dbs1.name,
                "ip": dbs1.ip,
                "port": dbs1.port,
                "note": dbs1.note,
            }
            dbsinfo.append(dbinfo)
        if manager is None:
            mid = 0
            mgrname = "暂无数据"
        else:
            mid = manager.id
            mgrname = manager.name
        deptmanager = {
            "id": dept.id,
            "name": dept.deptname,
            "mid": mid,
            "mgrname": mgrname,
            "deptdbcount": ducount,
            "dbsinfo": dbsinfo
        }
        # 汇总一个部门的所有信息
        deptdbs.append(deptmanager)

    return render_template('DBs/DeptDB/DeptDB.html', deptdbs=deptdbs)


# 从部门中移除
@DeptDBs.route('/delete/<dbsdeptid>/', methods=['GET', 'POST'])
@login_required
def delete(dbsdeptid):
    dbdept = DbsDept.query.filter_by(id=dbsdeptid).first()
    if dbdept:
        db.session.delete(dbdept)
        db.session.commit()

    return redirect(url_for('DeptDB.DeptDB'))
