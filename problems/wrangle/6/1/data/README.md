# 书店 App 原始导出

数据来自本仓库产品分析线的虚构练习库。原始种子有 48 位读者，生成器读取八张表，将读者扩到 2,000 位，然后模拟流水重复回传、字段缺失和不同设备的时间写法。仓库内可运行 `python problems/wrangle/6/1/data/generate.py` 重建本目录的 CSV，固定种子为 20261123，只使用 Python 标准库。[原表结构](../../../../analytics/_db/readerapp/schema.sql) · [原始种子](../../../../analytics/_db/readerapp/seed.sql)

原有读者、登录和交易记录参与导出。新增读者的城市、设备、渠道从原始登记中抽样，注册日和每周访问时刻有随机偏移。读者有不同的访问和购买频率，可在两个月内表现出相似的消费习惯。生成器还为新增读者模拟实验分组、会员开通和少量退款。checkout_visits 与 renewal_offers 保留原库的专项样本。

| 文件 | 明细行数（含重复） | 一行记录的内容 |
| --- | ---: | --- |
| readers.csv | 2,050 | 读者编号、注册日、获客渠道、城市和设备 |
| events.csv | 39,986 | 带时间戳的一次搜索、浏览、加购、下单或支付操作 |
| payments.csv | 6,734 | 一笔付款或退款；正金额代表有效付款 |
| logins.csv | 10,612 | 一次登录 |
| memberships.csv | 419 | 一次会员开始、续订或取消 |
| assignments.csv | 1,999 | 一位读者进入一次实验的分组记录 |
| checkout_visits.csv | 40 | 一次结账访问以及后续加购、下单时刻 |
| renewal_offers.csv | 32 | 一个到期订阅周期和续费日期 |

## 构建特征表

从项目页下载数据包并解压，让 `data/` 与导出的 `features.py` 并列。在有 pandas 的环境运行 `python features.py`，当前工作目录会得到 `features.csv`。Notebook 放在同一目录，从头执行各格即可。输入使用 readers、events、payments 三张表；其余五张可与产品分析线对照。

项目把无偏移的时间当作 UTC，带偏移的时间换算为 UTC。按各自主键去重；渠道 test 是测试账号，空城市归为 unknown。有效付款以唯一 payment_id 计单，负数退款、零元和缺字段的流水不计入订单和消费额。

以 2025-03-01 00:00 UTC 为界，观察窗口从 1 月 30 日零点起到 3 月 1 日零点前。标签窗口从 3 月 1 日零点起到 3 月 31 日零点前。这 30 天内没有正向付款记作 churned=1。所有已登记且在截止日前注册的正式读者各占一行，含零事件和零订单读者。最近付款查截止前全部历史，以 UTC 自然日计；从未下单记为 31。

输出供机器学习项目直接读取，列序如下。

```text
user_id,city,signup_days,sessions_30d,active_days_30d,events_30d,orders_30d,spend_30d,avg_basket,days_since_last_order,churned
```

## 来源与许可

原始库、扩展脚本和 CSV 均为 code-dojo 项目内的合成教学数据，无第三方数据或真实用户记录。随本仓库提供，仓库声明保留全部权利，未另授开放许可。[仓库许可声明](../../../../../README.md#license)
