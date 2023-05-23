# coding:utf-8

from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from werkzeug.utils import secure_filename
import os
import cv2
import time

from datetime import timedelta

# 设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


app = Flask(__name__)
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)


# @app.route('/upload', methods=['POST', 'GET'])
@app.route('/upload', methods=['POST', 'GET'])  # 添加路由
def upload():
    if request.method == 'POST':
        f1 = request.files['file1']
        f2 = request.files['file2']

        if not (f1 and allowed_file(f1.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})

        if not (f2 and allowed_file(f2.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})

        basepath = os.path.dirname(__file__)  # 当前文件所在路径

        upload_path1 = os.path.join(basepath, 'static/images', secure_filename(f1.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        upload_path2 = os.path.join(basepath, 'static/images', secure_filename(f2.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径

        f1.save(upload_path1)
        f2.save(upload_path2)



        # 使用Opencv转换一下图片格式和名称
        img = cv2.imread(upload_path1)
        cv2.imwrite(os.path.join(basepath, 'static/images', 'test.jpg'), img)

        return render_template('upload_ok.html', val1=time.time())

    return render_template('upload.html')


if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0', port=8987, debug=True)