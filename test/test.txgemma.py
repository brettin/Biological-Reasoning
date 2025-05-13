from openai import OpenAI

input_type = "{Drug SMILES}"
drug_smiles = "CN1C(=O)CN=C(C2=CCCCC2)c2cc(Cl)ccc21"

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, default=8000,
                    help="port number, default 8000")
parser.add_argument("--host", type=str, default="localhost",
		    help="host name, default localhost")
parser.add_argument("--model", type=str, default="mistralai/Mixtral-8x7B-Instruct-v0.1",
                    help="repo/model, default mistralai/Mixtral-8x7B-Instruct-v0.1")
parser.add_argument("--key", type=str, default="EMPTY",
        help="the key passed to the vllm entrypoint when it was started")

args = parser.parse_args()
print(f'using host: {args.host}')
print(f'using port: {args.port}')
print(f'using model: {args.model}')
print(f'using api-key: {args.key}')

import json
from huggingface_hub import hf_hub_download

# Download google/txgemma prompts
tdc_prompts_filepath = hf_hub_download(
    repo_id=args.model,
    filename="tdc_prompts.json",
)

with open(tdc_prompts_filepath, "r") as f:
    tdc_prompts_json = json.load(f)

# Set OpenAI's API key and API base to use vLLM's API server.
openai_api_base = f"http://{args.host}:{args.port}/v1"
client = OpenAI(
    api_key=args.key,
    base_url=openai_api_base,
)

task_names=[]
for task_name, value in tdc_prompts_json.items():
    task_names.append(task_name)
    if input_type in value:
        TDC_PROMPT = tdc_prompts_json[task_name].replace(input_type, drug_smiles)
        print("User: ")
        print(TDC_PROMPT)

        # sampling_params = SamplingParams({"prompt_logprobs": 1, "logprobs": 1))
        chat_response = client.chat.completions.create(
            model=args.model,
            # logprobs=1,
            # top_logprobs=1,
            messages=[
                {"role": "user", "content": TDC_PROMPT},
            ],
            temperature=0.0,
            max_tokens=2056,
        )
        print("Chat response: ", chat_response.choices[0].message.content)

    else:
        continue
