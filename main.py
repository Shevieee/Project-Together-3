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