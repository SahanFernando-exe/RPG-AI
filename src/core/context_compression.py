# context-LOD
# recalibrates context after output is given to user every so often

def add_entry(memory_short, entry):
    memory_short.append(entry)
    return memory_short

def summarize_(memory_short, memory_summary, summarizer):
    summary = summarizer("\n".join(memory_short))
    memory_summary.append(summary)
    memory_short.clear()
