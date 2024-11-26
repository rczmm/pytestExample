import requests


def wk_main_user_handre_fuse(workOrderId, remark):
    wk_main_user_handre_fuse_url = api.HOST + 'stage-api/workorder/workorderhandleinfo/mainuserhandrefuse'
    data = {
        "workOrderId": workOrderId,
        'remark': remark}
    res = requests.post(url=wk_main_user_handre_fuse_url, headers=api.headers, json=data).json()
    print(res)
    assert res['success'] == 'True', f'id为{id}的工单驳回请求成功-->{res}'


wk_main_user_handre_fuse(workOrderCode_toBeMainUserExecuted, '脚本自动驳回')
