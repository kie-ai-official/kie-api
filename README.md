# Kie.ai API — Python client

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE) [![Hosted on Synexa](https://img.shields.io/badge/hosted%20on-Synexa-6366f1.svg)](https://synexa.ai/explore/google/veo3.1?utm_source=github&utm_medium=ugc&utm_campaign=kie-ai-official&utm_content=readme-badge&utm_term=tier-c)

Kie.ai is an API marketplace that resells access to third-party generation models, such as Google Veo, ByteDance Seedance and Google's image models, behind a single key and credit balance, so developers do not have to open an account with each vendor. This repository is a Python client for the same kind of multi-model access through Kie.ai-class hosted endpoints on Synexa: Veo 3.1 and Seedance 2.5 for video and Nano Banana Pro for images, all callable with one `pip install` and one API token.

You get a blocking `run()` that takes a prompt and returns the result URL, a non-blocking create-and-poll path for batches, and webhook delivery for services that would rather be called back. The client has a single runtime dependency and no model weights. It is aimed at developers who want frontier video and image models behind one interface, one bill and one set of retry semantics, without integrating three vendor SDKs.

> **Try it now:** [https://synexa.ai/explore/google/veo3.1](https://synexa.ai/explore/google/veo3.1?utm_source=github&utm_medium=ugc&utm_campaign=kie-ai-official&utm_content=readme-top&utm_term=tier-c) — the hosted model behind this client. New accounts get a free trial credit.

## Contents

- [Why this client](#why-this-client)
- [Installation](#installation)
- [Quickstart](#quickstart)
- [Hosted models](#hosted-models)
- [Parameters](#parameters)
- [Advanced usage](#advanced-usage)
- [About Kie.ai](#about-kie-ai)
- [Use cases](#use-cases)
- [FAQ](#faq)
- [License](#license)

## Why this client

- **None of these models can be self-hosted.** Veo 3.1, Seedance 2.5 and Nano Banana Pro are proprietary; there is no checkpoint to download, so an aggregator endpoint is the only way to call them from your own code without three vendor accounts.
- **One key, one billing line.** Each model is a separate slug on the same endpoint with the same auth, request shape and job lifecycle, so switching a workload from Veo to Seedance is a one-string change.
- **No cold start and no queue to build.** The models are resident on Synexa's fleet; you submit a job and poll or receive a webhook, and the same code path serves a single request or a batch of thousands.
- **Predictable cost.** `google/veo3.1` is billed at $0.80 per run, `bytedance/seedance-2.5` at $0.473 and `google/nano-banana-pro` at $0.10, so you can price a job before submitting it and route by budget.

## Installation

```bash
pip install git+https://github.com/kie-ai-official/kie-api.git
```

Then set your API key (create one at [synexa.ai](https://synexa.ai?utm_source=github&utm_medium=ugc&utm_campaign=kie-ai-official&utm_content=readme-apikey&utm_term=tier-c)):

```bash
export SYNEXA_API_KEY="sk-..."
```

## Quickstart

```python
import kie_api

output = kie_api.run({
    "prompt": "A cinematic shot of a lighthouse at dawn"
})
print(output)   # URL(s) of the generated result
```

Or with an explicit client:

```python
from kie_api import Client

client = Client(api_key="sk-...")
output = client.run({"prompt": "A cinematic shot of a lighthouse at dawn"})
```

## Hosted models

| Model | Category | What it does | Price / run |
|---|---|---|---|
| [`google/veo3.1`](https://synexa.ai/explore/google/veo3.1?utm_source=github&utm_medium=ugc&utm_campaign=kie-ai-official&utm_content=readme-models&utm_term=tier-c) | text-to-video | New and improved version of Veo 3, with higher-fidelity video, context-aware audio, reference image and last frame support | $0.8 |
| [`bytedance/seedance-2.5`](https://synexa.ai/explore/bytedance/seedance-2.5?utm_source=github&utm_medium=ugc&utm_campaign=kie-ai-official&utm_content=readme-models&utm_term=tier-c) | text-to-video | Seedance 2.5 generates a single-shot video of up to 30 seconds from a text prompt, with synchronised audio. | $0.473 |
| [`google/nano-banana-pro`](https://synexa.ai/explore/google/nano-banana-pro?utm_source=github&utm_medium=ugc&utm_campaign=kie-ai-official&utm_content=readme-models&utm_term=tier-c) | text-to-image | Google's state of the art image generation and editing model 🍌🍌 | $0.1 |

The default model is **`google/veo3.1`**; pass `model="owner/name"` to `run()` to use another one from the table.

## Parameters

### `google/veo3.1`

| Field | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `seed` | integer | no | `1234` | 0, 10000000 | Random Seed |
| `mode` | string | no | `generate` | generate, upscale, extend | Operation mode |
| `count` | integer | no | `1` | 1, 4 | Number of image variations to generate |
| `prompt` | string | no | `A serene mountain landscape at sunset wi…` | — | Text description for video generation |
| `media_id` | string | no | — | — | Reference media id for upscale/extend (format: '<uuid>:<id>') |
| `end_image` | file | no | — | — | Video ends with this frame (Optional) |
| `references` | files | no | — | — | Reference images (Optional) |
| `resolution` | string | no | `original` | original, 1080p, 4K | Output resolution (original = no upscale) |
| `start_image` | file | no | — | — | Video starts with this frame (Optional) |
| `aspect_ratio` | string | no | `landscape` | landscape, portrait | Output image aspect ratio |

### `bytedance/seedance-2.5`

| Field | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `prompt` | string | yes | `A lone fisherman rows out at dawn across…` | — | The text prompt used to generate the video |
| `resolution` | string | no | `720p` | 480p, 720p, 1080p | Video resolution - 480p for faster generation, 720p for balance, 1080p for high quality. |
| `duration` | string | no | `auto` | auto, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 1… | Duration of the video in seconds. Supports 4 to 30 seconds, or auto to let the model decide based on the prompt. |
| `aspect_ratio` | string | no | `auto` | auto, 21:9, 16:9, 4:3, 1:1, 3:4, 9:16 | The aspect ratio of the generated video. Use 16:9 for landscape, 9:16 for portrait/vertical, 1:1 for square, 21:9 for ultrawide cinematic, or auto to let the model decide. |
| `generate_audio` | boolean | no | `True` | — | Whether to generate synchronized audio for the video, including sound effects, ambient sounds, and lip-synced speech. The cost of video generation is the same regardless of whether audio is generated or not. |
| `bitrate_mode` | string | no | `standard` | standard, high | Output bitrate mode. 'high' requests a higher-quality, larger-file encode from the model; 'standard' uses the default bitrate. |

### `google/nano-banana-pro`

| Field | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `seed` | integer | no | `1234` | 0, 10000000 | Random Seed |
| `count` | integer | no | `1` | 1, 4 | Number of image variations to generate |
| `prompt` | string | yes | `A serene mountain landscape at sunset wi…` | — | Text description for image generation |
| `references` | files | no | — | — | Reference images (Optional) |
| `resolution` | string | no | `original` | original, 2k, 4k | Output resolution (original = no upscale) |
| `aspect_ratio` | string | no | `landscape` | landscape, portrait | Output image aspect ratio |

## Advanced usage

**Submit without blocking, then poll:**

```python
prediction = client.run(input, wait=False)      # returns immediately
prediction = client.wait(prediction, timeout=300)
print(prediction["output"])
```

**Webhook on completion:**

```python
client.run(input, wait=False, webhook="https://your-app.example/hooks/synexa")
```

**Errors:**

```python
from kie_api import ModelError, PredictionTimeout

try:
    output = client.run(input)
except ModelError as e:
    print("failed:", e, e.prediction and e.prediction.get("id"))
except PredictionTimeout:
    print("still running — poll later")
```

Status values you will see on a prediction: `starting` → `processing` → `succeeded` | `failed`.

## About Kie.ai

Kie.ai ([kie.ai](https://kie.ai)) is a model API marketplace. Rather than training its own models, it fronts models from other vendors, including Google Veo, ByteDance Seedance, Suno, Flux and image models from Google and OpenAI, behind a single API key, a credit balance and a shared task-polling convention. Its appeal is operational: one account, one invoice, one request shape, and access to models whose first-party APIs are regionally restricted, waitlisted or priced for enterprise. Developers use it to add several generation capabilities to a product without maintaining a vendor integration for each.

The endpoints exposed by this client provide the same pattern with three of the most requested models. `google/veo3.1` is Google DeepMind's video model, an update to Veo 3 with higher-fidelity output, context-aware generated audio, reference-image conditioning and start and end frames; the endpoint also exposes an `mode` for operations such as extend and upscale via a `media_id`. `bytedance/seedance-2.5` is ByteDance's text-to-video model, producing a single-shot clip of 4 to 30 seconds at up to 1080p with synchronised sound effects, ambience and lip-synced speech. `google/nano-banana-pro` is Google's image generation and editing model, which takes a prompt and optional reference images and returns one or more variations at a chosen aspect ratio and resolution.

Typical outputs are short ads and social clips from Veo or Seedance, image assets and edits from Nano Banana Pro, and mixed pipelines where an image is generated first and then animated. Limits to plan for: one run yields one video clip (or `count` image variations), Seedance caps at 30 seconds, and the per-run cost differs by an order of magnitude between the image model and Veo, so route by need.

This client does not talk to Kie.ai. The hosted endpoints it uses are `google/veo3.1`, `bytedance/seedance-2.5` and `google/nano-banana-pro` on Synexa, which provide the same models Kie.ai resells but through Synexa's API and billing. Kie.ai's own marketplace, credit pricing and model catalogue are at [kie.ai](https://kie.ai).

**Official project:** https://kie.ai

## Use cases

- **Premium video ads** — call `run()` on `google/veo3.1` with a prompt, `start_image` and `end_image` for a controlled shot with context-aware audio.
- **Budget-tiered video** — route drafts to `bytedance/seedance-2.5` at $0.473 and only final renders to Veo 3.1 at $0.80, switching by slug.
- **Image-then-animate pipelines** — generate a hero frame with `google/nano-banana-pro`, then pass it as the start frame to a video model in the same script.
- **Reference-guided edits** — send product photos as `references` to Nano Banana Pro with a prompt describing the change, and request several `count` variations.
- **Extend or upscale a clip** — use Veo 3.1's `mode` with the `media_id` of a previous run to lengthen or upscale it without regenerating from scratch.
- **Automated social publishing** — enqueue prompts from a content calendar through the poll path and receive finished assets by webhook.

## FAQ

**Is there a Kie.ai API?**

Yes. Kie.ai's own marketplace API is at kie.ai. This client does not call it; it calls hosted endpoints on Synexa that serve the same models, `google/veo3.1`, `bytedance/seedance-2.5` and `google/nano-banana-pro`, through Synexa's API and billing.

**How much does Kie.ai-class access cost through this client?**

`google/veo3.1` is billed at $0.80 per run, `bytedance/seedance-2.5` at $0.473 per run and `google/nano-banana-pro` at $0.10 per run. There is no credit pack or subscription; you pay per completed job.

**Can I run these models without a GPU?**

Yes, and only this way: Veo 3.1, Seedance 2.5 and Nano Banana Pro are hosted-only models with no public weights. Your machine needs Python and network access; generation happens on Synexa's GPUs.

**Does this client work with a Kie.ai account or credits?**

No. It uses a Synexa API token and Synexa billing. Kie.ai credits, task IDs and callback formats are not compatible with it.

**What input formats does it accept?**

All three models take a text `prompt`. Veo 3.1 optionally takes `start_image`, `end_image`, `references`, `resolution`, `aspect_ratio`, `seed`, and `mode` plus `media_id` for extend and upscale. Seedance 2.5 optionally takes `resolution`, `duration` (4 to 30 seconds), `aspect_ratio`, `generate_audio` and `bitrate_mode`. Nano Banana Pro optionally takes `references`, `count`, `resolution`, `aspect_ratio` and `seed`.

**Is this the official Kie.ai SDK?**

No. This is an independent client that wraps hosted endpoints on Synexa. Kie.ai's official marketplace and API are at https://kie.ai.

## Related

- [Kie.ai](https://kie.ai) — the marketplace this client is positioned against
- [Synexa Python client](https://github.com/synexa-ai/synexa-python) — the general-purpose SDK this client builds on
- [google/veo3.1 on Synexa](https://synexa.ai/explore/google/veo3.1) — high-fidelity video with context-aware audio and reference images
- [bytedance/seedance-2.5 on Synexa](https://synexa.ai/explore/bytedance/seedance-2.5) — text-to-video up to 30 seconds with synchronised audio
- [google/nano-banana-pro on Synexa](https://synexa.ai/explore/google/nano-banana-pro) — image generation and editing with reference images

## License

MIT. This is an independent, community-maintained client and is not affiliated with or endorsed by the authors of Kie.ai. Model weights and trademarks belong to their respective owners.


_Last reviewed: 2026-09-22_
