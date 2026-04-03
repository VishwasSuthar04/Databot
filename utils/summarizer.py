import pandas as pd
import numpy as np

def summarize(data, data_type):

    if data_type == 'dataframe':
        return summarize_dataframe(data)
    elif data_type == 'text':
        return summarize_text(data)
    else:
        return "Unsupported file type!"


def summarize_dataframe(df):
    summary = []

    # Basic info
    summary.append(f"📊 Total Rows: {df.shape[0]}")
    summary.append(f"📋 Total Columns: {df.shape[1]}")
    summary.append(f"🏷️ Column Names: {', '.join(df.columns.tolist())}")

    # Missing values
    missing = df.isnull().sum()
    total_missing = missing.sum()
    summary.append(f"❌ Total Missing Values: {total_missing}")

    if total_missing > 0:
        summary.append("Missing Values Per Column:")
        for col, count in missing.items():
            if count > 0:
                summary.append(f"   → {col}: {count} missing")

    # Duplicate rows
    duplicates = df.duplicated().sum()
    summary.append(f"🔁 Duplicate Rows: {duplicates}")

    # Numeric columns analysis
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if numeric_cols:
        summary.append(f"\n📈 Numeric Columns Analysis:")
        for col in numeric_cols:
            summary.append(f"\n  🔢 {col}:")
            summary.append(f"     Mean    : {df[col].mean():.2f}")
            summary.append(f"     Median  : {df[col].median():.2f}")
            summary.append(f"     Min     : {df[col].min():.2f}")
            summary.append(f"     Max     : {df[col].max():.2f}")
            summary.append(f"     Std Dev : {df[col].std():.2f}")

    # Text columns analysis
    text_cols = df.select_dtypes(include=['object']).columns.tolist()

    if text_cols:
        summary.append(f"\n📝 Text Columns Analysis:")
        for col in text_cols:
            unique_count = df[col].nunique()
            most_common = df[col].value_counts().idxmax()
            summary.append(f"\n  🔤 {col}:")
            summary.append(f"     Unique Values : {unique_count}")
            summary.append(f"     Most Common   : {most_common}")

    return '\n'.join(summary)


def summarize_text(text):
    summary = []

    # Basic info
    words = text.split()
    lines = text.split('\n')

    summary.append(f"📄 Total Words: {len(words)}")
    summary.append(f"📋 Total Lines: {len(lines)}")
    summary.append(f"🔤 Total Characters: {len(text)}")

    # First 200 characters preview
    summary.append(f"\n👀 Preview:")
    summary.append(text[:200] + "...")

    return '\n'.join(summary)