from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from sqlalchemy import and_

from app import login_required
from useddb.models import Workorder, db, Departments, WorkFlow
from . import OrderHistories


@OrderHistories.route('/OrderHistories')
@login_required
def OrderHistory():
    # 定义列表
    workordersinfo = []

    # 查询工单，并以权限分类用户能看到的正在进行的工单
    if g.user.is_super():
        workorders = Workorder.query.all()
    elif g.user.is_manager():
        workorders = db.session.query(Workorder).filter(Workorder.deptid == g.user.deptId).all()
    else:
        workorders = db.session.query(Workorder).filter(Workorder.uid == g.user.id).all()

    for workorder in workorders:
        dept = db.session.query(Departments).filter(Departments.id == workorder.deptid).first()
        workflow = WorkFlow.query.filter(WorkFlow.woid == workorder.id).first()
        workorderinfo = {
            'id': workorder.id,
            'uname': workflow.uname,
            'deptname': dept.deptname,
            'stime': workorder.stime,
            'type': workorder.applyreason,
            'nowstep': workflow.nowstep,
            'auditing': workflow.auditing,
            'status': workorder.status
        }
        workordersinfo.append(workorderinfo)

    return render_template('workorder/OrderHistory/OrderHistory.html', workordersinfo=workordersinfo)
