from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Text, Boolean
from sqlalchemy.orm import relationship, declarative_base

# Базовый класс для моделей
Base = declarative_base()

class User(Base):
    """Модель пользователя"""
    __tablename__ = "users"
    __table_args__ = {"schema": "mychat"}  # Указываем схему

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    is_active = Column(Boolean, default=True)  
    created_at = Column(TIMESTAMP, server_default='now()')
    is_admin = Column(Boolean, default=False)

    # Связь с сообщениями
    messages = relationship("Message", back_populates="user")

class Chat(Base):
    """Модель чата"""
    __tablename__ = "chats"
    __table_args__ = {"schema": "mychat"}

    chat_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("mychat.users.id"), nullable=False)
    created_at = Column(TIMESTAMP, server_default='now()')

    # Связи
    user = relationship("User", backref="chats")
    messages = relationship("Message", back_populates="chat")

class Message(Base):
    """Модель сообщения"""
    __tablename__ = "messages"
    __table_args__ = {"schema": "mychat"}

    message_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("mychat.chats.chat_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("mychat.users.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default='now()')

    # Связи
    user = relationship("User", back_populates="messages")
    chat = relationship("Chat", back_populates="messages")