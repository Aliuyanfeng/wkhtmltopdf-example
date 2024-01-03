import json
import platform
import time

import pdfkit



class PDFExportUtil(object):

    def start_export(self):
        """导出报告"""

        # 字典存储pdf映射数据
        result = dict()

        file_path = f"./template/report.js"
        insert_data = f"""
            var reportJsonData = {json.dumps(result, indent=4, ensure_ascii=False)}
        """.strip()
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(insert_data)
        self.html_to_pdf()

    def html_to_pdf(self):
        """html 转 pdf"""
        # 启动参数
        wkhtmltopdf_options = {
            'enable-local-file-access': '--enable-local-file-access',
            'encoding': "utf-8",
            'javascript-delay': '10000',
            'header-left': '报告-[date] [time]',
            'header-font-size': 8,
            'header-spacing': 5,
            'footer-center': '第[page] / [topage]页',
            'footer-font-size': 8,
            'margin-top': 10,
            'dpi': 300
        }
        # 下载的wkhtmltopdf绝对路径，修改为自己存放的位置
        if platform.system() == 'Linux':
            path_wkthmltopdf = r"/usr/local/wkhtmltox/bin/wkhtmltopdf"
        else:
            path_wkthmltopdf = r'E:\wkhtmltopdf\bin\wkhtmltopdf.exe'

        config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

        # html 输入 out.pdf 输出
        cur_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        out_path = f"./file/report/报告({cur_time}).pdf"
        pdfkit.from_file("./template/index.html", out_path, configuration=config,
                         options=wkhtmltopdf_options)
        return True
        """更新报告路径"""
        params = {
            "id": r_id,
            "report_path": r_path
        }
        sql = """
            update t_report_export set report_path = %(report_path)s where id = %(id)s
        """
        self.pg_conn.execute(sql, params)
        self.pg_conn.commit()
