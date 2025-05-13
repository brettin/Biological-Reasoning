MODEL_VARIANT = "9b-chat"
model_id = f"google/txgemma-{MODEL_VARIANT}"

if MODEL_VARIANT == "2b-predict":
    additional_args = {}
else:
    additional_args = {
        "quantization_config": BitsAndBytesConfig(load_in_8bit=True)
    }

tokenizer = AutoTokenizer.from_pretrained(model_id)

