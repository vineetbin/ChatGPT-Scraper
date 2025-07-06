"""
SQLAlchemy models for the brand mentions system.
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Index
from sqlalchemy.sql import func
from .database import Base


class Prompt(Base):
    """
    Model for storing ChatGPT prompts and their responses.
    """
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True)
    prompt_text = Column(Text, nullable=False)
    response_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Index for faster queries
    __table_args__ = (Index('idx_prompts_created_at', 'created_at'),)


class BrandMention(Base):
    """
    Model for storing brand mention counts per prompt.
    """
    __tablename__ = "brand_mentions"

    id = Column(Integer, primary_key=True, index=True)
    prompt_id = Column(Integer, nullable=False)
    brand_name = Column(String(50), nullable=False)
    mention_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Indexes for faster queries
    __table_args__ = (
        Index('idx_brand_mentions_prompt_id', 'prompt_id'),
        Index('idx_brand_mentions_brand_name', 'brand_name'),
        Index('idx_brand_mentions_created_at', 'created_at'),
    )


class BrandSummary(Base):
    """
    Model for storing aggregated brand mention totals.
    """
    __tablename__ = "brand_summaries"

    id = Column(Integer, primary_key=True, index=True)
    brand_name = Column(String(50), unique=True, nullable=False)
    total_mentions = Column(Integer, default=0)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Index for faster queries
    __table_args__ = (Index('idx_brand_summaries_brand_name', 'brand_name'),) 