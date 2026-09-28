import json
import os
import torch
from datasets import Dataset
from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    DataCollatorForSeq2Seq,
    Seq2SeqTrainer,
    Seq2SeqTrainingArguments,
)

MODEL_NAME = "Salesforce/codet5-base"
OUTPUT_DIR = "./models/semantix_codet5"
TRAIN_DATA_PATH = "dataset/train.json"
VAL_DATA_PATH = "dataset/validation.json"

print("[INFO] Initializing Memory-Optimized CodeT5 Pipeline...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

with open(TRAIN_DATA_PATH, "r") as f:
    train_data = json.load(f)

with open(VAL_DATA_PATH, "r") as f:
    val_data = json.load(f)

train_dataset = Dataset.from_list(train_data)
val_dataset = Dataset.from_list(val_data)


def preprocess_function(examples):
    # Truncate inputs to 256 tokens and use dynamic padding via DataCollator
    model_inputs = tokenizer(
        examples["input"], max_length=256, truncation=True
    )

    labels = tokenizer(
        examples["target"], max_length=32, truncation=True
    )

    labels_with_ignore = []
    for label in labels["input_ids"]:
        labels_with_ignore.append(
            [l if l != tokenizer.pad_token_id else -100 for l in label]
        )

    model_inputs["labels"] = labels_with_ignore
    return model_inputs


print("[INFO] Tokenizing dataset with dynamic lengths...")
tokenized_train = train_dataset.map(preprocess_function, batched=True)
tokenized_val = val_dataset.map(preprocess_function, batched=True)

training_args = Seq2SeqTrainingArguments(
    output_dir=OUTPUT_DIR,
    evaluation_strategy="epoch",
    learning_rate=5e-4,
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    gradient_accumulation_steps=4,
    weight_decay=0.01,
    save_total_limit=1,
    num_train_epochs=20,
    predict_with_generate=True,
    fp16=False,
    logging_steps=5,
    report_to="none",
    dataloader_num_workers=0,
)

data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_val,
    tokenizer=tokenizer,
    data_collator=data_collator,
)

print("[INFO] Starting CodeT5 fine-tuning...")
trainer.train()

print("[INFO] Saving fine-tuned model...")
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print(f"[SUCCESS] Fine-tuned model saved successfully to: {OUTPUT_DIR}")