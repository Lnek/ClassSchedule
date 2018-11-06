import xlrd


def open_excel(file=""):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print(str(e))


def process_class_schedule_child():
    print("中小幼数据")
    data = open_excel("ClassSchedule_child.xlsx")
    table = data.sheets()[0]
    nrows = table.nrows
    # print(nrows)
    # print(table.row_values(0))
    cn_teacher_name_group = ["何小南", "moirai8803", "叶陆源", "bolidiadia"]
    class_value_num = 0
    cancel_desc = 0
    class_status = 0
    teacher_type = 0
    start_time = 0
    nationality = 0

    less_than_15_min_num = 0

    ns_booked_10_7_num = 0
    ns_completed_10_7_num = 0
    ns_booked_7_11_num = 0
    ns_completed_7_11_num = 0

    cn_booked_10_7_num = 0
    cn_completed_10_7_num = 0
    cn_booked_7_11_num = 0
    cn_completed_7_11_num = 0

    workday_peak_hour_booked_num = 0
    workday_none_peak_hour_booked_num = 0
    workday_peak_hour_completed_num = 0
    workday_none_peak_hour_completed_num = 0

    weekend_peak_hour_booked_num = 0
    weekend_none_peak_hour_booked_num = 0
    weekend_peak_hour_completed_num = 0
    weekend_none_peak_hour_completed_num = 0

    row_index = 0
    for i in table.row_values(0):
        if i == "取消预约描述(Description Of Cancellation)":
            cancel_desc = row_index
        if i == "上课内容":
            class_value_num = row_index
        if i == "上课状态(Class Status)":
            class_status = row_index
        if i == "老师用户名(Teacher's Username)":
            teacher_type = row_index
        if i == "上课开始时间(Class Starting Time)":
            start_time = row_index
        if i == "老师国籍(Nationality)":
            nationality = row_index
        if i == "取消预约时间":
            cancel_time = row_index
        row_index += 1

    for i in range(1, nrows):
        if (table.row_values(i)[class_value_num] == "中小幼-外教口语 一对一测评课"
                and table.row_values(i)[cancel_desc] != "取消测评课预约"
                and table.row_values(i)[class_status] == "无状态"):
            print("存在无状态列表,请去平台查看:")
            print("第" + str(i+1) + "行")
            print(table.row_values(i))
            return
    # open

    cn_10_19_sum, cn_19_23_sum, ns_10_19_sum, ns_19_23_sum, ns_19_21_sum, un_19_21_sum, all_11_21_sum, un_11_21_sum, = process_open_class_child()

    # 15分钟内取消

    # 十五分钟内取消数
    for i in range(1, nrows):

        if (table.row_values(i)[class_value_num] == "中小幼-外教口语 一对一测评课"
                and table.row_values(i)[cancel_desc] == "取消测评课预约"
                and (table.row_values(i)[nationality] != "CN")):

            start_hour = int(table.row_values(i)[start_time].split(" ")[1].split(":")[0])
            start_minutes = int(table.row_values(i)[start_time].split(" ")[1].split(":")[1])
            cancel_hour = int(table.row_values(i)[cancel_time].split(" ")[1].split(":")[0])
            cancel_minutes = int(table.row_values(i)[cancel_time].split(" ")[1].split(":")[1])
            if (19*60 <= start_hour*60+start_minutes < 22*60):
                if (((start_hour*60+start_minutes) - (cancel_hour*60+cancel_minutes)) == 15):
                    continue
            if (0 <= ((start_hour*60+start_minutes) - (cancel_hour*60+cancel_minutes)) <= 15):
                less_than_15_min_num += 1
                if (19 * 60 <= start_hour * 60 + start_minutes <= 22 * 60) and ((start_hour*60+start_minutes) - (cancel_hour*60+cancel_minutes)) == 15:
                    less_than_15_min_num -= 1

    print("十五分钟内外教取消数: " + str(less_than_15_min_num))
    # 外教数据
    for i in range(1, nrows):
        if (table.row_values(i)[class_value_num] == "中小幼-外教口语 一对一测评课"
                and table.row_values(i)[cancel_desc] != "取消测评课预约"
                and (table.row_values(i)[nationality] != "CN")):
            hour = int(table.row_values(i)[start_time].split(" ")[1].split(":")[0])
            minutes = int(table.row_values(i)[start_time].split(" ")[1].split(":")[1])
            if 10*60 <= hour*60+minutes < 19*60:
                ns_booked_10_7_num += 1
                if table.row_values(i)[class_status] == "已完成":
                    ns_completed_10_7_num += 1
            if 19*60 <= hour*60+minutes <= 23*60:
                ns_booked_7_11_num += 1
                if table.row_values(i)[class_status] == "已完成":
                    ns_completed_7_11_num += 1

    print("欧教NS: 10am-7pm open: " + str(ns_booked_10_7_num + ns_10_19_sum) + " booked: " + str(ns_booked_10_7_num) + " completed: " + str(ns_completed_10_7_num))
    print("欧教NS: 7pm-11pm open: " + str(ns_booked_7_11_num + ns_19_23_sum) + " booked: " + str(ns_booked_7_11_num) + " completed: " + str(ns_completed_7_11_num) + "\n")

    # 中教数据
    for i in range(1, nrows):
        if (table.row_values(i)[class_value_num] == "中小幼-外教口语 一对一测评课"
                and table.row_values(i)[cancel_desc] != "取消测评课预约"
                and table.row_values(i)[nationality] == "CN"):
            hour = int(table.row_values(i)[start_time].split(" ")[1].split(":")[0])
            minutes = int(table.row_values(i)[start_time].split(" ")[1].split(":")[1])
            if 10*60 <= hour*60+minutes < 19*60:
                cn_booked_10_7_num += 1
                if table.row_values(i)[class_status] == "已完成":
                    cn_completed_10_7_num += 1
            if 19*60 <= hour*60+minutes < 23*60:
                cn_booked_7_11_num += 1
                if table.row_values(i)[class_status] == "已完成":
                    cn_completed_7_11_num += 1
    print("中教CN: 10am-7pm open: " + str(cn_booked_10_7_num + cn_10_19_sum) + " booked: " + str(cn_booked_10_7_num) + " completed: " + str(cn_completed_10_7_num))
    print("中教CN: 7pm-11pm open: " + str(cn_booked_7_11_num + cn_19_23_sum) + " booked: " + str(cn_booked_7_11_num) + " completed: " + str(cn_completed_7_11_num))

    # 高峰信息
    for i in range(1, nrows):
        if (table.row_values(i)[class_value_num] == "中小幼-外教口语 一对一测评课"
                and table.row_values(i)[cancel_desc] != "取消测评课预约"):
            hour = int(table.row_values(i)[start_time].split(" ")[1].split(":")[0])
            minutes = int(table.row_values(i)[start_time].split(" ")[1].split(":")[1])
            if table.row_values(i)[nationality] != "CN":
                if 19*60 <= hour*60+minutes < 21*60:
                    workday_peak_hour_booked_num += 1
                    if table.row_values(i)[class_status] == "已完成":
                        workday_peak_hour_completed_num += 1
                else:
                    workday_none_peak_hour_booked_num += 1
                    if table.row_values(i)[class_status] == "已完成":
                        workday_none_peak_hour_completed_num += 1

                if 11*60 <= hour*60+minutes < 21*60:
                    weekend_peak_hour_booked_num += 1
                    if table.row_values(i)[class_status] == "已完成":
                        weekend_peak_hour_completed_num += 1
                else:
                    weekend_none_peak_hour_booked_num += 1
                    if table.row_values(i)[class_status] == "已完成":
                        weekend_none_peak_hour_completed_num += 1
    print("")
    print("工作日")
    print("高峰期   open: " + str(ns_19_21_sum + workday_peak_hour_booked_num) +" booked: " + str(workday_peak_hour_booked_num) + "   completed: " + str(workday_peak_hour_completed_num))
    print("非高峰期  open: " + str(un_19_21_sum + workday_none_peak_hour_booked_num) + " booked: " + str(workday_none_peak_hour_booked_num) + " completed: " + str(workday_none_peak_hour_completed_num))
    print("")
    print("周末")
    print("高峰期   open: " + str(all_11_21_sum + weekend_peak_hour_booked_num) + " booked: " + str(weekend_peak_hour_booked_num) + "   completed: " + str(weekend_peak_hour_completed_num))
    print("非高峰期  open: " + str(un_11_21_sum + weekend_none_peak_hour_booked_num) + " booked: " + str(weekend_none_peak_hour_booked_num) + "  completed: " + str(weekend_none_peak_hour_completed_num))
    print("")

def process_open_class_child(filename="child_open.xlsx"):
    data = open_excel(filename)
    table = data.sheets()[0]
    nrows = table.nrows
    time_index = 0
    name_index = 1
    cn_teacher_name_group = ["何小南", "moirai8803", "叶陆源", "bolidiadia"]
    cn_10_19_sum = 0
    cn_19_23_sum = 0

    ns_10_19_sum = 0
    ns_19_23_sum = 0

    ns_19_21_sum = 0
    un_19_21_sum = 0
    all_11_21_sum = 0
    un_11_21_sum = 0

    for i in range(nrows):
        if table.row_values(i)[name_index] in cn_teacher_name_group or table.row_values(i)[name_index][:3] in cn_teacher_name_group:
            start_hour = int(table.row_values(i)[time_index].split("-")[0].split(":")[0])
            start_minutes = int(table.row_values(i)[time_index].split("-")[0].split(":")[1])
            if 10 * 60 <= start_hour * 60 + start_minutes < 19 * 60:
                cn_10_19_sum += 1
            if 19 * 60 <= start_hour * 60 + start_minutes < 23 * 60:
                cn_19_23_sum += 1

            if 11 * 60 <= start_hour * 60 + start_minutes < 21 * 60:
                all_11_21_sum += 1
            else:
                un_11_21_sum +=1
        else:
            start_hour = int(table.row_values(i)[time_index].split("-")[0].split(":")[0])
            start_minutes = int(table.row_values(i)[time_index].split("-")[0].split(":")[1])
            if 10 * 60 <= start_hour * 60 + start_minutes < 19 * 60:
                ns_10_19_sum += 1
            if 19 * 60 <= start_hour * 60 + start_minutes < 23 * 60:
                ns_19_23_sum += 1
            if 19 * 60 <= start_hour * 60 + start_minutes < 21 * 60:
                ns_19_21_sum += 1
            else:
                un_19_21_sum += 1
            if 11 * 60 <= start_hour * 60 + start_minutes < 21 * 60:
                all_11_21_sum += 1
            else:
                un_11_21_sum +=1
    return cn_10_19_sum, cn_19_23_sum, ns_10_19_sum, ns_19_23_sum, ns_19_21_sum, un_19_21_sum, all_11_21_sum, un_11_21_sum,

def process_class_schedule_adult():
    print("成人数据")
    data = open_excel("ClassSchedule_adult.xlsx")
    table = data.sheets()[0]
    nrows = table.nrows
    # print(nrows)
    # print(table.row_values(0))
    class_value_num = 0
    cancel_desc = 0
    class_status = 0
    teacher_type = 0
    start_time = 0
    cancel_time = 0

    less_than_15_min_num = 0

    ns_booked_10_14_num = 0
    ns_completed_10_14_num = 0
    ns_booked_14_19_num = 0
    ns_completed_14_19_num = 0
    ns_booked_19_23_num = 0
    ns_completed_19_23_num = 0

    cn_booked_10_14_num = 0
    cn_completed_10_14_num = 0
    cn_booked_14_19_num = 0
    cn_completed_14_19_num = 0
    cn_booked_19_23_num = 0
    cn_completed_19_23_num = 0

    cn_workday_peak_hour_booked_19_20_num = 0
    cn_workday_peak_hour_booked_20_21_num = 0
    cn_workday_peak_hour_booked_21_22_num = 0
    cn_workday_peak_hour_completed_19_20_num = 0
    cn_workday_peak_hour_completed_20_21_num = 0
    cn_workday_peak_hour_completed_21_22_num = 0

    ns_workday_peak_hour_booked_19_20_num = 0
    ns_workday_peak_hour_booked_20_21_num = 0
    ns_workday_peak_hour_booked_21_22_num = 0
    ns_workday_peak_hour_completed_19_20_num = 0
    ns_workday_peak_hour_completed_20_21_num = 0
    ns_workday_peak_hour_completed_21_22_num = 0

    row_index = 0
    for i in table.row_values(0):
        if i == "取消预约描述(Description Of Cancellation)":
            cancel_desc = row_index
        if i == "上课内容":
            class_value_num = row_index
        if i == "上课状态(Class Status)":
            class_status = row_index
        if i == "老师用户名(Teacher's Username)":
            teacher_type = row_index
        if i == "上课开始时间(Class Starting Time)":
            start_time = row_index
        if i == "取消预约时间":
            cancel_time = row_index
        row_index += 1
    sums = 0
    # 十五分钟内取消数
    for i in range(1, nrows):
        if (table.row_values(i)[class_value_num] == "口语 一对一测评课"
                and table.row_values(i)[cancel_desc] == "取消测评课预约"):
            sums += 1
            start_hour = int(table.row_values(i)[start_time].split(" ")[1].split(":")[0])
            start_minutes = int(table.row_values(i)[start_time].split(" ")[1].split(":")[1])
            cancel_hour = int(table.row_values(i)[cancel_time].split(" ")[1].split(":")[0])
            cancel_minutes = int(table.row_values(i)[cancel_time].split(" ")[1].split(":")[1])
            if (19*60 <= start_hour*60+start_minutes < 22*60):
                if (((start_hour*60+start_minutes) - (cancel_hour*60+cancel_minutes)) == 15):
                    continue
            if (0 <= ((start_hour*60+start_minutes) - (cancel_hour*60+cancel_minutes)) <= 15):
                less_than_15_min_num += 1
                if (19 * 60 <= start_hour * 60 + start_minutes <= 22 * 60) and ((start_hour*60+start_minutes) - (cancel_hour*60+cancel_minutes)) == 15:
                    less_than_15_min_num -= 1

    print("十五分钟内取消数: " + str(less_than_15_min_num))

    novalue_flag = 0
    for i in range(1, nrows):
        if (table.row_values(i)[class_value_num] == "口语 一对一测评课"
                and table.row_values(i)[cancel_desc] != "取消测评课预约"
                and table.row_values(i)[class_status] == "无状态"):
            print("存在无状态列表,请去平台查看:")
            print("第" + str(i + 1) + "行")
            novalue_flag = 1
    if novalue_flag == 1:
        return

    # before open

    cn_10_14_sum, cn_14_19_sum, cn_19_23_sum, ns_10_14_sum, ns_14_19_sum, ns_19_23_sum, cn_19_20_sum, cn_20_21_sum, cn_21_22_sum, ns_19_20_sum, ns_20_21_sum, ns_21_22_sum = process_open_class_adult("adult_open.xlsx")

    # 外教数据
    for i in range(1, nrows):
        if (table.row_values(i)[class_value_num] == "口语 一对一测评课"
                and table.row_values(i)[cancel_desc] != "取消测评课预约"
                and (table.row_values(i)[teacher_type][0:2] == "T_" or table.row_values(i)[teacher_type][0:4] == "Demo")):
            hour = int(table.row_values(i)[start_time].split(" ")[1].split(":")[0])
            minutes = int(table.row_values(i)[start_time].split(" ")[1].split(":")[1])
            if 10 * 60 <= hour * 60 + minutes < 14 * 60:
                ns_booked_10_14_num += 1
                if table.row_values(i)[class_status] == "已完成":
                    ns_completed_10_14_num += 1
            if 14 * 60 <= hour * 60 + minutes < 19 * 60:
                ns_booked_14_19_num += 1
                if table.row_values(i)[class_status] == "已完成":
                    ns_completed_14_19_num += 1
            if 19 * 60 <= hour * 60 + minutes < 24 * 60:
                ns_booked_19_23_num += 1
                if table.row_values(i)[class_status] == "已完成":
                    ns_completed_19_23_num += 1

            if 19 * 60 <= hour * 60 + minutes < 20 * 60:
                ns_workday_peak_hour_booked_19_20_num += 1
                if table.row_values(i)[class_status] == "已完成":
                    ns_workday_peak_hour_completed_19_20_num += 1
            if 20 * 60 <= hour * 60 + minutes < 21 * 60:
                ns_workday_peak_hour_booked_20_21_num += 1
                if table.row_values(i)[class_status] == "已完成":
                    ns_workday_peak_hour_completed_20_21_num += 1
            if 21 * 60 <= hour * 60 + minutes < 22 * 60:
                ns_workday_peak_hour_booked_21_22_num += 1
                if table.row_values(i)[class_status] == "已完成":
                    ns_workday_peak_hour_completed_21_22_num += 1

    print("欧教NS: 10am-2pm open: " + str(ns_10_14_sum + ns_booked_10_14_num) + " booked: " + str(ns_booked_10_14_num) + " completed: " + str(ns_completed_10_14_num))
    print("欧教NS: 2pm-7pm open: " + str(ns_14_19_sum + ns_booked_14_19_num) + " booked: " + str(ns_booked_14_19_num) + " completed: " + str(ns_completed_14_19_num))
    print("欧教NS: 7pm-11pm open: " + str(ns_19_23_sum + ns_booked_19_23_num) + " booked: " + str(ns_booked_19_23_num) + " completed: " + str(ns_completed_19_23_num) + "\n")
    print("欧教NS: 高峰 7pm-8pm open: " + str(ns_19_20_sum + ns_workday_peak_hour_booked_19_20_num) + " booked: " + str(
        ns_workday_peak_hour_booked_19_20_num) + " completed: " + str(ns_workday_peak_hour_completed_19_20_num))
    print("欧教NS: 高峰 8pm-9pm open: " + str(ns_20_21_sum + ns_workday_peak_hour_booked_20_21_num) + " booked: " + str(
        ns_workday_peak_hour_booked_20_21_num) + " completed: " + str(ns_workday_peak_hour_completed_20_21_num))
    print("欧教NS: 高峰 9pm-10pm open: " + str(ns_21_22_sum + ns_workday_peak_hour_booked_21_22_num) + " booked: " + str(
        ns_workday_peak_hour_booked_21_22_num) + " completed: " + str(ns_workday_peak_hour_completed_21_22_num) + "\n")

    # 中教数据
    for i in range(1, nrows):
        if (table.row_values(i)[class_value_num] == "口语 一对一测评课"
                and table.row_values(i)[cancel_desc] != "取消测评课预约"
                and table.row_values(i)[teacher_type][0:2] != "T_"
                and table.row_values(i)[teacher_type][0:4] != "Demo"):
            hour = int(table.row_values(i)[start_time].split(" ")[1].split(":")[0])
            minutes = int(table.row_values(i)[start_time].split(" ")[1].split(":")[1])
            if 10 * 60 <= hour * 60 + minutes < 14 * 60:
                cn_booked_10_14_num += 1
                if table.row_values(i)[class_status] == "已完成":
                    cn_completed_10_14_num += 1
            if 14 * 60 <= hour * 60 + minutes < 19 * 60:
                cn_booked_14_19_num += 1
                if table.row_values(i)[class_status] == "已完成":
                    cn_completed_14_19_num += 1
            if 19 * 60 <= hour * 60 + minutes < 24 * 60:
                cn_booked_19_23_num += 1
                if table.row_values(i)[class_status] == "已完成":
                    cn_completed_19_23_num += 1
            if 19 * 60 <= hour * 60 + minutes < 20 * 60:
                cn_workday_peak_hour_booked_19_20_num += 1
                if table.row_values(i)[class_status] == "已完成":
                    cn_workday_peak_hour_completed_19_20_num += 1
            if 20 * 60 <= hour * 60 + minutes < 21 * 60:
                cn_workday_peak_hour_booked_20_21_num += 1
                if table.row_values(i)[class_status] == "已完成":
                    cn_workday_peak_hour_completed_20_21_num += 1
            if 21 * 60 <= hour * 60 + minutes < 22 * 60:
                cn_workday_peak_hour_booked_21_22_num += 1
                if table.row_values(i)[class_status] == "已完成":
                    cn_workday_peak_hour_completed_21_22_num += 1

    print("中教CN: 10am-2pm open: " + str(cn_booked_10_14_num + cn_10_14_sum) + " booked: " + str(
        cn_booked_10_14_num) + " completed: " + str(cn_completed_10_14_num))
    print("中教CN: 2pm-7pm open: " + str(cn_booked_14_19_num + cn_14_19_sum) + " booked: " + str(
        cn_booked_14_19_num) + " completed: " + str(cn_completed_14_19_num))
    print("中教CN: 7pm-11pm open: " + str(cn_booked_19_23_num + cn_19_23_sum) + " booked: " + str(
        cn_booked_19_23_num) + " completed: " + str(cn_completed_19_23_num) + "\n")
    print("中教CN: 高峰 7pm-8pm open: " + str(cn_19_20_sum + cn_workday_peak_hour_booked_19_20_num) + " booked: " + str(
        cn_workday_peak_hour_booked_19_20_num) + " completed: " + str(cn_workday_peak_hour_completed_19_20_num))
    print("中教CN: 高峰 8pm-9pm open: " + str(cn_20_21_sum + cn_workday_peak_hour_booked_20_21_num) + " booked: " + str(
        cn_workday_peak_hour_booked_20_21_num) + " completed: " + str(cn_workday_peak_hour_completed_20_21_num))
    print("中教CN: 高峰 9pm-10pm open: " + str(cn_21_22_sum + cn_workday_peak_hour_booked_21_22_num) + " booked: " + str(
        cn_workday_peak_hour_booked_21_22_num) + " completed: " + str(cn_workday_peak_hour_completed_21_22_num) + "\n")


def process_open_class_adult(filename="adult_open.xlsx"):
    data = open_excel(filename)
    table = data.sheets()[0]
    nrows = table.nrows
    time_index = 0
    name_index = 1
    cn_10_14_sum = 0
    cn_14_19_sum = 0
    cn_19_23_sum = 0
    cn_19_20_sum = 0
    cn_20_21_sum = 0
    cn_21_22_sum = 0
    ns_10_14_sum = 0
    ns_14_19_sum = 0
    ns_19_23_sum = 0
    ns_19_20_sum = 0
    ns_20_21_sum = 0
    ns_21_22_sum = 0

    for i in range(nrows):
        if (table.row_values(i)[name_index][0:4] != "Demo"
                and table.row_values(i)[name_index][0:2] != "欧美"
                and table.row_values(i)[name_index][0:2] != "T_"):
            start_hour = int(table.row_values(i)[time_index].split("-")[0].split(":")[0])
            start_minutes = int(table.row_values(i)[time_index].split("-")[0].split(":")[1])
            end_hour = int(table.row_values(i)[time_index].split("-")[1].split(":")[0])
            end_minutes = int(table.row_values(i)[time_index].split("-")[1].split(":")[1])
            if (10 * 60 <= start_hour * 60 + start_minutes) and (end_hour * 60 + end_minutes <= 14 * 60):
                cn_10_14_sum += 1
            if (14 * 60 <= start_hour * 60 + start_minutes) and (end_hour * 60 + end_minutes <= 19 * 60):
                cn_14_19_sum += 1
            if (19 * 60 <= start_hour * 60 + start_minutes) and (end_hour * 60 + end_minutes <= 24 * 60):
                cn_19_23_sum += 1
            if (19 * 60 <= start_hour * 60 + start_minutes) and (end_hour * 60 + end_minutes <= 20 * 60):
                cn_19_20_sum += 1
            if (20 * 60 <= start_hour * 60 + start_minutes) and (end_hour * 60 + end_minutes <= 21 * 60):
                cn_20_21_sum += 1
            if (21 * 60 <= start_hour * 60 + start_minutes) and (end_hour * 60 + end_minutes <= 22 * 60):
                cn_21_22_sum += 1
    for i in range(nrows):
        if (table.row_values(i)[name_index][0:4] == "Demo"
                or table.row_values(i)[name_index][0:2] == "欧美"
                or table.row_values(i)[name_index][0:2] == "T_"):
            start_hour = int(table.row_values(i)[time_index].split("-")[0].split(":")[0])
            start_minutes = int(table.row_values(i)[time_index].split("-")[0].split(":")[1])
            end_hour = int(table.row_values(i)[time_index].split("-")[1].split(":")[0])
            end_minutes = int(table.row_values(i)[time_index].split("-")[1].split(":")[1])
            if (10 * 60 <= start_hour * 60 + start_minutes) and (end_hour * 60 + end_minutes <= 14 * 60):
                ns_10_14_sum += 1
            if (14 * 60 <= start_hour * 60 + start_minutes) and (end_hour * 60 + end_minutes <= 19 * 60):
                ns_14_19_sum += 1
            if (19 * 60 <= start_hour * 60 + start_minutes) and (end_hour * 60 + end_minutes <= 24 * 60):
                ns_19_23_sum += 1
            if (19 * 60 <= start_hour * 60 + start_minutes) and (end_hour * 60 + end_minutes <= 20 * 60):
                ns_19_20_sum += 1
            if (20 * 60 <= start_hour * 60 + start_minutes) and (end_hour * 60 + end_minutes <= 21 * 60):
                ns_20_21_sum += 1
            if (21 * 60 <= start_hour * 60 + start_minutes) and (end_hour * 60 + end_minutes <= 22 * 60):
                ns_21_22_sum += 1

    return cn_10_14_sum, cn_14_19_sum, cn_19_23_sum, ns_10_14_sum, ns_14_19_sum, ns_19_23_sum, cn_19_20_sum, cn_20_21_sum, cn_21_22_sum, ns_19_20_sum ,ns_20_21_sum, ns_21_22_sum

def main():
    process_class_schedule_child()
    process_class_schedule_adult()
main()