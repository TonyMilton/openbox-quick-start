# Temporal + OpenBox Governance Example

A minimal Python project demonstrating how to integrate [OpenBox](https://openbox.ai) governance with [Temporal](https://temporal.io) workflows.

## Setup

```bash
uv sync
```

Create a `.env` file in the project root:

```env
OPENBOX_URL=https://core.openbox.ai
OPENBOX_API_KEY=your_api_key_here
```

## Running

```bash
just dev      # Start Temporal server + worker together
just run      # Execute the hello workflow (in a separate terminal)
just weather  # Execute the weather workflow (in a separate terminal)
```

Or run the server and worker separately:

```bash
just server   # Start the Temporal dev server
just worker   # Start the worker
```
