"""One explicit native local Ollama route. No retries to other providers."""
import ipaddress
import json
import os
import socket
import urllib.error
import urllib.parse
import urllib.request


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("Inference redirects are disabled")


class LocalChat:
    def __init__(self):
        self.base_url = os.environ.get("AVOCADO_INFERENCE_URL", "http://127.0.0.1:11434").rstrip("/")
        self.key = os.environ.get("AVOCADO_API_KEY", "")

    def complete(self, model, prompt, inputs, settings, frames=None):
        if not self.base_url:
            raise ValueError("Set AVOCADO_INFERENCE_URL to local Ollama; no route is selected")
        url = urllib.parse.urlsplit(self.base_url)
        if url.scheme not in ("http", "https") or not url.hostname or url.username or url.password or url.query or url.fragment:
            raise ValueError("Invalid inference base URL")
        if url.path:
            raise ValueError("Use the native Ollama origin without /v1 or another path")
        if url.hostname != "localhost":
            try:
                ipaddress.ip_address(url.hostname)
            except ValueError as exc:
                raise ValueError("Use localhost or a literal private IP to avoid external DNS") from exc
        addresses = socket.getaddrinfo(url.hostname, url.port or (443 if url.scheme == "https" else 80))
        if not addresses or any(not (ipaddress.ip_address(a[4][0]).is_loopback or ipaddress.ip_address(a[4][0]).is_private) for a in addresses):
            raise ValueError("Inference route must resolve only to local/private addresses")
        if "cloud" in model.lower():
            raise ValueError("Cloud model aliases are not supported")
        allowed = {"temperature", "max_tokens", "num_predict", "num_ctx", "top_p", "seed", "think", "format", "keep_alive"}
        if set(settings) - allowed:
            raise ValueError(f"Unsupported chat settings: {sorted(set(settings) - allowed)}")
        content = prompt + "\n\nInputs:\n" + json.dumps(inputs, ensure_ascii=False)
        images = []
        for frame in frames or []:
            content += f"\nImage {len(images) + 1}: frame {frame['id']} at {frame['timestamp_s']:.3f}s"
            images.append(frame["image"].split(",", 1)[1])
        options = {k: v for k, v in settings.items() if k not in {"think", "format", "keep_alive", "max_tokens"}}
        if "max_tokens" in settings:
            if "num_predict" in settings:
                raise ValueError("Use num_predict or max_tokens, not both")
            options["num_predict"] = settings["max_tokens"]
        message = {"role": "user", "content": content}
        if images:
            message["images"] = images
        payload = {"model": model, "messages": [message], "stream": False, "think": settings.get("think", False),
                   "format": settings.get("format", "json"), "options": options}
        if "keep_alive" in settings:
            payload["keep_alive"] = settings["keep_alive"]
        headers = {"Content-Type": "application/json"}
        if self.key:
            headers["Authorization"] = f"Bearer {self.key}"
        request = urllib.request.Request(self.base_url + "/api/chat", json.dumps(payload).encode(), headers)
        # Ignore ambient HTTP proxies: footage must go directly to the selected route.
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
        # Ollama's model manifest exposes remote_host/remote_model for cloud-backed
        # models. Fail closed if the local manifest cannot be checked. A managed
        # proxy must forward this endpoint as well as /api/chat.
        manifest_url = urllib.parse.urlunsplit((url.scheme, url.netloc, "/api/show", "", ""))
        show_request = urllib.request.Request(manifest_url, json.dumps({"model": model}).encode(), headers)
        try:
            with opener.open(show_request, timeout=15) as response:
                manifest_raw = response.read(2 * 1024 * 1024 + 1)
            if len(manifest_raw) > 2 * 1024 * 1024:
                raise ValueError("Ollama manifest exceeds 2 MiB")
            manifest = json.loads(manifest_raw)
        except (urllib.error.URLError, json.JSONDecodeError) as exc:
            raise ValueError(f"Cannot verify installed local Ollama model {model}; start Ollama and install it before running") from exc
        if manifest.get("remote_host") or manifest.get("remote_model") or not manifest.get("model_info"):
            raise ValueError("A locally installed Ollama model is required; remote/cloud manifests are refused")
        if frames and "vision" not in manifest.get("capabilities", []):
            raise ValueError("Selected local model does not advertise vision capability")
        try:
            with opener.open(request, timeout=180) as response:
                raw = response.read(8 * 1024 * 1024 + 1)
                status = response.status
        except urllib.error.HTTPError as exc:
            raw, status = exc.read(8 * 1024 * 1024 + 1), exc.code
        except urllib.error.URLError as exc:
            raise ValueError(f"Local inference unavailable ({type(exc).__name__}); check local Ollama and the configured route") from exc
        if len(raw) > 8 * 1024 * 1024:
            raise ValueError("Inference response exceeds 8 MiB")
        return {"raw": raw.decode("utf-8"), "request": payload, "route": self.base_url, "http_status": status,
                "local_model_manifest": manifest}


def parse_response(raw):
    envelope = json.loads(raw)
    content = envelope["message"]["content"] if "message" in envelope else envelope["choices"][0]["message"]["content"]
    if not isinstance(content, str):
        raise ValueError("Expected JSON text in the model response")
    if not content.strip():
        raise ValueError("Model returned no final JSON; inspect raw response, disable thinking or increase num_predict")
    text = content.strip()
    if text.startswith("```") and text.endswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(text)
