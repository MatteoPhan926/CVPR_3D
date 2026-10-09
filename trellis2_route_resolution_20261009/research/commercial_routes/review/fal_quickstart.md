> ## Documentation Index
> Fetch the complete documentation index at: https://fal.ai/docs/llms.txt
> Use this file to discover all available pages before exploring further.

> ## Agent Instructions
> fal has two developer products. Model APIs run hosted models through an API key. fal Serverless deploys your own Python apps and models on fal GPUs.
> To call a hosted model, start with the [Quick Start](https://fal.ai/docs/documentation/quickstart.md) and the [Model APIs overview](https://fal.ai/docs/documentation/model-apis/overview.md).
> To deploy your own model with fal Serverless, start with these pages:
> - [Introduction to Serverless](https://fal.ai/docs/documentation/serverless/index.md): What fal Serverless is and the three ways to deploy on it.
> - [Installation & Setup](https://fal.ai/docs/documentation/development/getting-started/installation.md): Install the fal CLI with `pip install fal` and authenticate.
> - [Quick Start](https://fal.ai/docs/documentation/development/getting-started/quick-start.md): Build a Hello World app, test it with `fal run`, and ship it with `fal deploy`.
> - [App Lifecycle](https://fal.ai/docs/documentation/development/app-lifecycle.md): How a `fal.App` goes from code to running runners.
> - [Define Your Endpoints](https://fal.ai/docs/documentation/development/endpoints-overview.md): Structure the API endpoints that your app exposes.
> - [Deploy to Production](https://fal.ai/docs/documentation/deployment/deploy-to-production.md): Persistent URLs, authentication modes, and automatic scaling.
> - [Machine Types](https://fal.ai/docs/documentation/deployment/machine-types.md): Available GPU and CPU machine types and how to choose one.
> - [Pricing](https://fal.ai/docs/documentation/serverless/pricing.md): Per-second billing and the runner states that are billed.
> - [Scaling Parameter Reference](https://fal.ai/docs/documentation/deployment/scale-your-application.md): Parameters that control runners, concurrency, and scale to zero.
> - [Optimizing Cold Starts](https://fal.ai/docs/documentation/serverless/optimizations/optimize-cold-starts.md): Causes of cold starts and ways to make them shorter.
> - [Examples](https://fal.ai/docs/examples/index.md): Complete Serverless apps for image, video, audio, 3D, realtime, and multi-GPU workloads.
> - [Migrating to fal](https://fal.ai/docs/documentation/development/migrating-to-fal.md): Guides to move an existing Docker server or an app from another platform to fal.
> fal Serverless deploys need access that the fal team approves for each account. Request access at https://fal.ai/dashboard/serverless-get-started.

# Quick Start

> Get started with fal in minutes

fal gives you two ways to work with AI models. If you want to generate images, video, audio, or other media, the [Model APIs](/docs/documentation/model-apis/overview) let you call 1,000+ production-ready models with a single API call. If you have your own model to deploy, [Serverless](/docs/documentation/serverless) gives you the full lifecycle: develop, test, deploy, and scale on the same infrastructure that powers the [marketplace](https://fal.ai/models).

Both paths start with an [API key](/docs/documentation/model-apis/authentication) and take a few minutes. The "consume" path is for calling existing models through fal's [client libraries](/docs/documentation/model-apis/inference/client-setup) or HTTP. The "deploy" path is for teams bringing their own models to run on fal's GPU infrastructure, using the same [fal.App](/docs/documentation/development/app-setup) framework that powers every model on the platform.

<Tabs>
  <Tab title="I want to consume a model">
    ### What do you want to build?

    <CardGroup cols={2}>
      <Card title="Generate Images" icon="image" href="/docs/examples/image-generation/generate-images-from-text">
        Create images from text prompts with FLUX, Nano Banana 2, and more
      </Card>

      <Card title="Generate Videos" icon="video" href="/docs/examples/video-generation/generate-videos-from-image">
        Transform images into videos with Kling 3.0, Sora 2, and other models
      </Card>

      <Card title="Transcribe Audio" icon="microphone" href="/docs/examples/audio-speech/convert-speech-to-text">
        Convert speech to text with Whisper
      </Card>

      <Card title="Use LLMs" icon="message-bot" href="/docs/examples/integrations/use-llms">
        Build with Llama, Mistral, and other large language models
      </Card>

      <Card title="Fast FLUX" icon="bolt" href="/docs/examples/image-generation/fast-flux">
        Ultra-fast image generation with optimized FLUX
      </Card>

      <Card title="Build a Workflow UI" icon="window" href="/docs/examples/integrations/custom-workflow-ui">
        Create interfaces for complex AI workflows
      </Card>

      <Card title="Next.js Integration" icon="code" href="/docs/examples/integrations/nextjs">
        Build full-stack AI apps with Next.js and fal
      </Card>

      <Card title="Vercel Integration" icon="cloud" href="/docs/examples/integrations/vercel">
        Deploy AI-powered apps on Vercel with fal
      </Card>

      <Card title="n8n Integration" icon="diagram-project" href="/docs/examples/integrations/n8n">
        Automate workflows by connecting fal models to n8n
      </Card>
    </CardGroup>

    ### Quick example

    Generate your first image in under a minute.

    <Steps>
      <Step title="Install the client">
        <CodeGroup>
          ```bash Python theme={null}
          pip install fal-client
          ```

          ```bash JavaScript theme={null}
          npm install @fal-ai/client
          ```
        </CodeGroup>
      </Step>

      <Step title="Set your API key">
        Get a key from the [fal dashboard](https://fal.ai/dashboard/keys) and set it as an environment variable:

        ```bash theme={null}
        export FAL_KEY="your-api-key-here"
        ```
      </Step>

      <Step title="Generate an image">
        <CodeGroup>
          ```python Python theme={null}
          import fal_client

          result = fal_client.subscribe("fal-ai/flux/schnell", arguments={
              "prompt": "a futuristic cityscape at sunset"
          })
          print(result["images"][0]["url"])
          ```

          ```javascript JavaScript theme={null}
          import { fal } from "@fal-ai/client";

          const result = await fal.subscribe("fal-ai/flux/schnell", {
            input: { prompt: "a futuristic cityscape at sunset" }
          });
          console.log(result.data.images[0].url);
          ```

          ```bash cURL theme={null}
          curl -X POST "https://queue.fal.run/fal-ai/flux/schnell" \
            -H "Authorization: Key $FAL_KEY" \
            -H "Content-Type: application/json" \
            -d '{"prompt": "a futuristic cityscape at sunset"}'
          ```
        </CodeGroup>
      </Step>
    </Steps>
  </Tab>

  <Tab title="I want to deploy a model">
    ### What do you want to deploy?

    <CardGroup cols={2}>
      <Card title="Text-to-Image Model" icon="image" href="/docs/examples/image-generation/deploy-text-to-image-model">
        Deploy Sana, FLUX, or your custom image generation model
      </Card>

      <Card title="Text-to-Video Model" icon="video" href="/docs/examples/video-generation/deploy-text-to-video-model">
        Deploy WAN or other video generation models
      </Card>

      <Card title="Text-to-Speech Model" icon="volume-high" href="/docs/examples/audio-speech/deploy-text-to-speech-model">
        Deploy Kokoro or custom voice synthesis models
      </Card>

      <Card title="Text-to-Music Model" icon="music" href="/docs/examples/audio-speech/deploy-text-to-music-model">
        Deploy DiffRhythm or music generation models
      </Card>

      <Card title="ComfyUI Server" icon="server" href="/docs/examples/image-generation/deploy-comfyui-server">
        Run ComfyUI workflows as a serverless API
      </Card>

      <Card title="LoRA Training" icon="sliders" href="/docs/examples/image-generation/deploy-wan-lora-training">
        Fine-tune WAN video generation with LoRA training
      </Card>

      <Card title="Multi-GPU Inference" icon="microchip" href="/docs/examples/video-generation/deploy-multi-gpu-inference">
        Scale generation across multiple GPUs with streaming
      </Card>

      <Card title="3D Progressive Rendering" icon="cube" href="/docs/examples/video-generation/deploy-3d-progressive-rendering">
        Stream real-time text-to-3D reconstruction
      </Card>

      <Card title="Real-time Video-to-Video" icon="video" href="/docs/examples/video-generation/deploy-realtime-video-to-video-model">
        Run real-time video-to-video with object detection
      </Card>

      <Card title="Real-time World Model" icon="globe" href="/docs/examples/video-generation/deploy-realtime-world-model">
        Deploy a real-time world model powered by Matrix-Game
      </Card>

      <Card title="Custom Container" icon="docker" href="/docs/examples/deploy-models-with-custom-containers">
        Deploy any model with custom Docker containers
      </Card>
    </CardGroup>

    ### Migrating from another platform?

    <CardGroup cols={2}>
      <Card title="Migrate from Replicate" icon="arrow-right" href="/docs/documentation/development/migrate-from-replicate">
        Move your Replicate models to fal
      </Card>

      <Card title="Migrate from Modal" icon="arrow-right" href="/docs/documentation/development/migrate-from-modal">
        Move your Modal apps to fal
      </Card>

      <Card title="Migrate from RunPod" icon="arrow-right" href="/docs/documentation/development/migrate-from-runpod">
        Move your RunPod Serverless workers to fal
      </Card>

      <Card title="Migrate Docker Server" icon="arrow-right" href="/docs/documentation/development/migrate-external-docker-server">
        Move your existing Docker-based inference server to fal
      </Card>
    </CardGroup>

    ### Quick example

    Deploy your first app in under 2 minutes.

    <Steps>
      <Step title="Install the CLI and authenticate">
        ```bash theme={null}
        pip install fal
        fal auth login
        ```
      </Step>

      <Step title="Create your app">
        Create a file called `my_app.py`:

        ```python my_app.py theme={null}
        import fal
        from pydantic import BaseModel

        class Input(BaseModel):
            prompt: str

        class Output(BaseModel):
            message: str

        class MyApp(fal.App):
            @fal.endpoint("/")
            def run(self, input: Input) -> Output:
                return Output(message=f"Hello from fal! You said: {input.prompt}")
        ```

        <Note>
          Declare your endpoint input as a Pydantic model. A bare scalar parameter such as
          `def run(self, prompt: str)` is interpreted as a **query** parameter, so callers
          sending a JSON body — which is what the clients and every example here do — get
          an HTTP 422 response.
        </Note>
      </Step>

      <Step title="Validate with fal run">
        Always run this before deploying. `fal run` boots your app on a temporary worker — running `setup()` and your endpoints just like production — so errors surface here instead of as a production crashloop.

        ```bash theme={null}
        fal run my_app.py::MyApp
        ```
      </Step>

      <Step title="Deploy to production">
        Once `fal run` works, promote the same app to a persistent URL:

        ```bash theme={null}
        fal deploy my_app.py::MyApp
        ```
      </Step>
    </Steps>

    <Card title="Deploy a real model" icon="rocket" href="/docs/documentation/development/getting-started/deploy-your-first-image-generator">
      Step-by-step guide to deploying an image generation model
    </Card>
  </Tab>
</Tabs>

***

## Next Steps

<CardGroup cols={3}>
  <Card title="Get Your API Key" icon="key" href="/docs/documentation/model-apis/authentication">
    Create an API key to authenticate your requests
  </Card>

  <Card title="AI Tools" icon="message-bot" href="/docs/documentation/model-apis/mcp">
    Use AI coding assistants to build with fal faster
  </Card>

  <Card title="Explore Models" icon="cube" href="https://fal.ai/models">
    Browse 1,000+ available models
  </Card>
</CardGroup>
