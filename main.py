import telebot
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


class Attendance(Base):
    __tablename__ = 'attendance'

    id = Column(Integer, primary_key=True)
    class_info = Column(String)
    attendance = Column(Integer)
    sickness = Column(Integer)
    cold = Column(Integer)
    other_reason = Column(Integer)
    total_students = Column(Integer)


engine = create_engine('sqlite:///attendance.db')
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

TOKEN = '5151364048:AAHzaKEVC_tKAB_78icRi68h0NKqq-ysu9U'
bot = telebot.TeleBot(TOKEN)


class States:
    CLASS_INPUT = 1
    ATTENDANCE_INPUT = 2
    SICKNESS_INPUT = 3
    COLD_INPUT = 4
    OTHER_REASON_INPUT = 5
    TOTAL_STUDENTS_INPUT = 6


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id,
                     "Привет! Я бот для сбора данных. Давай начнем. Введи номер класса и букву (например, 10г):")
    bot.register_next_step_handler(message, handle_class_input)


def handle_class_input(message):
    try:
        class_info = message.text

        bot.send_message(message.chat.id, f"Теперь введи количество присутствующих в {class_info} классе:")
        bot.register_next_step_handler(message, handle_attendance_input, class_info)

    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")


def handle_attendance_input(message, class_info):
    try:
        attendance = int(message.text)

        bot.send_message(message.chat.id, f"Теперь введи количество отсутствующих по болезни в {class_info} классе:")
        bot.register_next_step_handler(message, handle_sickness_input, class_info, attendance)

    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите число.")


def handle_sickness_input(message, class_info, attendance):
    try:
        sickness = int(message.text)

        bot.send_message(message.chat.id,
                         f"Теперь введи количество отсутствующих в том числе по ОРВИ в {class_info} классе:")
        bot.register_next_step_handler(message, handle_cold_input, class_info, attendance, sickness)

    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите число.")


def handle_cold_input(message, class_info, attendance, sickness):
    try:
        cold = int(message.text)

        bot.send_message(message.chat.id,
                         f"Теперь введи количество отсутствующих по иным причинам в {class_info} классе:")
        bot.register_next_step_handler(message, handle_other_reason_input, class_info, attendance, sickness, cold)

    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите число.")


def handle_other_reason_input(message, class_info, attendance, sickness, cold):
    try:
        other_reason = int(message.text)

        bot.send_message(message.chat.id, f"Теперь введи общее количество учащихся в {class_info} классе:")
        bot.register_next_step_handler(message, handle_total_students_input, class_info, attendance, sickness, cold,
                                       other_reason)

    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите число.")