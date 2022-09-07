calculation_to_hours = 24
name_of_unit = "小时"


def days_to_units(num_of_days):
    return f"{num_of_days} 天有 {num_of_days * calculation_to_hours} {name_of_unit}"


def validate_and_execute():
    try:
        user_input_num = int(num_of_days_ele)
        if user_input_num > 0:
            print(days_to_units(user_input_num))
        elif user_input_num == 0:
            print("数字不能为0。")
        else:
            print("数字不能是负数。")

    except ValueError:
        print("输入错误，请输入正确整数！")


user_input = ""
while user_input != "退出":
    user_input = input("请输入数字：\n")
    for num_of_days_ele in set(user_input.split(",")):
        validate_and_execute()
