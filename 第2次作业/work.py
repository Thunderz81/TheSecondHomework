import os
import random
from datetime import datetime


class Student:
    def __init__(self, index, name, gender, class_name, student_id, college):
        self.index = index
        self.name = name
        self.gender = gender
        self.class_name = class_name
        self.student_id = student_id
        self.college = college

    def __str__(self):
        return (
            f"序号: {self.index}, 姓名: {self.name}, 性别: {self.gender}, "
            f"班级: {self.class_name}, 学号: {self.student_id}, 学院: {self.college}"
        )


class ExamSystem:
    def __init__(self, student_file_path, exam_output_path):
        self.student_file_path = student_file_path
        self.exam_output_path = exam_output_path
        self.students = {}
        self.exam_arrangement = []

    def load_students(self):
        with open(self.student_file_path, "r", encoding="utf-8") as file:
            next(file)  # 跳过表头
            for line in file:
                parts = line.strip().split("\t")
                if len(parts) != 6:
                    continue
                index, name, gender, class_name, student_id, college = parts
                self.students[student_id] = Student(
                    index=index,
                    name=name,
                    gender=gender,
                    class_name=class_name,
                    student_id=student_id,
                    college=college,
                )

    def query_student(self, student_id):
        return self.students[student_id]

    def random_roll_call(self, count):
        if count <= 0:
            raise ValueError("请输入大于 0 的整数。")
        if count > len(self.students):
            raise ValueError(f"输入数量超过学生总数（{len(self.students)}），请重新输入。")
        return random.sample(list(self.students.values()), count)

    def generate_exam_arrangement(self):
        shuffled_students = random.sample(list(self.students.values()), len(self.students))
        generated_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.exam_arrangement = []

        with open(self.exam_output_path, "w", encoding="utf-8") as file:
            file.write(f"生成时间：{generated_time}\n")
            file.write("考场座位号\t姓名\t学号\n")
            for seat_no, student in enumerate(shuffled_students, start=1):
                self.exam_arrangement.append(
                    {
                        "seat_no": seat_no,
                        "name": student.name,
                        "student_id": student.student_id,
                    }
                )
                file.write(f"{seat_no}\t{student.name}\t{student.student_id}\n")

    def load_exam_arrangement_from_file(self):
        arrangement = []
        with open(self.exam_output_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        for line in lines[2:]:
            parts = line.strip().split("\t")
            if len(parts) != 3:
                continue
            seat_no, name, student_id = parts
            try:
                seat_no = int(seat_no)
            except ValueError:
                continue
            arrangement.append(
                {
                    "seat_no": seat_no,
                    "name": name,
                    "student_id": student_id,
                }
            )

        self.exam_arrangement = arrangement

    def generate_admit_cards(self, output_dir="准考证"):
        if not self.exam_arrangement:
            self.load_exam_arrangement_from_file()

        if not self.exam_arrangement:
            raise ValueError("没有可用的考场安排信息，无法生成准考证。")

        os.makedirs(output_dir, exist_ok=True)
        width = max(2, len(str(len(self.exam_arrangement))))

        for info in self.exam_arrangement:
            file_name = f"{info['seat_no']:0{width}d}.txt"
            file_path = os.path.join(output_dir, file_name)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(f"考场座位号：{info['seat_no']}\n")
                file.write(f"姓名：{info['name']}\n")
                file.write(f"学号：{info['student_id']}\n")


def main():
    system = ExamSystem("人工智能编程语言学生名单.txt", "考场安排表.txt")

    try:
        system.load_students()
    except FileNotFoundError:
        print(f"未找到名单文件：{system.student_file_path}")
        return
    except Exception as error:
        print(f"读取名单时发生错误：{error}")
        return

    while True:
        student_id = input("请输入要查询的学号：").strip()
        try:
            print(system.query_student(student_id))
            break
        except KeyError:
            print(f"未找到学号为 {student_id} 的学生，请重新输入。")

    try:
        count = int(input("请输入随机点名学生数量：").strip())
        selected_students = system.random_roll_call(count)
    except ValueError as error:
        print(error)
        return

    print("\n随机点名结果：")
    for i, student in enumerate(selected_students, start=1):
        print(f"{i}. {student}")

    system.generate_exam_arrangement()
    print(f"\n已生成考场安排表：{system.exam_output_path}")

    try:
        system.generate_admit_cards("准考证")
        print("已在准考证文件夹生成 01.txt、02.txt 等文件。")
    except Exception as error:
        print(f"生成准考证失败：{error}")


if __name__ == "__main__":
    main()
